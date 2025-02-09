import pygame
from functions.game_funcs import *
from random import randint

class Prey():
    spawn = 35
    despawn = 90

    def __init__(self, list_images:list[pygame.Surface], aura_image:pygame.Surface, screen: pygame.Surface):

        """
        Takes with paths to images for random selection, aura image and pygame display.
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

        # Initial prey atributes
        self.reset_prey()

    def draw(self, increment:bool=True):
        """
        Draw prey on the screen.
        """
        # Reset prey atributes and cancel frame draw
        if self._counter >= Prey.despawn:
            self.reset_prey()
            return

        # Frame draw
        if self._counter >= Prey.spawn:

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
                self._aura_angle = (self._aura_angle % 360) - 1

                # Rotate prey once and display
                rotated_prey = rot_center(self._image, self._prey_angle, self._coords)
                self._screen.blit(rotated_prey[0], rotated_prey[1])

            else:
                # Rotate prey once and display
                rotated_prey = rot_center(self._image, self._prey_angle, self._coords)
                self._screen.blit(rotated_prey[0], rotated_prey[1])

        if increment:
            self._counter += 1
    
    def reset_prey(self):

        # New image
        self._image_index:int = rand_num(len(self._list_images))
        self._image = self._list_images[self._image_index]

        # New aura flag - apply only to sandwich, which is on index 0
        if self._image_index == 0:
            self._aura_flag = True
        else:
            self._aura_flag = False

        # New prey angle
        self._prey_angle = rand_num(360)

        # Reset counter
        self._counter = 0

        # Reset coords - done to prevent eating non-drawn prey:
        self._coords = float('inf'), float('inf')
        self._generated_coords = False

    @property
    def aura(self):
        return self._aura_flag
    
    @property
    def coords(self):
        return self._coords
    
    @property
    def counter(self):
        return self._counter
    
    @counter.setter
    def counter(self, value):
        self._counter = value
