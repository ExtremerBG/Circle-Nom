# Emko/ExtremerBG was here

# Circle Nom Game

# Importing modules
from functions.game_files_loader import *
from functions.game_funcs import *
from classes.health_bar import *
from classes.dagger import *
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

def eat_prey(player:Player, prey:Prey, easter:bool, points:int):
    """
    Checks if player is near a prey object.

    Args:
        player (class Player): The player to check with.
        prey (class Prey): The prey to check with.
        easter (bool): Bool if easter mode is on.
        points (int): Current points.
    
    Returns updated points.
    """
    if isclose(player.eat_pos.x, prey.coords[0], abs_tol=player.eat_tol) and isclose(player.eat_pos.y, prey.coords[1], abs_tol=player.eat_tol):
        # Normal eating
        if not easter:
            # Bonus size, speed & points for sandwich.
            if prey.index == 0:
                player.size += 20
                player.speed += 15
                points += 3
            else:
                player.size += 12
                player.speed += 5
                points += 1
        # Easter eating
        else:
            player.size += 10
            player.speed += 7
            points += 2

        # Play eat random sound
        eat_sounds[rand_num(len(eat_sounds))].play()

        # Set eat text to show & remove ow
        player.nom_txt_counter = 30
        player.ow_txt_counter = 0

        # Reset prey
        prey.reset_prey()

    return points

# Get random Player image and its dead counterpart
rand_player_image_index = rand_num(len(player_images))
player_image = player_images[rand_player_image_index]
player_image_dead = player_images_dead[rand_player_image_index]

# Declaring player
# 10% Chance of reversing Player/Prey for easter egg
easter = rand_num(9)
if easter == 9:
    # Turn on easter mode
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

# Prey declaration
prey_1 = Prey(prey_images, screen)
prey_2 = Prey(prey_images, screen)

# Health bar declaration
bar = HealthBar(hunger_bar, screen)

# Dagger declaration
dagger_1 = Dagger(dagger_images, screen)

# Initial points
points = 0

# Pause - Skips over entire game loop, except the event checker.
paused = False

# Main game loop
running = True

