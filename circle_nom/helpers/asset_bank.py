from circle_nom.systems.asset_loader import AssetLoader
from circle_nom.systems.logging import get_logger
import pygame

class AssetBank:
    """
    Initializes the AssetBank, containing all assets of the game, which are READ-ONLY. \n
    Use the property methods of AssetBank to access them.
    """
    # Asset loader
    _AL = AssetLoader()
    
    # Loggger reference
    _LOGGER = get_logger(name=__name__)
    
    # Assets
    _ICON = _AL.load_image('assets/images/icon/icon.ico')
    _PLAYER_EAT_SOUNDS = _AL.load_sounds(_AL.traverse_folder('assets/sounds/effects/player/eat/'), 6)
    _GAME_THEMES = _AL.load_playlist(_AL.traverse_folder('assets/sounds/themes/in_game/'), 16)
    _PLAYER_IMAGE = _AL.load_image('assets/images/player/alive/player_alive_image.png')
    _PLAYER_IMAGE_DEAD = _AL.load_image('assets/images/player/dead/player_dead_image.png')
    _PLAYER_EAT_SEQUENCE = _AL.load_images(_AL.traverse_folder('assets/images/player/eat_sequence/'), 10)
    _PLAYER_ACCESSORIES = (
        # const XY offset from player topleft, pygame image pairs
        (pygame.Vector2(x=90, y=70), _AL.load_image('assets/images/player/accessories/glasses.png')),
        (pygame.Vector2(x=90, y=3), _AL.load_image('assets/images/player/accessories/fedora.png')),
        (pygame.Vector2(x=90, y=-8), _AL.load_image('assets/images/player/accessories/propeller_hat.png')),
        (pygame.Vector2(x=90, y=70), _AL.load_image('assets/images/player/accessories/3d_glasses.png')),
        (pygame.Vector2(x=88, y=100), _AL.load_image('assets/images/player/accessories/blonde_wig.png')),
        (pygame.Vector2(x=110, y=88), _AL.load_image('assets/images/player/accessories/moustache_n_monacle.png')),
    )
    _PREY_IMAGES = _AL.load_images(_AL.traverse_folder('assets/images/prey/alive/'), 11)
    _PREY_AURA = _AL.load_image('assets/images/prey/aura/prey_aura_image.png')
    _BACKGROUND_IMAGES = _AL.load_images(_AL.traverse_folder('assets/images/backgrounds/'), 10)
    _HEALTH_BAR = {
        "OUTER": _AL.load_image('assets/images/health_bar/bar_outer_image.png'),
        "INNER": _AL.load_image('assets/images/health_bar/bar_inner_image.png')
    }
    _DAGGER_IMAGES = _AL.load_images(_AL.traverse_folder('assets/images/dagger/'), 7)
    _DAGGER_SOUNDS = _AL.load_sounds(_AL.traverse_folder('assets/sounds/effects/dagger/fly'), 5)
    _PLAYER_HIT_SOUNDS = _AL.load_sounds(_AL.traverse_folder('assets/sounds/effects/player/hit/'), 5)
    _PLAYER_AURA = _AL.load_image('assets/images/player/aura/player_aura_image.png')
    _MENU_THEMES = _AL.load_playlist(_AL.traverse_folder('assets/sounds/themes/menu/'), 2)
    _MENU_CLICK_SOUNDS = {
        "UPDOWN": _AL.load_sound('assets/sounds/effects/menu/menu_click_up_down.ogg'),
        "LEFTRIGHT": _AL.load_sound('assets/sounds/effects/menu/menu_click_left_right.ogg'),
        "UNKNOWN": _AL.load_sound('assets/sounds/effects/menu/menu_click_unknown.ogg')
    }
    _DASH_IMAGES = {
        "AVAIL": _AL.load_image('assets/images/player/dash/dash_available_image.png'),
        "UNAVAIL": _AL.load_image('assets/images/player/dash/dash_unavailable_image.png')
    }
    _DASH_SOUNDS = _AL.load_sounds(_AL.traverse_folder('assets/sounds/effects/player/dash/'), 4)
    _FLAME_SEQUENCE = _AL.load_images(_AL.traverse_folder('assets/images/flame_sequence'), 6)
    _CURSOR = _AL.load_image('assets/images/cursor/cursor_image.png')
    _COMIC_SANS_MS = _AL.resource_path("assets/fonts/comic_sans_ms.ttf")
    
    # Check if all assets are loaded and log it - current file target count is 102
    _TOTAL_ASSETS_TRGT = 101
    if _AL.total_assets_loaded == _TOTAL_ASSETS_TRGT:
        _LOGGER.info(f"All {_TOTAL_ASSETS_TRGT} assets successfully loaded.")
    elif _AL.total_assets_loaded < _TOTAL_ASSETS_TRGT:
        _LOGGER.warning(f"{_TOTAL_ASSETS_TRGT - _AL.total_assets_loaded} assets could not be loaded, out of {_TOTAL_ASSETS_TRGT}.")
    else:
        _LOGGER.warning(f"Loaded {_AL.total_assets_loaded} assets, {_AL.total_assets_loaded - _TOTAL_ASSETS_TRGT} more than the target of {_TOTAL_ASSETS_TRGT}.")
        
    # Asset properties
    @property
    def icon(self) -> pygame.Surface:
        """Game icon (pygame.Surface). Used for window icon."""
        return self._ICON

    @property
    def player_eat_sounds(self) -> tuple[pygame.Sound]:
        """Player eating sounds."""
        return self._PLAYER_EAT_SOUNDS

    @property
    def game_themes(self) -> tuple[tuple[str, str], ...]:
        """Playlist of in-game themes as tuples containing the path of the theme and its name."""
        return self._GAME_THEMES

    @property
    def player_image(self) -> pygame.Surface:
        """Player image when alive."""
        return self._PLAYER_IMAGE

    @property
    def player_image_dead(self) -> pygame.Surface:
        """Player image when dead."""
        return self._PLAYER_IMAGE_DEAD

    @property
    def player_eat_sequence(self) -> tuple[pygame.Surface, ...]:
        """Sequence of images for the player's eating animation."""
        return self._PLAYER_EAT_SEQUENCE

    @property
    def player_accessories(self) -> tuple[tuple[pygame.Vector2, pygame.Surface], ...]:
        """Player accessories as tuples containing an offset used for allignment with the player and the accessory image"""
        return self._PLAYER_ACCESSORIES

    @property
    def prey_images(self) -> tuple[pygame.Surface, ...]:
        """Prey images."""
        return self._PREY_IMAGES

    @property
    def prey_aura(self) -> pygame.Surface:
        """Prey aura image."""
        return self._PREY_AURA

    @property
    def background_images(self) -> tuple[pygame.Surface, ...]:
        """Background images."""
        return self._BACKGROUND_IMAGES

    @property
    def health_bar(self) -> dict[str, pygame.Surface]:
        """Dictionary with health bar images, keys: 'OUTER' and 'INNER'."""
        return self._HEALTH_BAR

    @property
    def dagger_images(self) -> tuple[pygame.Surface, ...]:
        """Dagger images."""
        return self._DAGGER_IMAGES

    @property
    def dagger_sounds(self) -> tuple[pygame.Sound, ...]:
        """Daggers flying sounds."""
        return self._DAGGER_SOUNDS

    @property
    def player_hit_sounds(self) -> tuple[pygame.Sound, ...]:
        """Player sounds when hit by a dagger"""
        return self._PLAYER_HIT_SOUNDS

    @property
    def player_aura(self) -> pygame.Surface:
        """Player aura image."""
        return self._PLAYER_AURA

    @property
    def menu_themes(self) -> tuple[tuple[str, str], ...]:
        """Playlist of menu themes as tuples containing the path of the theme and its name."""
        return self._MENU_THEMES

    @property
    def menu_click_sounds(self) -> dict[str, pygame.Sound]:
        """Dictionary of menu click sounds. Keys: 'UPDOWN', 'LEFTRIGHT', 'UNKNOWN'."""
        return self._MENU_CLICK_SOUNDS

    @property
    def dash_images(self) -> dict[str, pygame.Surface]:
        """Images representing dash availability. Keys: 'AVAIL', 'UNAVAIL'."""
        return self._DASH_IMAGES

    @property
    def dash_sounds(self) -> tuple[pygame.Sound]:
        """Player sounds when dashing."""
        return self._DASH_SOUNDS

    @property
    def flame_sequence(self) -> tuple[pygame.Surface]:
        """Sequence of images for the dagger's flame animation."""
        return self._FLAME_SEQUENCE

    @property
    def cursor(self) -> pygame.Surface:
        """Image for the Pygame cursor."""
        return self._CURSOR

    @property
    def comic_sans_ms(self) -> str:
        """Path to the Comic Sans MS font."""
        return self._COMIC_SANS_MS