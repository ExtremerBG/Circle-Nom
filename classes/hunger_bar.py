from functions.game_funcs import rand_num
import pygame

class HungerBar():

    def __init__(self, hunger_bar: list, screen: pygame.display):

        """
        Takes hunger_bar pygame image list, consiting of bar_inner (the moving bit), \n
        bar outer (the static white bit) and pygame display.
        """
        
        self._bar_inner = hunger_bar[0]
        self._bar_outer = hunger_bar[1]
        self._bar_inner_og = self._bar_inner
        self._screen = screen

    def draw(self, size, min_size, coords: list):
        """
        Draw Hunger bar on the screen. Takes current size, minimum size and position coordinates.
        """
        x, y = coords
        scale = [(size - min_size) * 2.8, 30]
        self._bar_inner = pygame.transform.scale(self._bar_inner_og, scale)
        self._screen.blit(self._bar_inner, (x + 50, y - 3))
        self._screen.blit(self._bar_outer, (x + 40, y - 8))