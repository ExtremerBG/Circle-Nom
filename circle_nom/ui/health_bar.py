from circle_nom.helpers.asset_bank import COMIC_SANS_MS
import pygame

class HealthBar():

    def __init__(self, health_bar: list[pygame.Surface], screen: pygame.Surface):

        """
        Initializes the HealthBar object with images and screen.

        Args:
            health_bar (list[pygame.Surface]): List of images for the health bar.
            screen (pygame.Surface): The game screen.
        """
        self._bar_inner = health_bar["INNER"] # moving (red) bit
        self._bar_outer = health_bar["OUTER"] # static (white) bit
        self._bar_inner_og = self._bar_inner
        self._font = pygame.Font(COMIC_SANS_MS, 30)
        self._screen = screen

    def draw(self, text: str, size: float, max_size: float, death_size: float, coords: list):
        """
        Draws the health bar on the screen.

        Args:
            text (str): The text to display next to the health bar.
            size (int): The current size of the player.
            min_size (int): The minimum size of the player.
            coords (list): The position coordinates to draw the hunger bar.
        """
        # Text draw
        text_display = self._font.render(text, True, (255, 255, 255))
        text_x = coords[0] - text_display.get_width() + 40
        text_y = coords[1] - text_display.get_height() + 33
        self._screen.blit(text_display, (text_x, text_y))

        # Bar draw
        bar_x, bar_y = coords
        if size < death_size:
            size = death_size
        scale = [((size - death_size) / (max_size - death_size)) * 215, 32]
        self._bar_inner = pygame.transform.scale(self._bar_inner_og, scale)
        self._screen.blit(self._bar_inner, (bar_x + 52, bar_y - 3))
        self._screen.blit(self._bar_outer, (bar_x + 40, bar_y - 8))