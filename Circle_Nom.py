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

# Spawn position at center of screen
player_pos = pygame.Vector2(screen.get_width() / 2 - 128, screen.get_height() / 2 - 128)

# Font setup
pygame.font.init()
text = pygame.font.SysFont('Comic Sans MS', 30)
text_big = pygame.font.SysFont('Comic Sans MS', 60)
text_small = pygame.font.SysFont('Comic Sans MS', 15)

# SFX setup
pygame.mixer.init()
eat_sound1 = pygame.mixer.Sound(resource_path('sounds/nom_1.wav'))
eat_sound2 = pygame.mixer.Sound(resource_path('sounds/nom_2.wav'))
eat_sound3 = pygame.mixer.Sound(resource_path('sounds/nom_3.wav'))
eat_sound4 = pygame.mixer.Sound(resource_path('sounds/nom_4.wav'))
eat_sound5 = pygame.mixer.Sound(resource_path('sounds/nom_5.wav'))

# List of eat sounds for random selection + lenght
eat_sounds = [eat_sound1, eat_sound2, eat_sound3, eat_sound4, eat_sound5]
len_eat_sounds = len(eat_sounds)

# Theme song setup
theme_song_1 = pygame.mixer.Sound(resource_path('sounds/theme_song_1.wav'))
theme_song_2 = pygame.mixer.Sound(resource_path('sounds/theme_song_2.wav'))
theme_song_3 = pygame.mixer.Sound(resource_path('sounds/theme_song_3.wav'))
theme_song_4 = pygame.mixer.Sound(resource_path('sounds/theme_song_4.wav'))
theme_song_5 = pygame.mixer.Sound(resource_path('sounds/theme_song_5.wav'))

# List of theme songs + lenght
theme_songs = [theme_song_1, theme_song_2, theme_song_3, theme_song_4, theme_song_5]
len_theme_songs = len(theme_songs)

# Play random theme song from list, set volume and get length of song
theme_song = theme_songs[rand_num(len_theme_songs)]
theme_lenght = theme_song.get_length()
theme_song.set_volume(0.4)
theme_song.play()

# Load Player images
player_image_1 = pygame.image.load(resource_path('images/player_image_1.png'))
player_image_2 = pygame.image.load(resource_path('images/player_image_2.png'))
player_image_3 = pygame.image.load(resource_path('images/player_image_3.png'))

# Load dead Player images
player_image_1_dead = pygame.image.load(resource_path('images/player_image_1_dead.png'))
player_image_2_dead = pygame.image.load(resource_path('images/player_image_2_dead.png'))
player_image_3_dead = pygame.image.load(resource_path('images/player_image_3_dead.png'))

# Make lists of both
player_images = [player_image_1, player_image_2, player_image_3]
player_images_dead = [player_image_1_dead, player_image_2_dead, player_image_3_dead]

# Get lenght of both
len_player_images = len(player_images)
len_player_images_dead = len(player_images_dead)

# Print warning message if lengths of player lists are different
if len_player_images != len_player_images_dead:
    for i in range(10):
        print("PLAYER IMAGES LISTS DIFFERENT LENGHTS!!!")

# Get random Player image and random dead Player image
rand_player_image_index = rand_num(len_player_images)
player_image = player_images[rand_player_image_index]
player_image_dead = player_images_dead[rand_player_image_index]

# Store backup Player image, so no loss of quality occurs with pygame.transform
player_image_og = player_image

# Load prey images
# prey_image_0 = pygame.image.load(resource_path('images/prey_image_0.png')) # sandwich which gives bonus points
# prey_image_0 is now prey_glowing_sandwich, when prey_image_index = 0, game loads it instead
prey_image_1 = pygame.image.load(resource_path('images/prey_image_1.png'))
prey_image_2 = pygame.image.load(resource_path('images/prey_image_2.png'))
prey_image_3 = pygame.image.load(resource_path('images/prey_image_3.png'))
prey_image_4 = pygame.image.load(resource_path('images/prey_image_4.png'))
prey_image_5 = pygame.image.load(resource_path('images/prey_image_5.png'))
prey_image_6 = pygame.image.load(resource_path('images/prey_image_6.png'))
prey_image_7 = pygame.image.load(resource_path('images/prey_image_7.png'))
prey_image_8 = pygame.image.load(resource_path('images/prey_image_8.png'))
prey_image_9 = pygame.image.load(resource_path('images/prey_image_9.png'))
prey_image_10 = pygame.image.load(resource_path('images/prey_image_10.png'))

# APNG Glowing sandwich prey load - Uses gif_pygame !
prey_glowing_sandwich = gif_pygame.load(resource_path('images/glowing_sandwich.png'))

# List of prey images from pygame ONLY
prey_images = [
    prey_image_1, prey_image_2, prey_image_3, prey_image_4, prey_image_5,
    prey_image_6, prey_image_7, prey_image_8, prey_image_9, prey_image_10
]
len_prey_images = len(prey_images)

