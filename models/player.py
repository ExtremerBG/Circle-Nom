from helpers.file_loader import dash_sounds
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
    TEXTS_NOM = "Nom!", "nom", "Nom-Nom!", "nom-nom"
    TEXTS_OW = "Ow!", "ow", "Ouch!", "ouch"
    
    def __init__(self, image: pygame.Surface, image_dead: pygame.Surface, easter_mode: bool, screen:pygame.Surface):
        """
        Initializes the Player object with images, easter mode, and screen.
        
        Args:
            image (pygame.Surface): The player's image.
            image_dead (pygame.Surface): The player's dead image.
            easter_mode (bool): Flag for easter mode.
            screen (pygame.Surface): The game screen.
        """
        self._image = image
        self._image_og = self._image
        self._image_dead = image_dead
        self._screen = screen
        self._easter = easter_mode
        self._size = 60
        self._scale = [self._size * 3, self._size * 3]
        self._position = pygame.Vector2(640, 140)
        self._speed = 30
        self._last_speed = 30
        self._dash_on = False
        self._dash_cd = Player.DASH_CD
        self._dash_dur = Player.DASH_DUR
        self._text = pygame.font.SysFont('Comic Sans MS', 30)
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
            self._eat_pos = pygame.Vector2(self._position.x, self._position.y - self._image.get_height() * - 0.3)
            self._eat_tol = self._size * 0.8
        
        self._hit_pos = self._position
        self._hit_tol = self._size * 1.25
        
    @property
    def eat_pos(self):
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
    def last_speed(self) -> int|float:
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
        
    def _draw_text(self, text:str):
        """
        Draws the specified text on the screen.
        
        Args:
            text (str): The text to draw.
        """
        text = self._text.render(f"{text}", True, (255, 255, 255))
        nom_text_rect = text.get_rect(center=(self._position.x, self._position.y - self._image.get_height() / 2 - self._size * 0.4))
        self._screen.blit(text, nom_text_rect)

    def _new_texts(self):
        """
        Selects new strings for ow_txt and nom_txt.
        """
        self._txt_nom = choice(Player.TEXTS_NOM)
        self._txt_ow = choice(Player.TEXTS_OW)
        
    def dash(self):
        """
        Activates the dash if the cooldown is ready.
        """
        FACTOR = 100
        EXPONENT = 1.4
        if self._dash_cd <= 0:
            self._last_speed = self._speed
            self._dash_on = True
            self._dash_dur = Player.DASH_DUR
            self._dash_cd = Player.DASH_CD
            # check others/dash_rates_bar_chart.py for visualization of this formula
            self._speed += ((FACTOR / (self._size ** EXPONENT)) * self._size)
            choice(dash_sounds).play()
            
    def draw(self, dt: float):
        """
        Draws the player on the screen and handles dash mechanics.

        Args:
            dt (float): Delta time, used for frame-independent drawing.
        """
        # Player resize and draw
        self._image = pygame.transform.smoothscale(self._image_og, self._scale)
        self._screen.blit(self._image, self._position - pygame.Vector2(self._image.get_width() / 2, self._image.get_height() / 2))
        
        # Dash cooldown and duration updates
        self._dash_cd = max(0, self._dash_cd - 60 * dt)
        if self._dash_on:
            self._dash_dur -= 40 * dt
            if self._dash_dur <= 0:
                self._dash_on = False
                self._speed = self._last_speed

        # Text draw
        if self.nom_txt_counter > 0:
            self._draw_text(self._txt_nom)
            self.nom_txt_counter -= 60 * dt
        if self.ow_txt_counter > 0:
            self._draw_text(self._txt_ow)
            self.ow_txt_counter -= 60 * dt

        # New texts
        if (self.nom_txt_counter or self.ow_txt_counter) <= 0:
            self._new_texts()

        # Update eat and hit positions
        if self._easter:
            self._eat_pos = self._position
            self._eat_tol = self._size * 1.25
        else:
            self._eat_pos = pygame.Vector2(self._position.x, self._position.y - self._image.get_height() * -0.3)
            self._eat_tol = self._size * 0.8

        # Update the other stuff
        self._hit_pos = self._position
        self._hit_tol = self._size * 1.25
        self._collision_tol = self._size * 1.5
        
        # Debug
        # print(f"dash_cd: {self.dash_cd:.2f} | dash_dur: {self._dash_dur:.2f} | dash_on: {self.dash_on}")

    def draw_dead(self):
        """
        Draws the dead player on the screen.
        Scales the player's dead image based on the current size and blits it to the screen.
        The position is adjusted based on whether the easter mode is active or not.
        """
        self._image_dead = pygame.transform.smoothscale(self._image_dead, self._scale)
        self._screen.blit(self._image_dead, self._position - pygame.Vector2(self._image_dead.get_width() / 2, self._image_dead.get_height() / 2))
        
    def draw_hit(self):
        """
        Temporarily modifies the player's image to be more reddish.
        """
        # Method 1 for easter mode.
        if self._easter:
            # Create a copy of the original image
            reddish_image = self._image.copy()

            # Fill the image with a red color, using the BLEND_RGBA_ADD flag to add the red component
            reddish_image.fill((200, 0, 0, 0), special_flags=pygame.BLEND_RGBA_ADD)

            # Blit the reddish image onto the screen
            self._screen.blit(reddish_image, self._position - pygame.Vector2(reddish_image.get_width() / 2, reddish_image.get_height() / 2))

        # Method 2 for non-easter mode.
        else:
            # Create a copy of the original image
            reddish_image = self._image.copy()

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

            # Blit the reddish image onto the screen
            self._screen.blit(reddish_image, self._position - pygame.Vector2(reddish_image.get_width() / 2, reddish_image.get_height() / 2))