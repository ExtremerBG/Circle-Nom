# Emko/ExtremerBG was here

# Circle Nom Game

# Importing modules
import pygame
import random
import time
import math
import sys
import os

# Function for resource path
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Pygame initialization
pygame.init()

# Screen size, title and icon
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Emko's Circle Nom Game")
pygame.display.set_icon(pygame.image.load(resource_path('icon.ico')))

# Clock for framerate
clock = pygame.time.Clock()

# Game loop
running = True

# Player position
dt = 0

# Spawn position at center of screen
player_pos = pygame.Vector2(screen.get_width() / 2 - 128, screen.get_height() / 2 - 128)

# font setup
pygame.font.init()
text = pygame.font.SysFont('Comic Sans MS', 30)
text_big = pygame.font.SysFont('Comic Sans MS', 60)
text_small = pygame.font.SysFont('Comic Sans MS', 15)

# Sound setup
pygame.mixer.init()
eat_sound1 = pygame.mixer.Sound(resource_path('nom_1.wav'))
eat_sound2 = pygame.mixer.Sound(resource_path('nom_2.wav'))
eat_sound3 = pygame.mixer.Sound(resource_path('nom_3.wav'))
eat_sound4 = pygame.mixer.Sound(resource_path('nom_4.wav'))
eat_sound5 = pygame.mixer.Sound(resource_path('nom_5.wav'))
theme_song = pygame.mixer.Sound(resource_path('theme_song.wav'))

# List of eat sounds for random selection
eat_sounds = [eat_sound1, eat_sound2, eat_sound3, eat_sound4, eat_sound5]

# Play theme song, set volume and get length of song
theme_song.play()
theme_song.set_volume(0.4)
theme_lenght = theme_song.get_length()

# Load Player images
player_image = pygame.image.load(resource_path('player_image_1.png'))
imagerect = player_image.get_rect()
player_image_og = pygame.image.load(resource_path('player_image_1.png'))
imagerect = player_image_og.get_rect()

# Load prey images
prey_image_0 = pygame.image.load(resource_path('prey_image_0.png')) # sandwitch which gives bonus points
prey_image_1 = pygame.image.load(resource_path('prey_image_1.png'))
prey_image_2 = pygame.image.load(resource_path('prey_image_2.png'))
prey_image_3 = pygame.image.load(resource_path('prey_image_3.png'))
prey_image_4 = pygame.image.load(resource_path('prey_image_4.png'))
prey_image_5 = pygame.image.load(resource_path('prey_image_5.png'))

# List of prey images for random selection
prey_images = [prey_image_0, prey_image_1, prey_image_2, prey_image_3, prey_image_4, prey_image_5]
for image in prey_images:
    imagerect = image.get_rect()

# Load background image
background_image = pygame.image.load(resource_path('background_image_1.jpg'))

# Easter egg 10% chance of reversing player/prey
easter = random.randint(1, 10)
if easter == 10:

    player_image = prey_images[random.randint(0, len(prey_images)-1)]
    prey_image = pygame.transform.smoothscale(player_image_og, (64, 64))
    player_image_og = player_image
    prey_images = [prey_image]

# Function for random screen position
# offset to prevent nums close to the edge
def rand_screen_pos():
    
    # Screen size: width 1280 x height 720
    # Bias for return positions
    # 80% Chance to return closer to edge
    # 20% chance to return closer to middle

    bias_edge = random.randrange(1, 100)

    # Return closer to top left
    if bias_edge <= 20:
        # Debug print
        # print("TOP LEFT")
        return random.randint(64, 448), random.randint(36, 288)
    
    # Return closer to bottom right
    elif bias_edge > 20 and bias_edge <= 40:
        # Debug print
        # print("BOTTOM RIGHT")
        return random.randint(832, 1216), random.randint(432, 648)
    
    # Return closer to bottom left
    elif bias_edge > 40 and bias_edge <= 60:
        # Debug print
        # print("BOTTOM LEFT")
        return random.randint(64, 448), random.randint(432, 648)
    
    # Return closer to top right
    elif bias_edge > 60 and bias_edge <= 80:
        # Debug print
        # print("TOP RIGHT")
        return random.randint(832, 1216), random.randint(36, 288)

    # Return closer to center
    else:
        # Debug print
        # print("CENTER")
        return random.randint(480, 960), random.randint(270, 540)

