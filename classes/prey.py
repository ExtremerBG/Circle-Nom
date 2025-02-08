import pygame
from functions.game_funcs import *

class Prey():
    spawn = 35
    despawn = 90

    def __init__(self, list_images:list[pygame.Surface], screen: pygame.Surface):

        """
        Takes with paths to images for random selection (index 0 is gif_pygame) and pygame display.
        """
        # List of all prey images
        # CONTAINS GIF_PYGAME AND PYGAME
        self._list_images = list_images

        # Pygame screen
        self._screen = screen

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
            
            try: # gif pygame render
                self._image.render(self._screen, self._coords- pygame.Vector2(self._image.get_width() / 2, self._image.get_height() / 2))
            except AttributeError: # pygame render
                self._screen.blit(image_rotate(self._image, self._angle), self._coords - pygame.Vector2(self._image.get_width() / 2, self._image.get_height() / 2))
    
        if increment:
            self._counter += 1
    
    def reset_prey(self):

        # New image
        self._image_index:int = rand_num(len(self._list_images))
        self._image = self._list_images[self._image_index]

        # New angle
        self._angle = rand_num(360)

        # Reset counter
        self._counter = 0

        # Reset coords - done to prevent eating non-drawn prey:
        self._coords = float('inf'), float('inf')
        self._generated_coords = False

    @property
    def index(self):
        return self._image_index
    
    @property
    def coords(self):
        return self._coords
    
    @property
    def counter(self):
        return self._counter
    
    @counter.setter
    def counter(self, value):
        self._counter = value
