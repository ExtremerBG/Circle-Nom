import pygame

class Player():

    def __init__(self, image: pygame.image, image_dead: pygame.image, easter_mode: bool, screen:pygame.display):

        """
        Takes the directory to 2 pygame images, \n
        bool for easter mode and a pygame display.
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
        self._speed = 10
        self._eat_txt = False
        self._text = pygame.font.SysFont('Comic Sans MS', 30)


    def draw(self):
        """
        Draws player on the screen.
        """
        self._image = pygame.transform.smoothscale(self._image_og, self._scale)
        if self._easter == False:
            self._screen.blit(self._image, self._position - pygame.Vector2(self._image.get_width() / 2, self._image.get_height() / 1.3))
        else:
            self._screen.blit(self._image, self._position - pygame.Vector2(self._image.get_width() / 2, self._image.get_height() / 2))

    def draw_dead(self):
        """
        Draws dead player on the screen.
        """
        self._image_dead = pygame.transform.smoothscale(self._image_dead, self._scale)
        if self._easter == False:
            self._screen.blit(self._image_dead, self._position - pygame.Vector2(self._image_dead.get_width() / 2, self._image_dead.get_height() / 1.3))
        else:
            self._screen.blit(self._image_dead, self._position - pygame.Vector2(self._image_dead.get_width() / 2, self._image_dead.get_height() / 2))

    def draw_eat_text(self):
        """
        Draw eat text.
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
        Returns player eat tolerance.
        """
        return self._eat_tol
    
    @property
    def size(self) -> float:
        """
        Returns player size.
        """
        return self._size
    
    @property
    def speed(self) -> float:
        """
        Returns player speed.
        """
        return self._speed
    
    @property
    def position(self) -> pygame.Vector2:
        """
        Returns player position.
        """
        return self._position
    
    @property
    def eat_txt(self) -> bool:
        """
        Returns eat text state.
        """
        return self._eat_txt
    
    @size.setter
    def size(self, value:tuple):
        """
        Value: Tuple with 2 elements: \n
        1 - Given size, accepts float. \n
        2 - ADD/SET: False to add the size, True to set it.
        """
        if type(value) != tuple:
            raise ValueError("Size setter only accepts tuple with 2 values: (int/float, bool)!")

        if len(value) > 2 or len(value) < 2:
            raise ValueError("Size setter only accepts tuple with 2 values: (int/float, bool)!")

        # If bool is true, SET the size
        if value[1] == True:

            self._size = value[0]
            self._scale = [self._size * 3, self._size * 3]

        else:
            self._size += value[0]
            self._scale = [self._size * 3, self._size * 3]

    @speed.setter
    def speed(self, value:tuple):
        """
        Value: Tuple with 2 elements: \n
        1 - Given speed, accepts integer or float. \n
        2 - ADD/SET setting (bool): False to += the speed, True to = it.
        """

        if len(value) > 2 or len(value) < 2:
            raise ValueError("Speed setter only accepts tuple with 2 values: (int/float, bool)!")
        
        # If bool is true, SET the speed
        if value[1] == True:
            self._speed = value[0]

        else:
            self._speed += value[0]

    @position.setter
    def position(self, value: pygame.Vector2):
        """
        SET player position to the given value.
        """
        if type(value) != pygame.Vector2:
            raise ValueError("Position coordinates accepts pygame.Vector2 only!")
        self._position = value

    @eat_tol.setter
    def eat_tol(self, value:float):
        """
        SET player eat tolerance to the given value.
        """
        if value < 0:
            raise ValueError("Eat tolerance cannot be less than 0!")
        self._eat_tol = value

    @eat_txt.setter
    def eat_txt(self, value:bool):
        """
        SET player eat text value.
        """
        if type(value) != bool:
            raise ValueError("Eat text accepts bool only!")
        self._eat_txt = value
