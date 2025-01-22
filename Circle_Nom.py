# Emko/ExtremerBG was here

# Circle Nom Game

# Importing modules
from game_funcs import *
from time import sleep
import pygame
import gif_pygame
from math import isclose

# Pygame initialization
pygame.init()

# Screen size, title and icon
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Circle Nom")
pygame.display.set_icon(pygame.image.load(resource_path('images/icon.ico')))

# Clock for framerate
clock = pygame.time.Clock()

# Game loop
running = True

# Delta time
dt = 0

# Font setup
pygame.font.init()
text = pygame.font.SysFont('Comic Sans MS', 30)
text_big = pygame.font.SysFont('Comic Sans MS', 60)
text_small = pygame.font.SysFont('Comic Sans MS', 15)

# SFX setup
pygame.mixer.init()
_eat_sound1 = pygame.mixer.Sound(resource_path('sounds/nom_1.wav'))
_eat_sound2 = pygame.mixer.Sound(resource_path('sounds/nom_2.wav'))
_eat_sound3 = pygame.mixer.Sound(resource_path('sounds/nom_3.wav'))
_eat_sound4 = pygame.mixer.Sound(resource_path('sounds/nom_4.wav'))
_eat_sound5 = pygame.mixer.Sound(resource_path('sounds/nom_5.wav'))

# List of eat sounds for random selection + lenght
eat_sounds = [_eat_sound1, _eat_sound2, _eat_sound3, _eat_sound4, _eat_sound5]
len_eat_sounds = len(eat_sounds)

# Theme song setup
_theme_song_1 = pygame.mixer.Sound(resource_path('sounds/theme_song_1.wav'))
_theme_song_2 = pygame.mixer.Sound(resource_path('sounds/theme_song_2.wav'))
_theme_song_3 = pygame.mixer.Sound(resource_path('sounds/theme_song_3.wav'))
_theme_song_4 = pygame.mixer.Sound(resource_path('sounds/theme_song_4.wav'))
_theme_song_5 = pygame.mixer.Sound(resource_path('sounds/theme_song_5.wav'))

# List of theme songs + lenght
theme_songs = [_theme_song_1, _theme_song_2, _theme_song_3, _theme_song_4, _theme_song_5]
len_theme_songs = len(theme_songs)

# Play random theme song from list, set volume and get length of song
song_index = rand_num(len_theme_songs)
theme_song = theme_songs[song_index]
theme_lenght = theme_song.get_length()
theme_song.set_volume(0.4)
theme_song.play()

# Load Player images
_player_image_1 = pygame.image.load(resource_path('images/player_image_1.png'))
_player_image_2 = pygame.image.load(resource_path('images/player_image_2.png'))
_player_image_3 = pygame.image.load(resource_path('images/player_image_3.png'))

# Load dead Player images
_player_image_1_dead = pygame.image.load(resource_path('images/player_image_1_dead.png'))
_player_image_2_dead = pygame.image.load(resource_path('images/player_image_2_dead.png'))
_player_image_3_dead = pygame.image.load(resource_path('images/player_image_3_dead.png'))

# Make lists of both
player_images = [_player_image_1, _player_image_2, _player_image_3]
player_images_dead = [_player_image_1_dead, _player_image_2_dead, _player_image_3_dead]

# Get lenght of both
len_player_images = len(player_images)
len_player_images_dead = len(player_images_dead)

# Warning message if lengths of player lists are different
if len_player_images != len_player_images_dead:
    raise ValueError("Lenghts of player lists different!")

# Load prey images
prey_glowing_sandwich = gif_pygame.load(resource_path('images/glowing_sandwich.png'))
_prey_image_1 = pygame.image.load(resource_path('images/prey_image_1.png'))
_prey_image_2 = pygame.image.load(resource_path('images/prey_image_2.png'))
_prey_image_3 = pygame.image.load(resource_path('images/prey_image_3.png'))
_prey_image_4 = pygame.image.load(resource_path('images/prey_image_4.png'))
_prey_image_5 = pygame.image.load(resource_path('images/prey_image_5.png'))
_prey_image_6 = pygame.image.load(resource_path('images/prey_image_6.png'))
_prey_image_7 = pygame.image.load(resource_path('images/prey_image_7.png'))
_prey_image_8 = pygame.image.load(resource_path('images/prey_image_8.png'))
_prey_image_9 = pygame.image.load(resource_path('images/prey_image_9.png'))
_prey_image_10 = pygame.image.load(resource_path('images/prey_image_10.png'))

