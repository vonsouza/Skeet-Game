"""

This program implements an awesome version of skeet.
"""
import arcade
import math
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 500

RIFLE_WIDTH = 100
RIFLE_HEIGHT = 20
RIFLE_COLOR = arcade.color.DARK_RED

BULLET_RADIUS = 5
BULLET_COLOR = arcade.color.BLACK_OLIVE
BULLET_SPEED = 10

TARGET_RADIUS = 20
TARGET_COLOR = arcade.color.CARROT_ORANGE
TARGET_SAFE_COLOR = arcade.color.AIR_FORCE_BLUE
TARGET_SAFE_RADIUS = 15
"""
The Point and Velocity class are classes that hold values, they do not have another function than init values
but they are very important
"""
class Point():
    def __init__ (self):
        self.x = 0
        self.y = 0
        
class Velocity():
    def __init__ (self):
        self.dx = 0
        self.dy = 0
        
class Rifle:
    """
    The rifle is a rectangle that tracks the mouse.
    """
    def __init__(self):
        self.center = Point()
        self.center.x = 0
        self.center.y = 0
        self.angle = 45

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, RIFLE_WIDTH, RIFLE_HEIGHT, RIFLE_COLOR, 360-self.angle)

"""
The flying object is the parent class but it also works as a grandparent class for target and its child classes
"""
class Flying_object():
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 0
        self.alive = True
    """
    Flying_object as parent holds values and methods that inherit to its child classes, in order to fulfill its purpose
    the child classes doesn't need to stablish the methods because they can easily take from the parent class.
    """
    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        
    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, self.color)    
    
    """
    We should be checking for 0 as well to cover the bottom and left (left isn't as important for this one).
    """
    def is_off_screen(self, screen_width, screen_height):
        off_screen = True
        if (self.center.x < screen_width and self.center.x >= 0) and (self.center.y >= 0 and self.center.y < screen_height):
            off_screen = False
        else:
            off_screen = True
            self.alive = False
            
        return off_screen
            
        
class Bullet(Flying_object):
    def __init__(self):
        super().__init__()
        self.radius = BULLET_RADIUS
        self.color = BULLET_COLOR
    
    """
    Trig functions will likely be helpful in determining the x and y components of an angle.
    They can be found in the math library
    """
    def fire(self, angle):
        self.velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        self.velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED
"""
The target type, direction, velocity, and timing to release (delay) are random
"""
class Target(Flying_object):
    def __init__(self):
        super().__init__()
        """
        The initial position of the target is anywhere along the top half of the left side the screen.
        """
        self.radius = TARGET_RADIUS
        self.color = TARGET_COLOR
        self.center.x = 0
        self.center.y = random.uniform(SCREEN_HEIGHT / 2, SCREEN_HEIGHT)
    """
    An abstract method that reminds it child classes to use draw method
    """
    def draw(self):
        pass  
    
    def hit(self):
        self.alive = False 
        return 1
    
class standard_target(Target):
    def __init__(self):
        super().__init__()
        """
        The horizontal component of the velocity should be between 1 and 5 pixels/frame.
​
        The vertical component of the velocity should be between -2 and +5 pixels/frame.
        """
        self.velocity.dx = random.uniform(1,5)
        self.velocity.dy = random.uniform(-2,5)
   
    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, self.color)

"""
I use the principle of inheritance to create various classes for the different targets
"""
class strong_target(Target):
    def __init__(self):
        super().__init__()
        """
        To give the user a greater chance to hit the strong target,
        it should move more slowly than the others.
        """
        self.velocity.dx = random.uniform(1,3)
        self.velocity.dy = random.uniform(-2,3)
        self.lives = 3 
    
    def draw(self):
        arcade.draw_circle_outline(self.center.x, self.center.y, self.radius, self.color)
        text_x = self.center.x - (self.radius / 2)
        text_y = self.center.y - (self.radius / 2)
        arcade.draw_text(repr(self.lives), text_x, text_y, self.color, font_size=20)
    """
    The hit values changes for Strong and Safe target because they return a different score than the standard target
    """
    def hit(self):
        self.lives -= 1
        if self.lives == 0:
            self.alive = False
            return 5
        else:
            return 1
       
class safe_target(Target):
    def __init__(self):
        super().__init__()
        self.radius = TARGET_SAFE_RADIUS
        self.color = TARGET_SAFE_COLOR
        self.velocity.dx = random.uniform(1,3)
        self.velocity.dy = random.uniform(-2,3)
             
    def draw(self):
        """
        Since the safe target is a rectangle you most wonder why it holds a radius value...
        well it interacts with the bullet (circle) and that's why it holds a radius value
        """
        arcade.draw_rectangle_filled(self.center.x, self.center.y, self.radius, self.radius, self.color)
        
    def hit(self):
        self.alive = False 
        return -10
    
class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Rifle
        Target (and it's sub-classes)
        Point
        Velocity
        Bullet
​
    This class will then call the appropriate functions of
    each of the above classes.
​
    You are welcome to modify anything in this class, but mostly
    you shouldn't have to. There are a few sections that you
    must add code to.
    """
    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.rifle = Rifle()
        self.score = 0

        self.bullets = []

        # TODO: Create a list for your targets (similar to the above bullets)
        self.targets = []


        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.rifle.draw()

        for bullet in self.bullets:
            bullet.draw()

        for target in self.targets:
            target.draw()


        self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()

        # decide if we should start a target
        """
        There is no limit to the number of targets that can be on the screen,
        I decided to increase the targets on the game so I modified this value
        """
        if random.randint(1, 25) == 1:
            self.create_target()

        for bullet in self.bullets:
            bullet.advance()

        # TODO: Iterate through your targets and tell them to advance
        for target in self.targets:
            target.advance()

    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        :return:
        """
        target_count = random.randint(1,100)
        """
        The new targets are created with random probabilty a standard target has more
        probability to appear on the game than a strong or safe target
        """
        if target_count < 50:
            target = standard_target()           
        elif target_count > 75:
            target = strong_target()
        else:
            target = safe_target()
            
        self.targets.append(target)           

    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                                abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        self.score += target.hit()

                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for target in self.targets:
            if not target.alive:
                self.targets.remove(target)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        :return:
        """
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for target in self.targets:
            if target.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.targets.remove(target)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # set the rifle angle in degrees
        self.rifle.angle = self._get_angle_degrees(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire!
        angle = self._get_angle_degrees(x, y)

        bullet = Bullet()
        bullet.fire(angle)

        self.bullets.append(bullet)

    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.

        Note: This could be a static method, but we haven't
        discussed them yet...
        """
        # get the angle in radians
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()