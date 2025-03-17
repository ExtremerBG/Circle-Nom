from functions.game_funcs import rot_center, rand_screen_pos
from random import randint
import pygame

class Prey():
    
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

    def draw(self, dt:float):
        """
        Draw prey on the screen.

        Args:
            dt (float): Delta time, used for frame independent drawing.
        """
        # Reset prey attributes and cancel frame draw
        if self._counter >= Prey.DESPAWN:
            self.reset_prey()
            return

        # Frame draw
        if self._counter >= Prey.SPAWN:

            # Check if coords are generated
            if self._generated_coords == False:
                # Generate actual coords only when counter > spawn
                self._coords = rand_screen_pos()
                self._generated_coords = True

            # Check if prey is aura-d
            if self._aura_flag == True:
                # Rotate aura constantly and display
                rotated_aura = rot_center(self._aura_image, self._aura_angle, self._coords)
                self._screen.blit(rotated_aura[0], rotated_aura[1])
                self._aura_angle = (self._aura_angle % 360) - 60 * dt

                # Rotate prey once and display
                rotated_prey = rot_center(self._image, self._prey_angle, self._coords)
                self._screen.blit(rotated_prey[0], rotated_prey[1])

            else:
                # Rotate prey once and display
                rotated_prey = rot_center(self._image, self._prey_angle, self._coords)
                self._screen.blit(rotated_prey[0], rotated_prey[1])

        # Increment counter
        self._counter += 60 * dt
    
    def reset_prey(self):
        """
        Resets the prey's attributes including image, aura flag, angle, counter, and coordinates.
        """
        # New image
        self._image_index:int = randint(0, len(self._list_images) - 1)
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

        # Reset coords - done to prevent eating non-drawn prey:
        self._coords = float('inf'), float('inf')
        self._generated_coords = False

    @property
    def aura(self):
        """
        Returns whether the prey has an aura effect.

        Returns:
            bool: True if the prey has an aura effect, False otherwise.
        """
        return self._aura_flag
    
    @property
    def coords(self):
        """
        Returns the coordinates of the prey.

        Returns:
            tuple: The x and y coordinates of the prey.
        """
        return self._coords
    
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