# List of prey images
prey_images = [ prey_glowing_sandwich,
    _prey_image_1, _prey_image_2, _prey_image_3, _prey_image_4, _prey_image_5,
    _prey_image_6, _prey_image_7, _prey_image_8, _prey_image_9, _prey_image_10
]
len_prey_images = len(prey_images)

# Load background images
background_image_1 = pygame.image.load(resource_path('images/background_image_1.jpg'))
background_image_2 = pygame.image.load(resource_path('images/background_image_2.jpg'))
background_image_3 = pygame.image.load(resource_path('images/background_image_3.jpg'))

# List of backgrounds for random selection + lenght
background_images = [background_image_1, background_image_2, background_image_3]
len_background_images = len(background_images)

# Declare random background
background_image = background_images[rand_num(len_background_images)]

# Function for displaying FPS
def fps_counter():
    fps = int(clock.get_fps())
    return fps

class Player():

    def __init__(self, image: pygame.image, image_dead: pygame.image, easter_mode: bool):

        self._image = image
        self._image_og = self._image
        self._image_dead = image_dead
        self._easter_mode = easter_mode
        self._position = pygame.Vector2(screen.get_width() / 2 - 128, screen.get_height() / 2 - 128)
        self._size = 80
        self._scale = [self._size * 3, self._size * 3]
        self._eat_tol = self._size * 1.75
        self._speed = 10
        self._eat_txt = False

    def draw(self):
        """
        Draws player on the screen.
        """
        self._image = pygame.transform.smoothscale(self._image_og, self._scale)
        if self._easter_mode == False:
            screen.blit(self._image, self._position - pygame.Vector2(self._image.get_width() / 2, self._image.get_height() / 1.3))
        else:
            screen.blit(self._image, self._position - pygame.Vector2(self._image.get_width() / 2, self._image.get_height() / 2))

    def draw_dead(self):
        """
        Draws dead player on the screen.
        """
        self._image_dead = pygame.transform.smoothscale(self._image_dead, self._scale)
        if self._easter_mode == False:
            screen.blit(self._image_dead, self._position - pygame.Vector2(self._image_dead.get_width() / 2, self._image_dead.get_height() / 1.3))
        else:
            screen.blit(self._image_dead, self._position - pygame.Vector2(self._image_dead.get_width() / 2, self._image_dead.get_height() / 2))

    def draw_eat_text(self):
        """
        Draw 2 different eat texts above player, decided by the prey index.
        """
        if prey_1.index == 0 and prey_1.created == False and easter == False:
            nom_text = text.render("NOM NOM NOM!", True, (255, 255, 255))
        else:
            nom_text = text.render("Nom!", True, (255, 255, 255))

        x, y = self._position
        x -= nom_text.get_width() / 2
        y -= self._size / 0.335
        screen.blit(nom_text, (x, y))

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

        if len(value) > 2 or len(value) < 2:
            raise ValueError("Size setter only accepts list with 2 values: (int/float, bool)!")

        # If bool is true, SET the size
        if value[1] == True:

            self._size = 100
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

class Prey():

    def __init__(self, list_images:list):

        self._created = True
        self._counter = 0
        self._image_index = rand_num(len_prey_images)
        self._image = list_images[self._image_index]
        self._coords = rand_screen_pos()
        self._angle = rand_num(360)

    def draw(self):
        """
        Draw prey on the screen.
        """
        if self._image_index == 0 and easter == False:
            self._image.render(screen, self._coords- pygame.Vector2(self._image.get_width() / 2, self._image.get_height() / 2))
        else:
            screen.blit(image_rotate(self._image, self._angle), self._coords - pygame.Vector2(self._image.get_width() / 2, self._image.get_height() / 2))

    def coords_reset(self):
        """
        Sets prey coordinates (X, Y) to infinite.
        """
        self._coords = float('inf'), float('inf')

    @property
    def index(self):
        """
        Returns prey image index.
        """
        return self._image_index
    
    @property
    def coords(self):
        """
        Returns prey coordinates (X, Y).
        """
        return self._coords
    
    @property
    def created(self):
        """
        Returns prey created state.
        """
        return self._created
    
    @property
    def counter(self):
        """
        Returns prey counter.
        """
        return self._counter
    
    @created.setter
    def created(self, value:bool):
        if type(value) != bool:
            raise ValueError("Created accepts bool only!")
        self._created = value

    @counter.setter
    def counter(self, value: float):
        if value < 0:
            raise ValueError("Counter cannot be below 0!")
        self._counter = value

