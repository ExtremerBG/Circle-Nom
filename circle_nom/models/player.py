from encodings.punycode import T
from circle_nom.helpers.player_utils import player_dash_speed_increase
from circle_nom.helpers.asset_bank import DASH_SOUNDS, COMIC_SANS_MS
from random import choice
import numpy as np
import pygame

class Player():
    
    # Dash cooldown and duration
    DASH_CD = 70
    DASH_DUR = 6

    # Speed limiters
    MIN_SPEED = 15   
    MAX_SPEED = 30

    # Size limiters
    MIN_SIZE = 30
    MAX_SIZE = 120
    
    # Texts for drawing
    TEXTS_NOM = "Nom!", "Nom", "nom!", "nom"
    TEXTS_OW = "Ow!", "ow", "Ouch!", "ouch"
    
    def __init__(self, image_alive: pygame.Surface, image_dead: pygame.Surface, 
                 eat_sequence: list[pygame.Surface] | None, accessory: tuple[pygame.Vector2, pygame.Surface] | None,
                 easter_mode: bool, screen:pygame.Surface):
        """
        Initializes the Player object with images, easter mode, and screen.
        
        Args:
            image_alive (pygame.Surface): The player's alive image.
            image_dead (pygame.Surface): The player's dead image.
            eat_sequence (list(pygame.Surface)|None): The player's eat sequence animation.
            player_accessory (tuple(pygame.Vector2, pygame.Surface)|None): The player's accessory data pair.
            easter_mode (bool): Flag for easter mode.
            screen (pygame.Surface): The game screen.
        """
        self._easter = easter_mode
        self._image_alive = image_alive
        self._image_hit = self._modify_hit()
        self._draw_hit = False
        self._image_dead = image_dead
        self._eat_sequence = eat_sequence
        self._eat_animation_counter = 0
        self._can_eat = True
        self._accessory = accessory
        self._screen = screen
        self._size = 60
        self._scale = [self._size * 3, self._size * 3]
        self._position = pygame.Vector2(640, 140)
        self._speed = 30
        self._last_speed = 30
        self._dash_on = False
        self._dash_cd = Player.DASH_CD
        self._dash_dur = Player.DASH_DUR
        self._font = pygame.Font(COMIC_SANS_MS, 30)
        self.nom_txt_counter = 0
        self.ow_txt_counter = 0
        self._txt_nom = choice(Player.TEXTS_NOM)
        self._txt_ow = choice(Player.TEXTS_OW)
        self._points = 0

       # Different eat pos / eat_tol if easter is on
        if self._easter == True:
            self._eat_pos = self._position
            self._eat_tol = self._size * 1.25
        else:
            self._eat_pos = pygame.Vector2(self._position.x, self._position.y - self._image_alive.get_height() * - 0.3)
            self._eat_tol = self._size * 0.8
        
        self._hit_pos = self._position
        self._hit_tol = self._size * 1.25
        
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
        return self._hit_pos
    
    @property
    def hit_tol(self) -> float:
        """
        Returns the player's hit tolerance.
        
        Returns:
            float: The hit tolerance of the player.
        """
        return self._hit_tol
    
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
    def last_speed(self) -> float:
        """
        Returns the player's last speed before dash.
        
        Returns:
            float: The last speed of the player.
        """
        return self._last_speed
    
    @property
    def dash_available(self) -> bool:
        """
        Returns if the player's dash is available.
        
        Returns:
            bool: True if internal dash CD is <= 0, false otherwise.
        """
        return self._dash_cd <= 0
    
    @property
    def dash_on(self) -> bool:
        """ 
        Returns if the player's dash is currently active.
        
        Returns:
            bool: The dash_on bool.
        """
        return self._dash_on
    
    @property
    def position(self) -> pygame.Vector2:
        """
        Returns the player's position.
        
        Returns:
            pygame.Vector2: The position of the player.
        """
        return self._position
    
    @property
    def scale(self) -> list[int|float]:
        """
        Returns the player's scale.
        
        Returns:
            list: The scale of the player.
        """
        return self._scale
    
    @property
    def eat_txt(self) -> bool:
        """
        Returns whether the eat text is displayed.
        
        Returns:
            bool: True if the eat text is displayed, False otherwise.
        """
        return self._nom_txt_counter > 0
    
    @property
    def ow_txt(self) -> bool:
        """
        Returns whether the ow text is displayed.
        
        Returns:
            bool: True if the ow text is displayed, False otherwise.
        """
        return self._ow_txt_counter > 0
    
    @property
    def points(self) -> int:
        """
        Returns the player's points.
        
        Returns:
            int: The points of the player.
        """
        return self._points
    
    @property
    def draw_hit(self) -> bool:
        """
        Returns the player's draw_hit boolean.
        
        Returns:
            bool: The draw_hit boolean.
        """
        return self._draw_hit
    
    @property
    def can_eat(self) -> bool:
        """
        Returns the player's can_eat boolean.
        
        Returns:
            bool: The can_eat boolean.
        """
        return self._can_eat
    
    @size.setter
    def size(self, value:float):
        """
        Sets the player's size. Has min/max values, Player check class.
        
        Args:
            value (float): The new size of the player.
        """
        self._size = value

        if self._size < Player.MIN_SIZE:
            self._size = Player.MIN_SIZE
        
        if self._size > Player.MAX_SIZE:
            self._size = Player.MAX_SIZE

        self._scale = [self._size * 3, self._size * 3]

    @speed.setter
    def speed(self, value:float):
        """
        Sets the player's speed. Has min/max values, check Player class.
        
        Args:
            value (float): The new speed of the player.
        """
        self._speed = value
        if self._speed < Player.MIN_SPEED: self._speed = Player.MIN_SPEED
        if not self._dash_on: # Max speed cap only if dash is not on
            if self._speed > Player.MAX_SPEED: self._speed = Player.MAX_SPEED 
            
    @last_speed.setter
    def last_speed(self, value:float):
        """
        Set the player's last speed before a dash.
        
        Args:
            value (float): The new last speed of the player.
        """
        self._last_speed = value
        
    @position.setter
    def position(self, value: pygame.Vector2):
        """
        Sets the player's position.
        
        Args:
            value (pygame.Vector2): The new position of the player.
        """
        if type(value) != pygame.Vector2:
            raise ValueError("Position coordinates accepts pygame.Vector2 only!")
        self._position = value

    @eat_tol.setter
    def eat_tol(self, value:float):
        """
        Sets the player's eat tolerance.
        
        Args:
            value (float): The new eat tolerance of the player.
        """
        if value < 0:
            raise ValueError("Eat tolerance cannot be less than 0!")
        self._eat_tol = value

    @eat_txt.setter
    def eat_txt(self, value:int):
        """
        Sets whether the eat text is displayed.
        
        Args:
            value (int): Frames for eat_txt to display.
        """
        if type(value) != int:
            raise ValueError("Nom text accepts int only!")
        if value:
            self._nom_txt_counter = value
        else:
            self._nom_txt_counter = 0

    @ow_txt.setter
    def ow_txt(self, value:bool):
        """
        Sets whether the ow text is displayed.
        
        Args:
            value (bool): Frames for ow_txt to display.
        """
        if type(value) != int:
            raise ValueError("Ow text accepts int only!")
        if value:
            self._ow_txt_counter = value
        else:
            self._ow_txt_counter = 0

    @points.setter
    def points(self, value:int):
        """
        Sets the player's points.
        
        Args:
            value (int): The new points of the player.
        """
        if type(value) != int:
            raise ValueError("Points accepts int only!")
        
        if value < 0:
            raise ValueError("Points cannot be less than 0!")

        self._points = value
        
    @draw_hit.setter
    def draw_hit(self, value:bool):
        """
        Set the player's draw hit boolean. If True, draw() method will use \n
        reddish image instead of the normal one.
        
        Args:
            value (bool): The state boolean.
        """
        if type(value) != bool:
            raise ValueError("draw_hit accepts bool only!")
        self._draw_hit = value
        
    @classmethod
    def dash_cd(cls, value:int):
        """ 
        Sets the Player's dash cooldown to the given value.
        
        Args:
            value (int): The given new value for the cooldown.
        """
        if type(value) != int:
            raise ValueError("dash_cd accepts int only!")
        cls.DASH_CD = value
        
    def _modify_hit(self):
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
        
    def _draw_text(self, text:str, image: pygame.Surface):
        """
        Draws the specified text on the screen.
        
        Args:
            text (str): The text to draw.
            image (pygame.Surface): The image to offset the text from.
        """
        text = self._font.render(f"{text}", True, (255, 255, 255))
        nom_text_rect = text.get_rect(center=(self._position.x, self._position.y - image.get_height() / 2 - self._size * 0.8))
        self._screen.blit(text, nom_text_rect)

    def _new_texts(self):
        """
        Selects new strings for ow_txt and nom_txt.
        """
        self._txt_nom = choice(Player.TEXTS_NOM)
        self._txt_ow = choice(Player.TEXTS_OW)
        
    def _draw_accessory(self):
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
                (self._accessory[1].get_width() * scale_factor),
                (self._accessory[1].get_height() * scale_factor)
            )
            scaled_image = pygame.transform.smoothscale(self._accessory[1], accessory_size)
            # Calculate the top-left of the player image
            player_topleft = self._position - pygame.Vector2(self._scale[0] / 2, self._scale[1] / 2)
            # Blit at the correct position
            self._screen.blit(
                scaled_image,
                player_topleft + scaled_offset - pygame.Vector2(scaled_image.get_width() / 2, scaled_image.get_height() / 2)
            )
        
    def dash(self):
        """
        Activates the dash if the cooldown is ready.
        """
        if self._dash_cd <= 0:
            self._last_speed = self._speed
            self._dash_on = True
            self._dash_dur = Player.DASH_DUR
            self._dash_cd = Player.DASH_CD
            self._speed += player_dash_speed_increase(self)
            choice(DASH_SOUNDS).play()
            
    def draw(self, dt: float):
        """
        Draws the player on the screen and handles dash mechanics.

        Args:
            dt (float): Delta time, used for frame-independent drawing.
        """
        # Eat animation draw
        if self.nom_txt_counter > 0 and self._eat_sequence:
            player_image = self._eat_sequence[int(self._eat_animation_counter / 6 % len(self._eat_sequence))]
            player_image = pygame.transform.smoothscale(player_image, self._scale)
            self._screen.blit(player_image, self._position - pygame.Vector2(player_image.get_width() / 2, player_image.get_height() / 2))
            self._can_eat = False
            
        # Hit draw
        elif self.ow_txt_counter > 0:
            player_image = pygame.transform.smoothscale(self._image_hit, self._scale)
            self._screen.blit(player_image, self._position - pygame.Vector2(player_image.get_width() / 2, player_image.get_height() / 2))
            self._can_eat = True
            
        # Normal draw
        else:
            # Player resize and draw
            player_image = pygame.transform.smoothscale(self._image_alive, self._scale)
            self._screen.blit(player_image, self._position - pygame.Vector2(player_image.get_width() / 2, player_image.get_height() / 2))
            self._can_eat = True
            
        # Update eat and hit positions based on the image from draw
        if not self._easter:
            self._eat_pos = pygame.Vector2(self._position.x, self._position.y - player_image.get_height() * -0.3)
            self._eat_tol = self._size * 0.8
        else:
            self._eat_pos = self._position
            self._eat_tol = self._size * 1.25
        
        # Draw player's accessory before text
        self._draw_accessory()
        
        # Text draw
        # Eat
        if self.nom_txt_counter > 0:
            self._draw_text(self._txt_nom, player_image)
            self.nom_txt_counter -= 80 * dt
            
        # Hit
        if self.ow_txt_counter > 0:
            self._draw_text(self._txt_ow, player_image)
            self.ow_txt_counter -= 80 * dt

        # New texts
        if (self.nom_txt_counter or self.ow_txt_counter) <= 0:
            self._new_texts()
            
        # Dash cooldown and duration updates
        self._dash_cd = max(0, self._dash_cd - 60 * dt)
        if self._dash_on:
            self._dash_dur -= 40 * dt
            if self._dash_dur <= 0:
                self._dash_on = False
                self._speed = self._last_speed

        # Update the other stuff
        self._hit_pos = self._position
        self._hit_tol = self._size * 1.25
        self._collision_tol = self._size * 1.5
        self._eat_animation_counter += 40 * dt
        
    def draw_dead(self):
        """
        Draws the dead player on the screen.
        Scales the player's dead image based on the current size and blits it to the screen.
        The position is adjusted based on whether the easter mode is active or not.
        """
        self._image_dead = pygame.transform.smoothscale(self._image_dead, self._scale)
        self._screen.blit(self._image_dead, self._position - pygame.Vector2(self._image_dead.get_width() / 2, self._image_dead.get_height() / 2))
        self._draw_accessory()