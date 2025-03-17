import pygame
import gif_pygame
from functions.game_files_loader import dagger_sounds
from random import randint, uniform, choice

class Dagger():
    
    def __init__(self, list_daggers:list[pygame.Surface], screen:pygame.Surface):
        """
        Initialize a Dagger object with direction and other attributes.

        Args:
            list_daggers (list[pygame.Surface]): List of dagger images.
            screen (pygame.Surface): The game screen.
        """
        self._screen = screen

        self._list_daggers = list_daggers
        self._direction = None
        self._angle = None
        self._played_sound = None
        self.reset_dagger()
        
    def reset_dagger(self):
        """
        Resets the dagger's position, direction, and image.
        """
        self._coords = pygame.Vector2(float('inf'), float('inf'))
        self._created = True

        self._rand_dir = randint(0, 3)
        if self._rand_dir == 0:
            self._direction = "RIGHT"
            self._angle = 270
            self._coords.x = -100 # margin
            self._coords.y = randint(100, 620)

        elif self._rand_dir == 1:
            self._direction = "LEFT"
            self._angle = 90
            self._coords.x = self._screen.get_width() + 100 # margin
            self._coords.y = randint(100, 620)

        elif self._rand_dir == 2:
            self._direction = "UP"
            self._angle = 0
            self._coords.x = randint(100, 1180)
            self._coords.y = self._screen.get_height() + 100 # margin

        elif self._rand_dir == 3:
            self._direction = "DOWN"
            self._angle = 180
            self._coords.x = randint(100, 1180)
            self._coords.y = -100 # margin
        else:
            raise ValueError(f"rand_dir ({self._rand_dir}) is invalid!")

        # dagger image declaration based on speed
        self._speed_multiplier = uniform(1, 2)
        if self._speed_multiplier < 1.6:
            self._flame = False
            self._image:pygame.Surface = pygame.transform.rotate(self._list_daggers[0], self._angle)
        else:
            self._flame = True
            if self._direction == "RIGHT":
                self._image:gif_pygame.GIFPygame = self._list_daggers[1] # flame dagger blade faces RIGHT
            elif self._direction == "LEFT":
                self._image:gif_pygame.GIFPygame = self._list_daggers[2] # flame dagger blade faces LEFT
            elif self._direction == "UP":
                self._image:gif_pygame.GIFPygame = self._list_daggers[3] # flame dagger blade faces UP
            elif self._direction == "DOWN":
                self._image:gif_pygame.GIFPygame = self._list_daggers[4] # flame dagger blade faces DOWN
            else:
                raise ValueError(f"'{self._direction}' is not a valid direction!")
        
        # Spawn time
        self._spawn = randint(20, 40)

        # Despawn time
        self._despawn = (240 + self._spawn) / self._speed_multiplier

        # Timer for spawn/despawn
        self._timer = 0

        # Played sound flag
        self._played_sound = False

    @property
    def get_dir(self) -> str:
        """
        Returns the direction of the dagger.

        Returns:
            str: The direction of the dagger ('RIGHT', 'LEFT', 'UP', or 'DOWN').
        """
        return self._direction
    
    @property
    def coords(self) -> pygame.Vector2:
        """
        Returns the coordinates of the dagger.

        Returns:
            Vector2: Vector2 type with the dagger's coordinates.
        """
        return self._coords
    
    @property
    def flame(self) -> bool:
        """
        Returns whether the dagger has a flame effect.

        Returns:
            bool: True if the dagger has a flame effect, False otherwise.
        """
        return self._flame
    
    def grace_spawn(self, value):
        """
        Set grace spawn time for the next dagger.

        Args:
            value (int | float): The value to add to the spawn time.

        Raises:
            ValueError: If the value is not an int or float.
        """
        if type(value) == int or type(value) == float:
            self._spawn += value
            self._despawn = (240 + self._spawn) / self._speed_multiplier # update despawn
        else:
            raise ValueError("Func grace_spawn accepts int/float only!")
    
    def draw(self, dt:float):
        """
        Draw the dagger on the screen.
        
        Args:
            dt (float): Delta time, used for frame independent drawing.
        """
        if self._timer > self._spawn:
            if self._direction == "RIGHT":
                self._coords.x += 600 * self._speed_multiplier * dt
            elif self._direction == "LEFT":
                self._coords.x -= 600 * self._speed_multiplier * dt
            elif self._direction == "UP":
                self._coords.y -= 600 * self._speed_multiplier * dt
            elif self._direction == "DOWN":
                self._coords.y += 600 * self._speed_multiplier * dt

        # Reset dagger and cancel next frame draw
        if self._timer > self._despawn:
            self.reset_dagger()
            return

        # Pygame draw
        if self._flame == False and self._timer > self._spawn:
            self._screen.blit(self._image, (self._coords.x, self._coords.y) - pygame.Vector2(self._image.get_width() / 2, self._image.get_height() / 2))

        # Gif pygame draw
        if self._flame == True and self._timer > self._spawn:
            self._image.render(self._screen, (self._coords.x, self._coords.y) - pygame.Vector2(self._image.get_width() / 2, self._image.get_height() / 2))

        # Increment timer
        self._timer += 60 * dt

        # Debug
        if False:
            print(f"X:{self._coords.x:.0f} | Y: {self._coords.y:.0f} | Timer {self._timer:.0f}: spawn {self._spawn:.0f}, despawn {self._despawn:.0f}")
            pygame.draw.circle(self._screen, "red", self.coords, 10)

    def play_sound(self):
        """
        Play a random dagger sound if it hasn't been played yet.
        """
        if self._played_sound == False:
            choice(dagger_sounds).play()
            self._played_sound = True