# Load background images
background_image_1 = pygame.image.load(resource_path('images/background_image_1.jpg'))
background_image_2 = pygame.image.load(resource_path('images/background_image_2.jpg'))
background_image_3 = pygame.image.load(resource_path('images/background_image_3.jpg'))

# List of backgrounds for random selection + lenght
background_images = [background_image_1, background_image_2, background_image_3]
len_background_images = len(background_images)

# Selection from background list
background_image = background_images[rand_num(len_background_images)]

# Function for displaying FPS
def fps_counter():
    fps = int(clock.get_fps())
    return fps

# Easter egg 10% chance of reversing player/prey
easter = rand_num(10)
if easter == 9:
    
    easter = True
    # Sets player image to random prey image
    player_image = prey_images[rand_num(len_prey_images)]

    # Creates backup for pygame.transform
    player_image_og = player_image

    # Sets player dead image to be the same as player image
    player_image_dead = player_image

    # Resets prey list
    prey_images = []

    # Resize and add player images to prey list
    for player_image in player_images:
        
        prey_image = pygame.transform.smoothscale(player_image, (64, 64))
        prey_images.append(prey_image)

else:
    easter = False

# Set len of prey images again after easter.
len_prey_images = len(prey_images)

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
prey_angle = rand_num(360)

# Initial prey image
prey_image_index = rand_num(len_prey_images)

# Is prey spawned
is_prey_spawned = False

# Is prey created
is_prey_generated = False

# Prey spawn timer
spawn = 30 

# Prey despawn timer
despawn = 90

# Eat text boolean
eat_text = False

# Player speed multiplier
player_speed = 10

