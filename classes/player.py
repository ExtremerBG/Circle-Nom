import pygame

class Player():

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
        self._position = pygame.Vector2(self._screen.get_width() / 2 - 128, self._screen.get_height() / 2 - 128)
        self._size = 90
        self._scale = [self._size * 3, self._size * 3]
        self._eat_tol = self._size * 1.75
        self._speed:float = 10
        self._eat_txt = False
        self._text = pygame.font.SysFont('Comic Sans MS', 30)


    def draw(self):
        """
        Draws the player on the screen.
        Scales the player's image based on the current size and blits it to the screen.
        The position is adjusted based on whether the easter mode is active or not.
        """
        self._image = pygame.transform.smoothscale(self._image_og, self._scale)
        if self._easter == False:
            self._screen.blit(self._image, self._position - pygame.Vector2(self._image.get_width() / 2, self._image.get_height() / 1.3))
        else:
            self._screen.blit(self._image, self._position - pygame.Vector2(self._image.get_width() / 2, self._image.get_height() / 2))

    def draw_dead(self):
        """
        Draws the dead player on the screen.
        Scales the player's dead image based on the current size and blits it to the screen.
        The position is adjusted based on whether the easter mode is active or not.
        """
        self._image_dead = pygame.transform.smoothscale(self._image_dead, self._scale)
        if self._easter == False:
            self._screen.blit(self._image_dead, self._position - pygame.Vector2(self._image_dead.get_width() / 2, self._image_dead.get_height() / 1.3))
        else:
            self._screen.blit(self._image_dead, self._position - pygame.Vector2(self._image_dead.get_width() / 2, self._image_dead.get_height() / 2))

    def draw_eat_text(self):
        """
        Draws the "Nom!" text on the screen when the player eats.
        The position of the text is adjusted based on whether the easter mode is active or not.
        """
        nom_text = self._text.render("Nom!", True, (255, 255, 255))

        if self._easter == False:
            nom_text_rect = nom_text.get_rect(center=(self._position.x, self._position.y - self._image.get_height() / 2 - self._size - 15))
        else:
            nom_text_rect = nom_text.get_rect(center=(self._position.x, self._position.y - self._image.get_height() / 2 - self._size + 15))

        self._screen.blit(nom_text, nom_text_rect)

    @property
    def eat_tol(self) -> float:
        """
        Returns the player's eat tolerance.
        The eat tolerance determines the range within which the player can eat prey.
        """
        return self._eat_tol
    
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
    def eat_txt(self) -> bool:
        """
        Returns whether the eat text is displayed.
        """
        return self._eat_txt
    
    @size.setter
    def size(self, value:float):
        """
        Sets the player's size.
        
        Args:
            value (float): The new size of the player.
        """
        self._size = value
        self._scale = [self._size * 3, self._size * 3]

    @speed.setter
    def speed(self, value:float):
        """
        Sets the player's speed.
        
        Args:
            value (float): The new speed of the player.
        """
        self._speed = value

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
    def eat_txt(self, value:bool):
        """
        Sets whether the eat text is displayed.
        
        Args:
            value (bool): The new state of the eat text display.
        """
        if type(value) != bool:
            raise ValueError("Eat text accepts bool only!")
        self._eat_txt = value