while running:

    # --------------------------------------------------------------------------------------------
    # EVENT CHECKER - MUST ALWAYS RUN.
    for event in pygame.event.get():
            
        # QUIT WINDOW / ALT + F4
        if event.type == pygame.QUIT:
            running = False

        # Music auto queue
        if event.type == pygame.USEREVENT:
            song_index += 1
            music_player(song_index)

        # Key event checker - part of EVENT CHECKER
        if event.type == pygame.KEYDOWN:

            # Game pause/unpause
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

            # Display mode change - always works
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen

                if fullscreen:
                    screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((1280, 720))
                    
                # Auto pause when display mode changed
                paused = True
                pygame.mixer.music.pause()

            # Music changer - works only when game is not paused
            if not paused:
                # Forward in list songs
                if event.key == pygame.K_e:
                    song_index += 1
                    music_player(song_index)
                # Backward in list songs
                elif event.key == pygame.K_q:
                    song_index -= 1
                    music_player(song_index)
    # --------------------------------------------------------------------------------------------

    # ACTUAL GAME LOOP
    if not paused:         
        # Fill the screen with background image to wipe away anything from last frame
        screen.blit(background_image, (0, 0))

        # Draw player
        player_1.draw()

        # Draw prey 1
        prey_1.draw()
        
        # Draw prey 2
        prey_2.draw()
            
        # Draw dagger
        dagger_1.draw()

        # Play dagger sound if its on screen
        if 0 <= dagger_1.coords[0] <= screen.get_width() and 0 <= dagger_1.coords[1] <= screen.get_height():
            dagger_1.play_sound()

        # Player decrease
        player_1.speed -= 0.1

        # Player size decrease
        player_1.size -= 0.15

        # # Dagger hit
        if isclose(player_1.hit_pos.x, dagger_1.coords[0], abs_tol=player_1.hit_tol) and isclose(player_1.hit_pos.y, dagger_1.coords[1], abs_tol=player_1.hit_tol):
            # Bigger penalty if its a flaming dagger
            if dagger_1.flame == True:
                player_1.size -= 15
                player_1.speed -= 5
            else:
                player_1.size -= 10

            # Set ow text to show & remove eat
            player_1.ow_txt_counter = 30
            player_1.nom_txt_counter = 0

            # Reset dagger
            dagger_1.reset_dagger()

            # if player is hit: dagger spawn has a grace period
            dagger_1.grace_spawn(randint(60, 90))

            # Play random sound 
            hit_sounds[rand_num(len(hit_sounds))].play()

        # Player draw Ow! text & Draw hit red overlay
        if player_1.ow_txt_counter > 0:
            player_1.draw_text("Ow!")
            if not easter:
                player_1.draw_hit()

        # Trying to eat prey_1 and prey_2
        points = eat_prey(player_1, prey_1, easter, points)
        points = eat_prey(player_1, prey_2, easter, points)

        # Player draw Nom! text
        if player_1.nom_txt_counter > 0:
            player_1.draw_text("Nom!")

        # Game over
        if player_1.size <= player_1.min_size:
            running = False

        # Set True to use Player debug console prints and dots
        if False:
            print(f"player_1_pos X: {player_1.position.x:.2f} Y: {player_1.position.y:.2f}",end=" || ") 

            print(f"player_1.eat_tol: {player_1.eat_tol:.2f}",end=" || ")

            print(f"player_1.hit_tol: {player_1.hit_tol:.2f}",end=" || ")

            print(f"player_1.size: {player_1.size:.2f}", end=" || ")

            print(f"player_1.speed: {player_1.speed:.2f}")

            # Player dots
            pygame.draw.circle(screen, "green", player_1.hit_pos, player_1.hit_tol) # Player 1 hit range dot
            pygame.draw.circle(screen, "red", player_1.eat_pos, player_1.eat_tol) # Player 1 eat range dot

        # Set True to use Prey debug console prints and dot
        if False:
            print(f"prey_1_pos X: {prey_1.coords[0]} Y: {prey_1.coords[1]}",end=" | ")

            print(f"prey_1.counter: {prey_1.counter}",end=" ||| ")

            print(f"prey_2_pos X: {prey_2.coords[0]} Y: {prey_2.coords[1]}",end=" | ")

            print(f"prey_2.counter: {prey_2.counter}")

            # Prey position dots
            pygame.draw.circle(screen, "blue", prey_1.coords, 5) # Prey 1
            pygame.draw.circle(screen, "blue", prey_2.coords, 5) # Prey 2

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

        # Song name display
        song_name = text_small.render(f"{get_song_name(song_index, theme_songs)}", True, (255, 255, 255))
        screen.blit(song_name, (10, 695))

        # Health bar display
        bar.draw(player_1.size, player_1.max_size, player_1.min_size, (1000, 21))
        health_txt = text.render('Health:', True, (255, 255, 255))
        screen.blit(health_txt, (930, 10))

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

    # -------------------------------------------------------------------------------------------- 
    # PAUSE SCREEN
    else:
        # Screen and player
        screen.blit(background_image, (0, 0))
        player_1.draw()

        # Game paused text
        paused_text = text_big.render('Game Paused', True, (255, 255, 255))
        paused_text_rect = paused_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 30))
        screen.blit(paused_text, paused_text_rect)

        # Press 'P' text
        press_text = text.render("Press 'P' to unpause", True, (255, 255, 255))
        press_text_rect = press_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 30))
        screen.blit(press_text, press_text_rect)
        pygame.display.flip()

    # flip() the display to put work on screen
    pygame.display.flip()

    # Limits FPS to 60
    dt = clock.tick(60) / 1000

# Draw game end screen
# screen and player
screen.blit(background_image, (0, 0))
player_1.draw_dead()

# Game over text
game_over = text_big.render('Game Over!', True, (255, 255, 255))
game_over_rect = game_over.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 30))
screen.blit(game_over, game_over_rect)

# Points txt
points_final = text.render(f'Points: {points}', True, (255, 255, 255))
points_final_rect = points_final.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 30))
screen.blit(points_final, points_final_rect)
pygame.display.flip()

sleep(3)
pygame.quit()