# Get random Player image and its dead counterpart
rand_player_image_index = rand_num(len_player_images)
player_image = player_images[rand_player_image_index]
player_image_dead = player_images_dead[rand_player_image_index]

# Store backup Player image, so no loss of quality occurs with pygame.transform
player_image_og = player_image

# Declaring player
# 10% Chance of reversing Player/Prey for easter egg
easter = rand_num(10)
if easter < 9:
    
    easter = True
    num = rand_num(len_prey_images)

    # Check if the image is glowing_sandwich
    if num > 0:
        player_1 = Player(prey_images[num], prey_images[num], easter)

    # If it is, set player images to another image, since gif_pygame doesn't support code below
    else:
        player_1 = Player(prey_images[1], prey_images[1], easter)
    
    # Resets prey list
    prey_images = []

    # Add all player images to prey list
    for image in player_images:
        prey_image = pygame.transform.smoothscale(image, (64, 64))
        prey_images.append(prey_image)
    for image in player_images_dead:
        prey_image = pygame.transform.smoothscale(image, (64, 64))
        prey_images.append(prey_image)

    # Set len of prey images again after easter
    len_prey_images = len(prey_images)
else:
    easter = False
    player_1 = Player(player_image, player_image_dead, easter)

# Initial points
points = 0

# Prey spawn timer
spawn = 30 

# Prey despawn timer
despawn = 90

# Initial prey declaration
prey_1 = Prey(prey_images)
prey_1.counter = despawn
prey_1.coords_reset()

