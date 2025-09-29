from circle_nom.helpers.asset_bank import AssetBank
from circle_nom.systems.logging import get_logger
import pygame

class HealthBar():
    
    # Logger reference
    _LOGGER = get_logger(name=__name__)
    
    # Game asset bank
    _AB = AssetBank()

    def __init__(self, health_bar: dict[str, pygame.Surface], screen: pygame.Surface) -> None:

        """
        Initializes the HealthBar object with images and screen.

        Args:
            health_bar (dict[str, pygame.Surface]): Dict of images for the health bar. Contains keys "INNER" and "OUTER",
            with values pygame.Surface corresponding to the inner and outer portion of the health bar.
            screen (pygame.Surface): The game screen.
        """
        self._bar_inner = health_bar["INNER"] # moving (red) bit
        self._bar_outer = health_bar["OUTER"] # static (white) bit
        self._bar_inner_og = self._bar_inner
        self._font = pygame.Font(self._AB.comic_sans_ms, 30)
        self._screen = screen
        
        # Log the Health Bar init
        self._LOGGER.info("Health bar initialized successfully.")
        
    def draw(self, text: str, size: float, max_size: float, death_size: float, coords: pygame.Vector2) -> None:
        """
        Draws the health bar on the screen.

        Args:
            text (str): The text to display next to the health bar.
            size (int): The current size of the player.
            min_size (int): The minimum size of the player.
            coords (pygame.Vector2): The position coordinates to draw the health bar.
        """
        # Text draw
        text_display = self._font.render(text, True, (255, 255, 255))
        text_x = coords.x - text_display.width + 40
        text_y = coords.y - text_display.height + 33
        self._screen.blit(text_display, (text_x, text_y))

        # Bar draw
        bar_x, bar_y = coords
        if size < death_size:
            size = death_size
        scale = [((size - death_size) / (max_size - death_size)) * 215, 32]
        self._bar_inner = pygame.transform.scale(self._bar_inner_og, scale)
        self._screen.blit(self._bar_inner, (bar_x + 52, bar_y - 3))
        self._screen.blit(self._bar_outer, (bar_x + 40, bar_y - 8))