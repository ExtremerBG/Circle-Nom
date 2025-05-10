from circle_nom.helpers.other_utils import rot_center, rand_screen_pos
from random import randint
import pygame

class Prey():
    
    ANIM_DUR = 20
    SPAWN = 35
    DESPAWN = 90
    
    def __init__(self, list_images:list[pygame.Surface], aura_image:pygame.Surface, screen: pygame.Surface):
        """
        Initializes the Prey object with images, aura image, and screen.

        Args:
            list_images (list[pygame.Surface]): List of prey images.
            aura_image (pygame.Surface): The aura image.
            screen (pygame.Surface): The game screen.
        """
        # List of all prey images
        self._list_images = list_images

        # Aura image
        self._aura_image = aura_image

        # Pygame screen
        self._screen = screen

        # Aura angle
        self._aura_angle = 0
        
        # Counter for spawn/despawn
        self._counter = 0

        # Initial prey attributes
        self.reset_prey()

    @property
    def aura(self):
        """
        Returns whether the prey has an aura effect.

        Returns:
            bool: True if the prey has an aura effect, False otherwise.
        """
        return self._aura_flag
    
    @property
    def position(self):
        """
        Returns the position coordinates of the prey. If none returns Vector2('inf', 'inf').

        Returns:
            Vector2: The x and y coordinates.
        """
        return self._position if self._position else pygame.Vector2(float('inf'), float('inf'))

    
    @property
    def eatable(self):
        """
        Returns the prey's eatable bool. True if prey is not in animation, false otherwise.
        
        Returns:
            bool: The eatable bool.
        """
        return self._eatable
    
    @property
    def counter(self):
        """
        Returns the counter for the prey's spawn/despawn.

        Returns:
            int: The counter value.
        """
        return self._counter
    
    @counter.setter
    def counter(self, value):
        """
        Sets the counter for the prey's spawn/despawn.

        Args:
            value (int): The new counter value.
        """
        self._counter = value
        
    def _animate(self, dt: float, duration: int, reverse: bool):
        """
        Handles the animation of the prey (scaling and rotation).

        Args:
            dt (float): Delta time for frame-independent animation.
            duration (int): Duration of the animation.
            reverse (bool): Whether the animation is in reverse (despawn).
        """
        # Normalize the duration influence
        reference_duration = 40  # or your chosen baseline
        factor = duration / reference_duration

        # Calculate scale_vect (0 to 1) based on the counter
        scale_vect = (self._counter - (Prey.SPAWN - duration if not reverse else Prey.DESPAWN)) / duration
        scale_vect = max(0, min(1, scale_vect))  # Clamp between 0 and 1
        rotation_vect = 1 # default clockwise rotation


        # Reverse for despawn
        if reverse:
            scale_vect = 1 - scale_vect
            rotation_vect = -1 # counterclockwise

        # Update scale and angle based on scale_vect
        self._scale = int(70 * scale_vect)  # Scale from 0 to 70
        self._prey_angle = (self._prey_angle % 360) - (400 / factor) * rotation_vect * dt

        # Prevent scale from being negative
        if self._scale < 0: self._scale = 0
        
        # Set eatable to false since prey is in animation
        self._eatable = False

        # Transform the aura image
        if self._aura_flag:
            aura_scale = int(190 * scale_vect)  # Scale the aura based on scale_vect
            aura = pygame.transform.smoothscale(self._aura_image, (aura_scale, aura_scale))
            rotated_aura = rot_center(aura, self._aura_angle, self._position)
            self._screen.blit(rotated_aura[0], rotated_aura[1])
            self._aura_angle = (self._aura_angle % 360) - 60 * dt

        # Transform the prey image
        prey = pygame.transform.smoothscale(self._image, (self._scale, self._scale))
        rotated_prey = rot_center(prey, self._prey_angle, self._position)
        self._screen.blit(rotated_prey[0], rotated_prey[1])
            
    def draw(self, dt: float):
        """
        Draw prey on the screen.

        Args:
            dt (float): Delta time, used for frame-independent drawing.
        """
        # Reset prey attributes and cancel frame draw
        if self._counter >= Prey.DESPAWN + self.ANIM_DUR:
            self.reset_prey()
            return

        # Skip drawing if the spawn animation hasn't started and increment counter
        if self._counter < Prey.SPAWN - Prey.ANIM_DUR:
            self._counter += 60 * dt
            return

        # Set valid coordinates when spawn animation starts
        if self._position is None:
            self._position = rand_screen_pos()

        # Spawn Animation
        if Prey.SPAWN - Prey.ANIM_DUR <= self._counter < Prey.SPAWN:
            self._animate(dt, Prey.ANIM_DUR, False)

        # Despawn Animation
        elif Prey.DESPAWN <= self._counter < Prey.DESPAWN + Prey.ANIM_DUR:
            self._animate(dt, Prey.ANIM_DUR, True)

        # Normal
        else:
            # Normal Frame draw
            self._eatable = True

            # Check if prey is aura-d
            if self._aura_flag:
                # Rotate aura constantly and display
                rotated_aura = rot_center(self._aura_image, self._aura_angle, self._position)
                self._screen.blit(rotated_aura[0], rotated_aura[1])
                self._aura_angle = (self._aura_angle % 360) - 60 * dt

            # Rotate prey once and display
            rotated_prey = rot_center(self._image, self._prey_angle, self._position)
            self._screen.blit(rotated_prey[0], rotated_prey[1])

        # Increment counter
        self._counter += 60 * dt
        
    def reset_prey(self):
        """
        Resets the prey's attributes including image, aura flag, angle, counter, and coordinates.
        """
        # New image
        self._image_index = randint(0, len(self._list_images) - 1)
        self._image = self._list_images[self._image_index]

        # New aura flag - apply only to sandwich, which is on index 0
        if self._image_index == 0:
            self._aura_flag = True
        else:
            self._aura_flag = False

        # New prey angle
        self._prey_angle = randint(0, 360)

        # Reset counter
        self._counter = 0

        # Set invalid coordinates to prevent premature drawing
        self._position = None
        self._eatable = False

        # Reset scale to 0 to prevent flashing
        self._scale = 0
