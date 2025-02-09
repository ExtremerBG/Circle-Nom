import pygame

class Player():

    # Speed limiters
    min_speed = 12    
    max_speed = 30

    # Size limiters
    min_size = 30
    max_size = 120

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
        self._speed = 24
        self._text = pygame.font.SysFont('Comic Sans MS', 30)
        self.ow_txt_counter = 0
        self.nom_txt_counter = 0

       # Different eat pos / eat_tol if easter is on
        if self._easter == True:
            self._eat_pos = self._position
            self._eat_tol = self._size * 1.25
        else:
            self._eat_pos = pygame.Vector2(self._position.x, self._position.y - self._image.get_height() * - 0.3)
            self._eat_tol = self._size * 0.8
        
        self._hit_pos = self._position
        self._hit_tol = self._size * 1.25

    def draw(self):
        """
        Draws the player on the screen.
        Scales the player's image based on the current size and blits it to the screen.
        The position is adjusted based on whether the easter mode is active or not.
        """

        self._image = pygame.transform.smoothscale(self._image_og, self._scale)
        self._screen.blit(self._image, self._position - pygame.Vector2(self._image.get_width() / 2, self._image.get_height() / 2))

        if self.ow_txt_counter > 0:
            self.draw_text("Ow!")
            self.ow_txt_counter -= 1
        if self.nom_txt_counter > 0:
            self.draw_text("Nom!")
            self.nom_txt_counter -= 1

       # Different eat pos / eat_tol if easter is on
        if self._easter == True:
            self._eat_pos = self._position
            self._eat_tol = self._size * 1.25
        else:
            self._eat_pos = pygame.Vector2(self._position.x, self._position.y - self._image.get_height() * - 0.3)
            self._eat_tol = self._size * 0.8
        
        self._hit_pos = self._position
        self._hit_tol = self._size * 1.25

    def draw_dead(self):
        """
        Draws the dead player on the screen.
        Scales the player's dead image based on the current size and blits it to the screen.
        The position is adjusted based on whether the easter mode is active or not.
        """
        self._image_dead = pygame.transform.smoothscale(self._image_dead, self._scale)
        self._screen.blit(self._image_dead, self._position - pygame.Vector2(self._image_dead.get_width() / 2, self._image_dead.get_height() / 2))

    def draw_text(self, text:str):
        """
        Draws the "Nom!" text on the screen when the player eats.
        The position of the text is adjusted based on whether the easter mode is active or not.
        """
        text = self._text.render(f"{text}", True, (255, 255, 255))

        nom_text_rect = text.get_rect(center=(self._position.x, self._position.y - self._image.get_height() / 2 - self._size * 0.5))

        self._screen.blit(text, nom_text_rect)

    def draw_hit(self):
        """
        Draws a red semi-transparent overlay over the player.
        """
        # Calculate the size of the hit overlay based on the player's size
        overlay_size = self.scale

        # Create a surface with an alpha channel (RGBA)
        hit_overlay = pygame.Surface(overlay_size, pygame.SRCALPHA)

        # Calculate the position and radius of the circle
        circle_center = (overlay_size[0] // 2, overlay_size[1] // 2)
        circle_radius = self._size * 1.5

        # Draw a red circle with a specified alpha value (0-255)
        pygame.draw.circle(hit_overlay, (255, 0, 0, 128), circle_center, int(circle_radius))  # 128 is the alpha value for 50% transparency

        # Blit (copy) the surface with the circle onto the display
        self._screen.blit(hit_overlay, self._position - pygame.Vector2(overlay_size[0] // 2, overlay_size[1] // 2))

    @property
    def eat_pos(self):
        return self._eat_pos

    @property
    def eat_tol(self) -> float:
        """
        Returns the player's eat tolerance.
        The eat tolerance determines the range within which the player can eat prey.
        """
        return self._eat_tol
    
    @property
    def hit_pos(self):
        return self._hit_pos
    
    @property
    def hit_tol(self):
        return self._hit_tol
    
    @property
    def size(self) -> float:
        """
        Returns the player's size.
        """
        return self._size
    
    @property
    def speed(self) -> float:
        """
        Returns the player's speed.
        """
        return self._speed
    
    @property
    def position(self) -> pygame.Vector2:
        """
        Returns the player's position.
        """
        return self._position
    
    @property
    def scale(self):
        return self._scale
    
    @property
    def eat_txt(self) -> bool:
        """
        Returns whether the eat text is displayed.
        """
        return self._nom_txt_counter > 0
    
    @property
    def ow_txt(self) -> bool:
        """
        Returns wheter the ow text is displayed.
        """
        return self._ow_txt_counter > 0
    
    @size.setter
    def size(self, value:float):
        f"""
        Sets the player's size. Min/Max values: {Player.min_size}/{Player.max_size}
        
        Args:
            value (float): The new size of the player.
        """
        self._size = value

        if self._size < Player.min_size:
            self._size = Player.min_size
        
        if self._size > Player.max_size:
            self._size = Player.max_size

        self._scale = [self._size * 3, self._size * 3]

    @speed.setter
    def speed(self, value:float):
        f"""
        Sets the player's speed. Min/Max values: {Player.min_speed}/{Player.max_speed}
        
        Args:
            value (float): The new speed of the player.
        """
        self._speed = value
        if self._speed < Player.min_speed:
            self._speed = Player.min_speed
        
        if self._speed > Player.max_speed:
            self._speed = Player.max_speed

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
            self._nom_txt_counter = value  # Display "Nom!" text for 60 frames (1 second at 60 FPS)
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
            self._ow_txt_counter = value  # Display "Ow!" text for 60 frames (1 second at 60 FPS)
        else:
            self._ow_txt_counter = 0