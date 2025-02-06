from functions.game_funcs import rand_num
import pygame

class HealthBar():

    def __init__(self, hunger_bar: list[pygame.Surface], screen: pygame.Surface):

        """
        Initializes the HealthBar object with images and screen.

        Args:
            hunger_bar (list[pygame.Surface]): List of images for the hunger bar.
            screen (pygame.Surface): The game screen.
        """
        
        self._bar_inner = hunger_bar[0] # moving (red) bit
        self._bar_outer = hunger_bar[1] # static (white) bit
        self._bar_inner_og = self._bar_inner
        self._screen = screen

    def draw(self, size, max_size, death_size, coords: list):
        """
        Draws the health bar on the screen.

        Args:
            size (int): The current size of the player.
            min_size (int): The minimum size of the player.
            coords (list): The position coordinates to draw the hunger bar.
        """
        x, y = coords
        if size < death_size:
            size = death_size
        scale = [((size - death_size) / (max_size - death_size)) * 215, 32]
        self._bar_inner = pygame.transform.scale(self._bar_inner_og, scale)
        self._screen.blit(self._bar_inner, (x + 52, y - 3))
        self._screen.blit(self._bar_outer, (x + 40, y - 8))