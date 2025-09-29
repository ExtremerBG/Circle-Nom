import circle_nom.helpers.player_utils as player_utils
from circle_nom.helpers.asset_bank import AssetBank
from circle_nom.systems.logging import get_logger
from circle_nom.systems.timer import Timer
from random import choice
import numpy as np
import pygame

class Player():
    
    # Starting values
    STARTING_SPEED = 25
    STARTING_SIZE = 60
    
    # Dash cooldown and duration in seconds
    DASH_CD =  0.6
    DASH_DUR = 0.14

    # Speed limiters - dashing overrides max speed
    MIN_SPEED = 15
    MAX_SPEED = 30

    # Size limiters
    MIN_SIZE = 30
    MAX_SIZE = 120
    
    # Texts for drawing
    EAT_TEXTS = "Nom!", "Nom", "nom!", "nom"
    HURT_TEXTS = "Ow!", "ow", "Ouch!", "ouch"
    
    # Texts & associated animations durations in seconds
    EAT_DUR = 0.3
    HURT_DUR = 0.3
    
    # Logger reference
    _LOGGER = get_logger(name=__name__)
    
    # Game asset bank
    _AB = AssetBank()
    
    def __init__(self, screen:pygame.Surface, game_timer: Timer, easter_mode: bool, 
                 image_alive: pygame.Surface, image_dead: pygame.Surface, 
                 eat_sequence: list[pygame.Surface] | None, 
                 accessory: tuple[pygame.Vector2, pygame.Surface] | None) -> None:
        """
        Initializes the Player object with images, easter mode, and screen.
        
        Args:
            screen (pygame.Surface): The game screen. Used in the different draw methods.
            game_timer (Timer): The game timer. Used for different cooldowns.
            easter_mode (bool): Flag for easter mode. Changes blitting methods to better fit other images.
            image_alive (pygame.Surface): The player's alive image.
            image_dead (pygame.Surface): The player's dead image.
            eat_sequence (list(pygame.Surface) | None): The player's eat sequence animation.
            player_accessory (tuple(pygame.Vector2, pygame.Surface) | None): The player's accessory data pair.
        """
        
        # Objects from engine
        self._screen = screen
        self._game_timer = game_timer
        
        # Easter mode flag from engine
        self._easter = easter_mode
        
        # Assets
        self._image_alive = image_alive
        self._image_hit = self._modify_hit()
        self._image_dead = image_dead
        self._eat_sequence = eat_sequence
        self._accessory = accessory
        self._text_font = pygame.Font(self._AB.comic_sans_ms, 30)
        
        # Below are the starting attributes
        # Core size, scale, position and speed of the player
        self._size = Player.STARTING_SIZE
        self._scale = [self._size * 3, self._size * 3]
        self._position = pygame.Vector2(640, 140)
        self._speed = Player.STARTING_SPEED
        
        # Dash attributes
        self._dash_on = False
        self._speed_before_dash = Player.STARTING_SPEED
        self._last_dash_timestamp = -1
        
        # Adjust eat position and tolerance based on the easter flag
        # eat_pos is the center, eat_tol is the radius of the eat circle
        if self._easter:
            self._eat_pos = self._position
            self._eat_tol = self._size * 1.25
        else:
            self._eat_pos = pygame.Vector2(self._position.x, self._position.y - self._image_alive.height * - 0.3)
            self._eat_tol = self._size * 0.8
        
        # Hurt attributes - simillar to eat
        self._hurt_pos = self._position
        self._hurt_tol = self._size * 1.25
        
        # Timestamps for eat/hurt draws & animations
        # using -1 since 0 shows them for a few frames at beggining of game
        self._last_eat_timestamp = -1
        self._last_hurt_timestamp = -1
        
        # Texts to display as part of the eat/hurt animations
        self._eat_text = choice(Player.EAT_TEXTS)
        self._hurt_text = choice(Player.HURT_TEXTS)
        
        # Initial player points
        self._points = 0
        
        # Log the Player init
        self._LOGGER.info("Player model initialized successfully.")
        
    @property
    def eat_pos(self) -> pygame.Vector2:
        """
        Returns the player's eat position.
        
        Returns:
            pygame.Vector2: The eat position of the player.
        """
        return self._eat_pos

    @property
    def eat_tol(self) -> float:
        """
        Returns the player's eat tolerance.
        The eat tolerance determines the range within which the player can eat prey.
        
        Returns:
            float: The eat tolerance of the player.
        """
        return self._eat_tol
    
    @property
    def hit_pos(self) -> pygame.Vector2:
        """
        Returns the player's hit position.
        
        Returns:
            pygame.Vector2: The hit position of the player.
        """
        return self._hurt_pos
    
    @property
    def hit_tol(self) -> float:
        """
        Returns the player's hit tolerance.
        
        Returns:
            float: The hit tolerance of the player.
        """
        return self._hurt_tol
    
    @property
    def collision_tol(self) -> float:
        """
        Returns the player's collision tolerance.
        
        Returns:
            float: The collision tolerance of the player.
        """
        return self._collision_tol
    
    @property
    def size(self) -> float:
        """
        Returns the player's size.
        
        Returns:
            float: The size of the player.
        """
        return self._size
    
    @property
    def speed(self) -> float:
        """
        Returns the player's speed.
        
        Returns:
            float: The speed of the player.
        """
        return self._speed
    
    @property
    def speed_before_dash(self) -> float:
        """
        Returns the player's last speed before dash.
        
        Returns:
            float: The last speed of the player.
        """
        return self._speed_before_dash
    
    @property
    def dash_available(self) -> bool:
        """
        Returns if the player's dash is available.
        
        Returns:
            bool: True if internal dash CD is <= 0, false otherwise.
        """
        return (self._game_timer.get_time() - self._last_dash_timestamp) >= Player.DASH_CD
    
    @property
    def position(self) -> pygame.Vector2:
        """
        Returns the player's position.
        
        Returns:
            pygame.Vector2: The position of the player.
        """
        return self._position
    
    @property
    def points(self) -> int:
        """
        Returns the player's points.
        
        Returns:
            int: The points of the player.
        """
        return self._points
    
    @property
    def can_eat(self) -> bool:
        """
        Returns the player's can_eat boolean.
        
        Returns:
            bool: The can_eat boolean.
        """
        return self._game_timer.get_time() - self._last_eat_timestamp > Player.EAT_DUR
    
    @size.setter
    def size(self, value: float) -> None:
        """
        Sets the player's size and updates scale. Limited by Player's min and max size consts.
        
        Args:
            value (float): The new size of the player.
        """
        if value < Player.MIN_SIZE: self._size = Player.MIN_SIZE
        elif value > Player.MAX_SIZE: self._size = Player.MAX_SIZE
        else: self._size = value            
        self._scale = [self._size * 3, self._size * 3]

    @speed.setter
    def speed(self, value:float) -> None:
        """
        Sets the player's speed. Has min/max values, check Player class.
        
        Args:
            value (float): The new speed of the player.
        """
        self._speed = value
        if self._speed < Player.MIN_SPEED: self._speed = Player.MIN_SPEED
        if not self._dash_on: # Max speed cap only if dash is not on
            if self._speed > Player.MAX_SPEED: self._speed = Player.MAX_SPEED 
            
    @speed_before_dash.setter
    def speed_before_dash(self, value:float) -> None:
        """
        Set the player's last speed before a dash.
        
        Args:
            value (float): The new last speed of the player.
        """
        self._speed_before_dash = value
        
    @position.setter
    def position(self, value: pygame.Vector2) -> None:
        """
        Sets the player's position.
        
        Args:
            value (pygame.Vector2): The new position of the player.
        """
        # if type(value) != pygame.Vector2:
        #     raise ValueError("Position coordinates accepts pygame.Vector2 only!")
        self._position = value

    @eat_tol.setter
    def eat_tol(self, value:float) -> None:
        """
        Sets the player's eat tolerance.
        
        Args:
            value (float): The new eat tolerance of the player.
        """
        # if value < 0:
        #     raise ValueError("Eat tolerance cannot be less than 0!")
        self._eat_tol = value

    @points.setter
    def points(self, value:int) -> None:
        """
        Sets the player's points.
        
        Args:
            value (int): The new points of the player.
        """
        # if type(value) != int:
        #     raise ValueError("Points accepts int only!")
        # if value < 0:
        #     raise ValueError("Points cannot be less than 0!")  
        self._points = value
        
    @classmethod
    def set_dash_cd(cls, cd: int | float) -> None:
        """
        Set the dash cooldown of the player.
        
        Args:
            cd (int|float): The new dash cooldown in seconds.
        """
        cls.DASH_CD = cd
        
    def _modify_hit(self) -> pygame.Surface:
        """
        Modifies the player's image to be more reddish. Used in the init.
        """
        # Method 1 for easter mode. Fills every pixel with red.
        if self._easter:
            # Create a copy of the original image
            reddish_image = self._image_alive.copy()

            # Fill the image with a red color, using the BLEND_RGBA_ADD flag to add the red component
            reddish_image.fill((200, 0, 0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        # Method 2 for non-easter mode. Modifies yellow pixels to red.
        else:
            # Create a copy of the original image
            reddish_image = self._image_alive.copy()

            # Convert the surface to a NumPy array
            pixel_array = pygame.surfarray.pixels3d(reddish_image)

            # Define the range for yellow color
            yellow_min = np.array([200, 200, 0])
            yellow_max = np.array([255, 255, 100])

            # Create a mask for yellow pixels
            mask = np.all((pixel_array >= yellow_min) & (pixel_array <= yellow_max), axis=-1)

            # Increase the red component and decrease the green and blue components for yellow pixels
            pixel_array[..., 0][mask] = np.minimum(255, pixel_array[..., 0][mask] + 240) # R
            pixel_array[..., 1][mask] = np.maximum(0, pixel_array[..., 1][mask] + 60)   # G
            pixel_array[..., 2][mask] = np.maximum(0, pixel_array[..., 2][mask] - 0)   # B

            # Unlock the surface
            del pixel_array
            
        return reddish_image
        
    def _draw_text(self, text: str, image: pygame.Surface) -> None:
        """
        Draws the specified text on the screen.
        
        Args:
            text (str): The text to draw.
            image (pygame.Surface): The image to offset the text from.
        """
        rendered_text = self._text_font.render(f"{text}", True, (255, 255, 255))
        text_rect = rendered_text.get_rect(center=(self._position.x, self._position.y - image.height / 2 - self._size * 0.8))
        self._screen.blit(rendered_text, text_rect)

    def _new_texts(self) -> None:
        """
        Selects new strings for _eat_text and _hurt_text.
        """
        self._eat_text = choice(Player.EAT_TEXTS)
        self._hurt_text = choice(Player.HURT_TEXTS)
        
    def _draw_accessory(self) -> None:
        """
        Draw player's accessory if it exists.
        """
        if self._accessory:
            # Calculate scale factor relative to menu player size (180)
            scale_factor = self._scale[0] / 180
            # Scale the offset
            scaled_offset = self._accessory[0] * scale_factor
            # Scale the accessory image
            accessory_size = (
                (self._accessory[1].width * scale_factor),
                (self._accessory[1].height * scale_factor)
            )
            scaled_image = pygame.transform.smoothscale(self._accessory[1], accessory_size)
            # Calculate the top-left of the player image
            player_topleft = self._position - pygame.Vector2(self._scale[0] / 2, self._scale[1] / 2)
            # Blit at the correct position
            self._screen.blit(
                scaled_image,
                player_topleft + scaled_offset - pygame.Vector2(scaled_image.width / 2, scaled_image.height / 2)
            )
            
    def reset_eat_attributes(self) -> None:
        """
        Set the eat timestamp at current game timer time and choose a new eat text. \n
        Must be used only once when the player eats a prey.
        """
        self._last_eat_timestamp = self._game_timer.get_time()
        self._eat_text = choice(Player.EAT_TEXTS)
        
    def reset_hurt_attributes(self) -> None:
        """
        Set the hurt timestamp at current game timer time and choose a new hurt text. \n
        Must be used only once when the player gets hurt.
        """
        self._last_hurt_timestamp = self._game_timer.get_time()
        self._eat_text = choice(Player.HURT_TEXTS)
        
    def dash(self) -> None:
        """
        Activates the dash if the cooldown is ready.
        """
        if self.dash_available:
            self._speed_before_dash = self._speed
            self._speed += player_utils.get_dash_speed(self)
            self._last_dash_timestamp = self._game_timer.get_time()
            self._dash_on = True
            choice(self._AB.dash_sounds).play()
            log_str = (
                f"Player dashed at time {self._game_timer.get_time():.2f} " 
                f"with init speed {self._speed_before_dash:.2f}, current speed {self._speed:.2f}"
            )
            self._LOGGER.info(log_str)
            
    def draw(self, dt: float) -> None:
        """
        Draws the player on the screen and handles dash mechanics.
        
        Args:
            dt (float): Delta time in seconds since the last frame. Ensures frame-rate independent animation.
        """
        # Eat animation draw
        if self._game_timer.get_time() - self._last_eat_timestamp < Player.EAT_DUR and self._eat_sequence:
            player_image = self._eat_sequence[int(self._game_timer.get_time() / 0.12 % len(self._eat_sequence))]
            player_image = pygame.transform.smoothscale(player_image, self._scale)
            self._screen.blit(player_image, self._position - pygame.Vector2(player_image.width / 2, player_image.height / 2))
            
        # Hurt draw
        elif self._game_timer.get_time() - self._last_hurt_timestamp < Player.HURT_DUR:
            player_image = pygame.transform.smoothscale(self._image_hit, self._scale)
            self._screen.blit(player_image, self._position - pygame.Vector2(player_image.width / 2, player_image.height / 2))
            
        # Normal draw
        else:
            # Player resize and draw
            player_image = pygame.transform.smoothscale(self._image_alive, self._scale)
            self._screen.blit(player_image, self._position - pygame.Vector2(player_image.width / 2, player_image.height / 2))
            
        # Update eat and hit positions based on the image from draw
        if not self._easter:
            self._eat_pos = pygame.Vector2(self._position.x, self._position.y - player_image.height * -0.3)
            self._eat_tol = self._size * 0.8
        else:
            self._eat_pos = self._position
            self._eat_tol = self._size * 1.25
            
        # Draw player's accessory before text
        self._draw_accessory()
            
        # Eat text draw
        if self._game_timer.get_time() - self._last_eat_timestamp < Player.EAT_DUR:
            self._draw_text(self._eat_text, player_image)
        
        # Hurt text draw
        elif self._game_timer.get_time() - self._last_hurt_timestamp < Player.HURT_DUR:
            self._draw_text(self._hurt_text, player_image)
            
        # If dash duration is over update player speed
        if self._dash_on and (self._game_timer.get_time() - self._last_dash_timestamp > Player.DASH_DUR):
            self._speed = self._speed_before_dash
            self._dash_on = False

        # Update the other stuff
        self._hurt_pos = self._position
        self._hurt_tol = self._size * 1.25
        self._collision_tol = self._size * 1.5
        
    def draw_dead(self) -> None:
        """
        Draws the dead player on the screen.
        Scales the player's dead image based on the current size and blits it to the screen.
        """
        self._image_dead = pygame.transform.smoothscale(self._image_dead, self._scale)
        self._screen.blit(self._image_dead, self._position - pygame.Vector2(self._image_dead.width / 2, self._image_dead.height / 2))
        self._draw_accessory()