# Game Loop
while running:

    # Counter for prey spawn
    prey_spawn_counter += 1

    # Theme song counter
    # Removes 1 per second based on the game's FPS
    theme_lenght -= 0.0169

    # Debug print
    # print(theme_lenght)

    # Eating tolerance
    eat_tolerance = player_size * 1.75

    # When theme_length is less than 0, 
    # select a random song from list, set volume and play
    if theme_lenght <= 0:
        theme_song = theme_songs[rand_num(len_theme_songs)]
        theme_song.set_volume(0.4)
        theme_song.play()

        # Reset theme_lenght
        theme_lenght = theme_song.get_length()

    # fill the screen with background image to wipe away anything from last frame
    # screen.fill("black")
    screen.blit(background_image, (0, 0))

    # Background draws over prey, so it must be drawn again
    is_prey_spawned = False
        
    # If prey is NOT spawned and NOT Created
    if is_prey_spawned == False and is_prey_generated == False and prey_spawn_counter > spawn:

         # Sets created to True
        is_prey_generated = True

         # New random position for prey spawn
        prey_spawn_pos = rand_screen_pos()

        # New random rotation for prey spawn
        prey_angle = rand_num(360)

        # New random prey image index
        prey_image_index = rand_num(len_prey_images)
            
        # Selects prey_image
        prey_image = prey_images[prey_image_index]

        eat_text = False

        # Debug print
        # print(f"PREY CREATED at X: {prey_spawn_pos[0]} Y: {prey_spawn_pos[1]} with index {prey_image_index}")

    # If prey is spawned maitain image for every frame
    if is_prey_spawned == False and is_prey_generated == True and prey_spawn_counter > spawn:

        if prey_image_index > 0 and easter == False:

            # Render normal prey
            screen.blit(image_rotate(prey_image, prey_angle), prey_spawn_pos - pygame.Vector2(prey_image.get_width() / 2, prey_image.get_height() / 2))

        elif prey_image_index == 0 and easter == False:

            # Render sandwich
            prey_glowing_sandwich.render(screen, prey_spawn_pos - pygame.Vector2(prey_glowing_sandwich.get_width() / 2, prey_glowing_sandwich.get_height() / 2))
        else:

            # If easter mode is active, render player as prey
            screen.blit(image_rotate(prey_image, prey_angle), prey_spawn_pos - pygame.Vector2(prey_image.get_width() / 2, prey_image.get_height() / 2))

        # Prey is spawned
        is_prey_spawned = True
        
        # Debug print
        # print("PREY IMAGE SET")
    
    # Despawn prey
    if prey_spawn_counter > despawn and is_prey_spawned == True and is_prey_generated == True: 
        
        # Set spawn/despawn counter to 0
        prey_spawn_counter = 0

        # Sets False so new prey can be generated
        is_prey_generated = False

        # Sets False because prey is despawned
        is_prey_spawned = False

        # Remove points for missing prey
        if points > 0:
            points -= 1

        # Remove eat text
        eat_text = False

        # Debug print
        # print("PREY DESPAWNED")

    # Eating prey
    if isclose(player_pos.x, prey_spawn_pos[0], abs_tol=eat_tolerance) and isclose(player_pos.y, prey_spawn_pos[1], abs_tol=eat_tolerance) and is_prey_spawned == True and is_prey_generated == True:

        if easter == False:
            # Bonus size & speed for sandwich.
            if prey_image_index == 0:
                player_size += 40
                player_speed += 20
            else:
                player_size += 20

            # bonus points for sandwich
            if prey_image_index == 0:
                points += 5
            else:
                points += 1

        # Different size/speed/points if easter is on
        else:
            player_size += 15
            player_speed += 8
            points += 2

        # Check if player is getting too big
        if player_size > 100:
            player_size = 100

        # Check if player is getting too fast
        if player_speed > 30:
            player_speed = 30

        # Play random sound
        eat_sounds[rand_num(len_eat_sounds)].play()

        # Sets False so new prey can be generated
        is_prey_generated = False
        
        # Sets False because prey is eaten
        is_prey_spawned = False

        # Reset spawn counter
        prey_spawn_counter = 0

        # Debug message
        # print("PREY EATEN")

        # Set eat text to show
        eat_text = True

    # Player circle decrease
    player_size -= 0.24
    player_scale[0] = player_size * 3
    player_scale[1] = player_size * 3

    # Player speed decrease
    if player_speed > 10:
        player_speed -= 0.1
    
    # Draw Player
    player_image = pygame.transform.smoothscale(player_image_og, player_scale)
    screen.blit(player_image, player_pos - pygame.Vector2(player_image.get_width() / 2, player_image.get_height() / 2))

    # Print eat text
    if eat_text == True:
        x, y  = player_pos
        x -= 30
        y -= eat_tolerance + 30
        nom_text = text.render(f"Nom!", True, (255, 255, 255))
        screen.blit(nom_text, (x, y))

    # Set True to use debug prints and dots
    if  False:
        # Print player position
        print(f"player_pos X: {player_pos.x:.2f} Y: {player_pos.y:.2f}",end=" || ")  

        # Print prey position  
        print(f"prey_pos X: {prey_spawn_pos[0]} Y: {prey_spawn_pos[1]}",end=" || ")

        # Print prey spawn counter
        print(f"prey_spawn_counter: {prey_spawn_counter}",end=" || ")

        # Print if prey is generated (new position, image, rotation)
        print(f"is_prey_generated: {is_prey_generated}",end=" || ")

        # Print if prey is spawned (visible on screen)
        print(f"is_prey_spawned: {is_prey_spawned}",end=" || ")

        # Print eat tolerance (range for eating prey)
        print(f"eat_tolerance: {eat_tolerance:.2f}",end=" || ")

        # Print player_size
        print(f"player_size: {player_size:.2f}", end=" || ")

        # Print player speed multiplier
        print(f"player_speed: {player_speed:.2f}")

        # Debug position dots
        pygame.draw.circle(screen, "red", player_pos, 10) # Player eat range dot
        pygame.draw.circle(screen, "blue", prey_spawn_pos, 5) # Prey draw dot

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
    if player_size < 60:
        circle_big = text.render('Eat more!', True, (255, 255, 255))
        screen.blit(circle_big, (1140, 10))

    # Game over
    if player_size < 25:

        # Change player pic to the dead one
        player_image_dead = pygame.transform.smoothscale(player_image_dead, player_scale)
        screen.blit(player_image_dead, player_pos - pygame.Vector2(player_image.get_width() / 2, player_image.get_height() / 2))

        # Display Game Over text
        game_over = text_big.render('Game Over!', True, (255, 255, 255))
        screen.blit(game_over, (screen.get_width() / 2 - 160, screen.get_height() / 2 - 45))

        # Break game loop
        running = False

     # pygame.QUIT event means the user clicked X to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            # Change player pic to the dead one
            player_image_dead = pygame.transform.smoothscale(player_image_dead, player_scale)
            screen.blit(player_image_dead, player_pos - pygame.Vector2(player_image.get_width() / 2, player_image.get_height() / 2))

            # Display Game Over text
            game_over = text_big.render('Game Over!', True, (255, 255, 255))
            screen.blit(game_over, (screen.get_width() / 2 - 160, screen.get_height() / 2 - 45))

            # Break game loop
            running = False

    # Controls for Player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_pos.x < screen.get_width():
        player_pos.y -= ((3000 / player_size) * player_speed) * dt
    if keys[pygame.K_s] and player_pos.x < screen.get_width():
        player_pos.y += ((3000 / player_size) * player_speed) * dt
    if keys[pygame.K_a] and player_pos.x < screen.get_width():
        player_pos.x -= ((3000 / player_size) * player_speed) * dt
    if keys[pygame.K_d] and player_pos.x < screen.get_width():
        player_pos.x += ((3000 / player_size) * player_speed) * dt
    
    # If player position is at the screen bounds, set it to the edge - 1, to limit going off screen
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

sleep(3)
pygame.quit()