# Function for random rotation
def rand_rotation():
    return random.randint(0, 360)

# Function for rotating image
def image_rotate(image, angle):
    return pygame.transform.rotate(image, angle)

# Function for random prey image
def rand_prey_img():
    return random.randint(0, len(prey_images)-1)

# Function for displaying FPS
def fps_counter():
    fps = int(clock.get_fps())
    return fps

# Initial Player circle size
player_size = 90
player_scale = [player_size, player_size]

# Initial prey spawn counter
prey_spawn_counter = 0

# Initial points
points = 0

# Initial prey spawn position
prey_spawn_pos = rand_screen_pos()

# Inital prey rotation int
prey_angle = rand_rotation()

# Initial prey image
prey_image_index = rand_prey_img()

# Is prey spawned
is_prey_spawned = False

# Is prey created
is_prey_created = False

# Prey spawn timer
spawn = 30 

# Prey despawn timer
despawn = 90

# Game Loop
while running:

    # Counter for prey spawn
    prey_spawn_counter += 1

    # Theme song counter
    # Removes 1 per second based on the game's FPS
    theme_lenght -= 0.01667

    # Debug print
    # print(theme_lenght)

    # Eating tolerance
    eat_tolerance = player_size * 1.75

    # When theme_length is less than 0, play theme song again
    if theme_lenght <= 0:
        theme_song.play()

        # Reset theme_lenght
        theme_lenght = theme_song.get_length()

    # poll for events
    # pygame.QUIT event means the user clicked X to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with background image to wipe away anything from last frame
    # screen.fill("black")
    screen.blit(background_image, (0,0))

    # Background draws over prey, so it must be drawn again
    is_prey_spawned = False
        
    # If prey is NOT spawned and NOT Created
    if is_prey_spawned == False and is_prey_created == False and prey_spawn_counter > spawn:

         # Sets created to True
        is_prey_created = True

         # New random position for prey spawn
        prey_spawn_pos = rand_screen_pos()

        # New random rotation for prey spawn
        prey_angle = rand_rotation()

        # New random prey image index
        prey_image_index = rand_prey_img()
            
        # Selects prey_image
        prey_image = prey_images[prey_image_index]

        # Debug print
        # print(f"PREY CREATED at X: {prey_spawn_pos[0]} Y: {prey_spawn_pos[1]}")

    # If prey is spawned maitain image for every frame
    if is_prey_spawned == False and is_prey_created == True and prey_spawn_counter > spawn:

        # Sets prey image
        screen.blit(image_rotate(prey_image, prey_angle), prey_spawn_pos - pygame.Vector2(prey_image.get_width() / 2, prey_image.get_height() / 2))

        is_prey_spawned = True
        
        # Debug print
        # print("PREY IMAGE SET")
    
    # Despawn prey
    if prey_spawn_counter > despawn and is_prey_spawned == True and is_prey_created == True: 
        
        # Set spawn/despawn counter to 0
        prey_spawn_counter = 0

        # Sets False so new prey can be generated
        is_prey_created = False

        # Sets False because prey is despawned
        is_prey_spawned = False

        # Remove points for missing prey
        if points > 0:
            points -= 1

        # Debug print
        # print("PREY DESPAWNED")

    # Eating prey
    if math.isclose(player_pos.x, prey_spawn_pos[0], abs_tol=eat_tolerance) and math.isclose(player_pos.y, prey_spawn_pos[1], abs_tol=eat_tolerance) and is_prey_spawned == True and is_prey_created == True:

        # Bonus size for sandwitch
        if  prey_image_index == 0:
            player_size += 40
        else:
            player_size += 20

        # Check if player is getting too big
        if player_size > 90:
            player_size = 90

        if prey_image_index == 0:
            # bonus points for sandwitch
            points += 5
        else:
            points += 1

        # Play random sound
        eat_sounds[random.randint(0, 4)].play()
        prey_image_index = rand_prey_img()

        # Sets False so new prey can be generated
        is_prey_created = False
        
        # Sets False because prey is eaten
        is_prey_spawned = False

        # Reset spawn counter
        prey_spawn_counter = 0

        # Debug message
        # print("PREY EATEN")

    # Player circle decrease
    player_size -= 0.24
    player_scale[0] = player_size * 3
    player_scale[1] = player_size * 3
    
    # Draw Player
    player_image = pygame.transform.smoothscale(player_image_og, player_scale)
    screen.blit(player_image, player_pos - pygame.Vector2(player_image.get_width() / 2, player_image.get_height() / 2))
    
    # Debug position dots
    # pygame.draw.circle(screen, "red", player_pos, 10) # Player draw dot
    # pygame.draw.circle(screen, "blue", prey_spawn_pos, 5) # Prey draw dot

    # Debug FPS
    fps_int = fps_counter()
    if fps_int > 55:
        fps_display = text_small.render(f'FPS: {fps_counter()}', True, (255, 255, 255))
        screen.blit(fps_display, (1220, 695))
    else:
        fps_display = text_small.render(f'FPS: {fps_counter()}', True, (255, 0, 0))
        screen.blit(fps_display, (1220, 695))

    # Debug variables
    # print(f"[DEBUG] Player Pos-> X: {player_pos.x:1f}, Y: {player_pos.y:1f}, Prey Pos-> X: {prey_spawn_pos[0]:1f}, Y: {prey_spawn_pos[1]:1f}, Prey Counter: {prey_spawn_counter:1f}, Is_Prey_Spawned: {is_prey_spawned}, Abs Tol: {eat_tolerance:1f}, Player Size: {player_size:1f}")

    # Points text
    points_text = text.render(f'Points: {points}', True, (255, 255, 255))
    screen.blit(points_text, (10, 10))

    # Losing Calories message
    if player_size < 50:
        circle_big = text.render('Eat more!', True, (255, 255, 255))
        screen.blit(circle_big, (1140, 10))

    # Game over
    if player_size < 20:
        game_over = text_big.render('Game Over!', True, (255, 255, 255))
        screen.blit(game_over, (screen.get_width() / 2 - 160, screen.get_height() / 2 - 45))
        running = False

    # Controls for Player circle
    # < is used to prevent player from going off screen
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_pos.x < screen.get_width() and player_pos.y < screen.get_height():
        player_pos.y -= (3000 / player_size * 10) * dt
    if keys[pygame.K_s] and player_pos.x < screen.get_width() and player_pos.y < screen.get_height():
        player_pos.y += (3000 / player_size * 10) * dt
    if keys[pygame.K_a] and player_pos.x < screen.get_width() and player_pos.y < screen.get_height():
        player_pos.x -= (3000 / player_size * 10) * dt
    if keys[pygame.K_d] and player_pos.x < screen.get_width() and player_pos.y < screen.get_height():
        player_pos.x += (3000 / player_size * 10) * dt
    
    # If player position is off screen, set it to the edge - 1, otherwise it will go off screen
    if player_pos.x >= screen.get_width():
        player_pos.x = screen.get_width() - 1

    if player_pos.y >= screen.get_height(): 
        player_pos.y = screen.get_height() - 1

    if player_pos.x <= 0:
        player_pos.x = 1

    if player_pos.y <= 0:
        player_pos.y = 1

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

time.sleep(3)
pygame.quit()