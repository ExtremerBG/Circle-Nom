import pygame
from functions.game_funcs import *

class Prey():

    def __init__(self, list_images, easter_mode: bool, screen: pygame.display):

        """
        Takes with paths to images for random selection (index 0 is gif_pygame), \n
        bool for easter mode and a pygame display.
        """

        self._created = True
        self._counter = 0

        self._image_index = rand_num(len(list_images))
        self._image = list_images[self._image_index]

        self._coords = rand_screen_pos()
        self._angle = rand_num(360)
        self._easter = easter_mode
        self._screen = screen

    def draw(self):
        """
        Draw prey on the screen.
        """
        if self._image_index == 0 and self._easter == False:
            self._image.render(self._screen, self._coords- pygame.Vector2(self._image.get_width() / 2, self._image.get_height() / 2))
        else:
            self._screen.blit(image_rotate(self._image, self._angle), self._coords - pygame.Vector2(self._image.get_width() / 2, self._image.get_height() / 2))

    def coords_reset(self):
        """
        Sets prey coordinates (X, Y) to infinite.
        """
        self._coords = float('inf'), float('inf')

    @property
    def index(self):
        """
        Returns prey image index.
        """
        return self._image_index
    
    @property
    def coords(self):
        """
        Returns prey coordinates (X, Y).
        """
        return self._coords
    
    @property
    def created(self):
        """
        Returns prey created state.
        """
        return self._created
    
    @property
    def counter(self):
        """
        Returns prey counter.
        """
        return self._counter
    
    @created.setter
    def created(self, value:bool):
        if type(value) != bool:
            raise ValueError("Created accepts bool only!")
        self._created = value

    @counter.setter
    def counter(self, value: float):
        if value < 0:
            raise ValueError("Counter cannot be below 0!")
        self._counter = value