# Game Loop
while running:

    # Fill the screen with background image to wipe away anything from last frame
    screen.blit(background_image, (0, 0))

    # Player size decrease
    player_1.size = -0.2, False

    # Player eat tolerance change
    if easter == False:
        player_1.eat_tol = player_1.size * 0.85
    else:
        player_1.eat_tol = player_1.size * 1.25

    # Player speed decrease
    if player_1.speed > 10:
        player_1.speed = -0.1, False

    # Draw player
    player_1.draw()

    # Print eat text
    if player_1.eat_txt == True:
        player_1.draw_eat_text()

    # Counter for prey spawn
    prey_1.counter += 1
    
    # Create new prey
    if prey_1.counter > spawn and prey_1.created == False:

        prey_1 = Prey(prey_images)
        prey_1.counter = 30

    # Draw prey & remove player eat text
    if prey_1.counter > spawn and prey_1.created == True:
        player_1.eat_txt = False
        prey_1.draw()

    # Despawn prey
    if prey_1.counter > despawn and prey_1.created == True: 
        
        # Set counter for spawn/despawn
        prey_1.counter = 0

        # Sets False so new prey can be created
        prey_1.created = False

        # Remove points for missing prey
        if points > 0:
            points -= 1

        # Remove eat text
        player_1.eat_txt = False

        # Reset coords
        prey_1.coords_reset()

    # Eating prey
    if isclose(player_1.position.x, prey_1.coords[0], abs_tol=player_1.eat_tol) and isclose(player_1.position.y, prey_1.coords[1], abs_tol=player_1.eat_tol) and prey_1.created == True:

        if easter == False:
            # Bonus size, speed & points for sandwich.
            if prey_1.index == 0:
                player_1.size = 40, False
                player_1.speed =20, False
                points += 5
            else:
                player_1.size = 20, False
                points += 1

        # Different size/speed/points if easter mode is on
        else:
            player_1.size = 14, False
            player_1.speed = 7, False
            points += 2

        # Check if player is getting too big
        if player_1.size > 110:
            player_1.size = 110, True

        # Check if player is getting too fast
        if player_1.speed > 30:
            player_1.speed = 30, True

        # Play random sound
        eat_sounds[rand_num(len_eat_sounds)].play()

        # Sets False because prey is eaten
        prey_1.created = False

        # Reset spawn counter
        prey_1.counter = 0

        # Set eat text to show
        player_1.eat_txt = True

        # Reset coords
        prey_1.coords_reset()

    # Set True to use debug prints and dots
    if False:
        print(f"player_1_pos X: {player_1.position.x:.2f} Y: {player_1.position.y:.2f}",end=" || ") 

        print(f"prey_1_pos X: {prey_1.coords[0]} Y: {prey_1.coords[1]}",end=" || ")

        print(f"prey_1.counter: {prey_1.counter}",end=" || ")

        print(f"prey_1.created: {prey_1.created}",end=" || ")

        print(f"player_1.eat_tol: {player_1.eat_tol:.2f}",end=" || ")

        print(f"player_1.size: {player_1.size:.2f}", end=" || ")

        print(f"player_1.speed: {player_1.speed:.2f}")

        # Debug position dots
        pygame.draw.circle(screen, "red", player_1.position, player_1.eat_tol) # Player eat range dot
        pygame.draw.circle(screen, "blue", prey_1.coords, 5) # Prey draw dot

    # FPS Counter
    fps_int = fps_counter()
    if fps_int > 55:
        fps_display = text_small.render(f'FPS: {fps_counter()}', True, (255, 255, 255))
        screen.blit(fps_display, (1220, 695))
    else:
        fps_display = text_small.render(f'FPS: {fps_counter()}', True, (255, 0, 0))
        screen.blit(fps_display, (1220, 695))

    # Points text
    points_text = text.render(f'Points: {points}', True, (255, 255, 255))
    screen.blit(points_text, (10, 10))

    # Losing Calories message
    if player_1.size < 65:
        warn_msg = text.render('Eat more!', True, (255, 255, 255))
        screen.blit(warn_msg, (1140, 10))

    # Game over
    if player_1.size < 30:

        # Draw dead player
        player_1.draw_dead()
            
        # Draw prey again over dead player
        prey_1.draw()

        # Display Game Over text
        game_over = text_big.render('Game Over!', True, (255, 255, 255))
        screen.blit(game_over, (screen.get_width() / 2 - 160, screen.get_height() / 2 - 45))

        # Break game loop
        running = False

    # Controls for Player 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_1.position.y -= ((3300 / player_1.size) * player_1.speed) * dt

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_1.position.y += ((3300 / player_1.size) * player_1.speed) * dt

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_1.position.x -= ((3300 / player_1.size) * player_1.speed) * dt

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_1.position.x += ((3300 / player_1.size) * player_1.speed) * dt

    # If player position is at the screen bounds, set it to the edge - 1, to limit going off screen
    if player_1.position.x >= screen.get_width():
        player_1.position.x = screen.get_width() - 1

    if player_1.position.y >= screen.get_height(): 
        player_1.position.y = screen.get_height() - 1

    if player_1.position.x <= 0:
        player_1.position.x = 1

    if player_1.position.y <= 0:
        player_1.position.y = 1

    # User window close and music change
    for event in pygame.event.get():

        # Close window
        if event.type == pygame.QUIT:

            # Draw dead player
            player_1.draw_dead()
            
            # Draw prey again over dead player
            prey_1.draw()

            # Display Game Over text
            game_over = text_big.render('Game Over!', True, (255, 255, 255))
            screen.blit(game_over, (screen.get_width() / 2 - 160, screen.get_height() / 2 - 45))

            # Break game loop
            running = False

        # Change song
        # Forward in list songs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                theme_lenght = 0
                song_index += 1

            # Backward in list songs
            elif event.key == pygame.K_q:
                theme_lenght = 0
                song_index -= 1

    # Theme song counter
    # Removes 1 per second based on the game's FPS
    theme_lenght -= 0.0169

    # When theme_length is less than 0, 
    # select song from the list with the given index
    if theme_lenght <= 0:
        theme_song.stop()
        theme_song = theme_songs[song_index % len_theme_songs]
        theme_song.set_volume(0.4)
        theme_song.play()

        # Reset theme_lenght
        theme_lenght = theme_song.get_length()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

sleep(3)
pygame.quit()