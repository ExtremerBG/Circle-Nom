# Emko/ExtremerBG was here

# Circle Nom Game

# Importing modules
from functions.game_files_loader import *
from functions.game_funcs import *
from classes.hunger_bar import *
from classes.player import *
from classes.prey import *
from math import isclose
from time import sleep
import pygame

# Pygame initialization
pygame.init()

# Screen size, title, icon and fullscreen bool
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Circle Nom")
pygame.display.set_icon(pygame.image.load(resource_path('image/others/icon.ico')))
fullscreen = False

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

# Play random theme song from list
song_index = rand_num(len(theme_songs))
pygame.mixer_music.load(theme_songs[song_index % len(theme_songs)])
pygame.mixer_music.play()

# Set end event for autoplaying
pygame.mixer_music.set_endevent(pygame.USEREVENT)

# Select random background
background_image = background_images[rand_num(len(background_images))]

def game_pause():
    """
    Pauses the game and displays the pause screen.
    Checks for key inputs to resume the game or change screen mode.
    """
    pygame.mixer.music.pause()

    global screen
    global fullscreen
    global running

    paused = True
    while paused:
        for event in pygame.event.get():
            
            # Exit pause screen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.mixer.music.unpause()
                    paused = False

                # Change screen modes
                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((1280, 720))

            # Exit game
            if event.type == pygame.QUIT:
                running = False
                paused = False        

        # Draw screen with player and prey
        screen.blit(background_image, (0, 0))
        player_1.draw()
        prey_1.draw()

        # Draw text stuff
        paused_text = text_big.render('Game Paused', True, (255, 255, 255))
        paused_text_rect = paused_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 30))
        screen.blit(paused_text, paused_text_rect)
        press_text = text.render("Press 'P' to unpause", True, (255, 255, 255))
        press_text_rect = press_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 30))
        screen.blit(press_text, press_text_rect)
        pygame.display.flip()

def game_end():
    """
    Displays the end game screen.
    """
    screen.blit(background_image, (0, 0))
    player_1.draw_dead()

    game_over = text_big.render('Game Over!', True, (255, 255, 255))
    game_over_rect = game_over.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 30))
    screen.blit(game_over, game_over_rect)

    points_final = text.render(f'Points: {points}', True, (255, 255, 255))
    points_final_rect = points_final.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 30))
    screen.blit(points_final, points_final_rect)
    pygame.display.flip()

def music_player(index:int):
    """
    Plays music from the theme_songs list with the given index.
    
    Args:
        index (int): The index of the song to play.
    """
    if type(index) != int:
        raise ValueError("Index must be integer!")
    
    pygame.mixer.music.unload()
    pygame.mixer_music.load(theme_songs[index % len(theme_songs)])
    pygame.mixer.music.play()

# Get random Player image and its dead counterpart
rand_player_image_index = rand_num(len(player_images))
player_image = player_images[rand_player_image_index]
player_image_dead = player_images_dead[rand_player_image_index]

# Declaring player
# 10% Chance of reversing Player/Prey for easter egg
easter = rand_num(10)
if easter == 9:
    
    easter = True
    num = rand_num(len(prey_images))

    # Check if the image is glowing_sandwich
    if num > 0:
        player_1 = Player(prey_images[num], prey_images[num], easter, screen)

    # If it is, set player images to another image, since gif_pygame doesn't support code below
    else:
        player_1 = Player(prey_images[1], prey_images[1], easter, screen)
    
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
    player_1 = Player(player_image, player_image_dead, easter, screen)

# Initial points
points = 0

# Prey spawn timer
spawn = 40 

# Prey despawn timer
despawn = 110

# Player max size
max_size = 110

# Player death size
death_size = 35

# Player max speed
max_speed = 30

# Initial prey declaration
prey_1 = Prey(prey_images, easter, screen)
prey_1.counter = despawn
prey_1.coords_reset()

# Hunger bar declaration
bar = HungerBar(hunger_bar, screen)

# Main game loop
running = True
while running:

    for event in pygame.event.get():
        
        # Game over if user quits window
        if event.type == pygame.QUIT:
            running = False

        # Auto queue next music
        if event.type == pygame.USEREVENT:
            song_index += 1
            music_player(song_index)

        if event.type == pygame.KEYDOWN:

            # Forward in list songs
            if event.key == pygame.K_e:
                song_index += 1
                music_player(song_index)
            # Backward in list songs
            elif event.key == pygame.K_q:
                song_index -= 1
                music_player(song_index)

            # Game pause
            if event.key == pygame.K_p:
                game_pause()

            # Display mode change
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen

                if fullscreen:
                    screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((1280, 720))
                
                # Auto pause after display mode change 
                game_pause()

    # Fill the screen with background image to wipe away anything from last frame
    screen.blit(background_image, (0, 0))

    # Player size decrease
    player_1.size -= 0.2

    # Player eat tolerance change based on easter mode
    if easter == False:
        player_1.eat_tol = player_1.size * 0.9
    else:
        player_1.eat_tol = player_1.size * 1.45

    # Player speed decrease
    if player_1.speed >= 10.1:
        player_1.speed -= 0.1

    # Draw player
    player_1.draw()

    # Print eat text
    if player_1.eat_txt == True:
        player_1.draw_eat_text()

    # Counter for prey spawn
    prey_1.counter += 1
    
    # Create new prey
    if prey_1.counter > spawn and prey_1.created == False:

        prey_1 = Prey(prey_images, easter, screen)
        prey_1.counter = spawn

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

        # Normal eating
        if easter == False:
            # Bonus size, speed & points for sandwich.
            if prey_1.index == 0:
                player_1.size += 40
                player_1.speed += 20
                points += 5
            else:
                player_1.size += 20
                points += 1

        # Different size/speed/points if easter mode is on
        else:
            player_1.size += 16
            player_1.speed += 6
            points += 2

        # Check if player is getting too big
        if player_1.size > max_size:
            player_1.size = max_size

        # Check if player is getting too fast
        if player_1.speed > max_speed:
            player_1.speed = max_speed

        # Play eat random sound
        eat_sounds[rand_num(len(eat_sounds))].play()

        # Sets False because prey is eaten
        prey_1.created = False

        # Reset spawn counter
        prey_1.counter = 0

        # Set eat text to show
        player_1.eat_txt = True

        # Reset coords
        prey_1.coords_reset()

    # Set True to use debug console prints and dots
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

    # FPS Text display
    fps = round(clock.get_fps())
    if fps > 55:
        fps_display = text_small.render(f'FPS: {fps}', True, (255, 255, 255))
        screen.blit(fps_display, (1220, 695))
    else:
        fps_display = text_small.render(f'FPS: {fps}', True, (255, 0, 0))
        screen.blit(fps_display, (1220, 695))

    # Points text display
    points_text = text.render(f'Points: {points}', True, (255, 255, 255))
    screen.blit(points_text, (10, 10))

    # Hunger bar display
    bar.draw(player_1.size, death_size, (1000, 21))
    warn_msg = text.render('Hunger:', True, (255, 255, 255))
    screen.blit(warn_msg, (930, 10))

    # Game over
    if player_1.size < death_size:
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

    # flip() the display to put work on screen
    pygame.display.flip()

    # Limits FPS to 60
    dt = clock.tick(60) / 1000

# Draw game end screen
game_end()
sleep(3)
pygame.quit()