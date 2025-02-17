# Emko/ExtremerBG was here

# Circle Nom Game

# Importing modules
from functions.game_funcs import *
from classes.health_bar import *
from classes.dagger import *
from classes.player import *
from classes.prey import *
from math import isclose
from time import sleep
import pygame
import sys

class CircleNom():

    def __init__(self, screen, difficulty, play_mode, eat_sounds, 
                 theme_songs, player_images, player_image_index, 
                 player_images_dead, prey_images, prey_aura,
                 background_image, health_bar, dagger_images, 
                 dagger_sounds, hit_sounds):
        
        self.screen:pygame.Surface = screen
        self.difficulty:int = difficulty
        self.play_mode:int = play_mode
        self.eat_sounds:list[pygame.Sound] = eat_sounds
        self.theme_songs:list = theme_songs
        self.player_image_index:int = player_image_index
        self.player_images:list[pygame.Surface] = player_images
        self.player_images_dead:list[pygame.Surface] = player_images_dead
        self.prey_aura:pygame.Surface = prey_aura
        self.prey_images:list[pygame.Surface] = prey_images
        self.background_image:pygame.Surface = background_image
        self.health_bar:list[pygame.Surface] = health_bar
        self.dagger_images:list[pygame.Surface] = dagger_images
        self.dagger_sounds:list[pygame.Sound] = dagger_sounds
        self.hit_sounds:list[pygame.Sound] = hit_sounds

    def start(self):

        # Pygame initialization
        pygame.init()

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
        song_index = rand_num(len(self.theme_songs))
        pygame.mixer_music.load(self.theme_songs[song_index % len(self.theme_songs)])
        pygame.mixer_music.play()

        # Set end event for autoplaying
        pygame.mixer_music.set_endevent(pygame.USEREVENT)

        def music_player(index:int):
            """
            Plays music from the theme_songs list with the given index.
            
            Args:
                index (int): The index of the song to play.
            """
            if type(index) != int:
                raise ValueError("Index must be integer!")
            
            pygame.mixer.music.unload()
            pygame.mixer.music.load(self.theme_songs[index % len(self.theme_songs)])
            pygame.mixer.music.play()

        def eat_prey(player:Player, prey:Prey, easter:bool):
            """
            Checks if player is near a prey object.

            Args:
                player (class Player): The player to check with.
                prey (class Prey): The prey to check with.
                easter (bool): Bool if easter mode is on.
            """
            if isclose(player.eat_pos.x, prey.coords[0], abs_tol=player.eat_tol) and isclose(player.eat_pos.y, prey.coords[1], abs_tol=player.eat_tol):

                # Normal eating
                if not easter:

                    # Bonus size, speed & points for aura'd food
                    if prey.aura:
                        player.size += 20
                        player.speed += 15
                        player.points += 3
                    else:
                        player.size += 12
                        player.speed += 5
                        player.points += 1

                # Easter eating
                else:

                    # Bonus points for aura'd food
                    if prey.aura:
                        player.size += 16
                        player.speed += 10
                        player.points += 2
                    else:
                        player.size += 8
                        player.speed += 5
                        player.points += 1

                # Play eat random sound
                self.eat_sounds[rand_num(len(self.eat_sounds))].play()

                # Set eat text to show & remove ow
                player.nom_txt_counter = 30
                player.ow_txt_counter = 0

                # Reset prey
                prey.reset_prey()
        
        def dagger_hit(player:Player, dagger:Dagger):
            """
            Checks if player is hit by a dagger object.
            Args:
                player (class Player): The player to check with.
                dagger (class Dagger): The dagger to check with.
            """

            if isclose(player.hit_pos.x, dagger.coords[0], abs_tol=player.hit_tol) and isclose(player.hit_pos.y, dagger.coords[1], abs_tol=player.hit_tol):

                # Bigger penalty if its a flaming dagger
                if dagger.flame == True:
                    player.size -= 15
                    player.speed -= 5
                else:
                    player.size -= 10

                # Set ow text to show & remove eat
                player.ow_txt_counter = 30
                player.nom_txt_counter = 0

                # Reset dagger
                dagger.reset_dagger()

                # if player is hit: dagger spawn has a grace period
                dagger.grace_spawn(randint(60, 90))

                # Play random sound 
                self.hit_sounds[rand_num(len(self.hit_sounds))].play()

        # Check if play_mode is valid
        if self.play_mode not in [0, 1]:
            raise ValueError("Invalid play mode!\n 0 - Singleplayer\n 1 - Multiplayer")
        
        # Difficulty selector - Adjusts prey despawn timers:
        # 0 - Easy
        # 1 - Medium
        # 2 - Hard
        if self.difficulty == 0:
            Prey.despawn = 120
            grace_period = 240
        elif self.difficulty == 1:
            Prey.despawn = 100
            grace_period = 200
        elif self.difficulty == 2:
            Prey.despawn = 80
            grace_period = 160
        else:
            raise ValueError(f"Invalid difficulty!")

        # Get Player image and its dead counterpart
        player_image = self.player_images[self.player_image_index]
        player_image_dead = self.player_images_dead[self.player_image_index]

        # Declaring player
        # 10% Chance of reversing Player/Prey for easter egg
        list_players:list[Player] = []
        easter = randint(1, 10) == 10
        if easter:
            
            # Random num for prey image
            num = rand_num(len(self.prey_images))

            # Singleplayer
            if self.play_mode == 0:
                list_players = [
                    Player(self.prey_images[num], self.prey_images[num], easter, self.screen)
                ]

            # Multiplayer
            elif self.play_mode == 1:
                list_players = [
                    Player(self.prey_images[num], self.prey_images[num], easter, self.screen),
                    Player(self.prey_images[num], self.prey_images[num], easter, self.screen)
                ]
            
            # Resets prey list
            self.prey_images = []

            # Add all player images to prey list
            for image in self.player_images:
                prey_image = pygame.transform.smoothscale(image, (64, 64))
                self.prey_images.append(prey_image)
            for image in self.player_images_dead:
                prey_image = pygame.transform.smoothscale(image, (64, 64))
                self.prey_images.append(prey_image)

        else:

            # Singleplayer
            if self.play_mode == 0:
                list_players = [
                    Player(player_image, player_image_dead, easter, self.screen)
                ]

            # Multiplayer
            elif self.play_mode == 1:
                list_players = [
                    Player(player_image, player_image_dead, easter, self.screen),
                    Player(player_image, player_image_dead, easter, self.screen)
                ]

        # Prey declaration
        list_preys:list[Prey] = []
        if self.play_mode == 0:
            list_preys = [
                Prey(self.prey_images, self.prey_aura, self.screen),
                Prey(self.prey_images, self.prey_aura, self.screen)
            ]

        elif self.play_mode == 1:
            list_preys = [
                Prey(self.prey_images, self.prey_aura, self.screen),
                Prey(self.prey_images, self.prey_aura, self.screen),
                Prey(self.prey_images, self.prey_aura, self.screen),
                Prey(self.prey_images, self.prey_aura, self.screen)
            ]

        # Dagger declaration
        list_daggers:list[Dagger] = []
        if self.play_mode == 0:
            list_daggers:list[Dagger] = [
                Dagger(self.dagger_images, self.screen)
            ]

        elif self.play_mode == 1:
            list_daggers:list[Dagger] = [
                Dagger(self.dagger_images, self.screen),
                Dagger(self.dagger_images, self.screen)
            ]


        # Health bar declaration
        health_bar = HealthBar(self.health_bar, self.screen)

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
                    sys.exit()

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
                self.screen.blit(self.background_image, (0, 0))

                # Play dagger sound if its on screen
                for dagger in list_daggers:
                    if 0 <= dagger.coords[0] <= self.screen.get_width() and 0 <= dagger.coords[1] <= self.screen.get_height():
                        dagger.play_sound()

                # Player speed decrease
                for player in list_players:
                    player.speed -= 0.10

                # Player size decrease
                if grace_period <= 0:
                    for player in list_players:
                        player.size -= 0.15
                else:
                    grace_period -= 1
                    for player in list_players:
                        player.size -= 0.10

                # Draw player/s
                [player.draw() for player in list_players]

                # Player draw Ow! text & Draw hit red overlay
                for player in list_players:
                    if player.ow_txt_counter > 0:
                        player.draw_text("Ow!")
                        player.draw_hit()
                
                # Draw prey
                [prey.draw() for prey in list_preys]
                    
                # Draw dagger
                [dagger.draw() for dagger in list_daggers]
                
                # Trying to eat prey
                for player in list_players:
                    for prey in list_preys:
                        eat_prey(player, prey, easter)
                
                # Check if player is hit by dagger
                for player in list_players:
                    for dagger in list_daggers:
                        dagger_hit(player, dagger)

                # Player draw Nom! text
                for player in list_players:
                    if player.nom_txt_counter > 0:
                        player.draw_text("Nom!")

                # Game over
                for player in list_players:
                    if player.size <= player.min_size:
                        running = False

                # Set True to use Player debug console prints and dots
                n = 0
                player_debug(list_players[n], self.screen, False)

                # Set True to use Prey debug console prints and dot
                m = 0
                prey_debug(list_preys[m], self.screen, False)

                # FPS Text display
                fps = round(clock.get_fps())
                if fps > 55:
                    fps_display = text_small.render(f'FPS: {fps}', True, (255, 255, 255))
                    self.screen.blit(fps_display, (1220, 695))
                else:
                    fps_display = text_small.render(f'FPS: {fps}', True, (255, 0, 0))
                    self.screen.blit(fps_display, (1220, 695))

                # Song name display
                song_name = text_small.render(f"{get_song_name(song_index, self.theme_songs)}", True, (255, 255, 255))
                self.screen.blit(song_name, (10, 695))

                # Points text display - only for singleplayer
                if self.play_mode == 0:
                    points_text = text.render(f'Points: {list_players[0].points}', True, (255, 255, 255))
                    self.screen.blit(points_text, (10, 10))
                
                # Health bar display
                # Singleplayer
                if self.play_mode == 0:
                    health_bar.draw("Health:", list_players[0].size, list_players[0].max_size, list_players[0].min_size, (1000, 20))
                # Multiplayer
                elif self.play_mode == 1:

                    # Player 1
                    health_bar.draw("Player 1 Health:", list_players[0].size, list_players[0].max_size, list_players[0].min_size, (188, 20))
                    
                    # Player 2
                    health_bar.draw("Player 2 Health:", list_players[1].size, list_players[1].max_size, list_players[1].min_size, (1000, 20))

                # Controls for Player/s
                # Singleplayer
                if self.play_mode == 0:
                    player_control(list_players[0], dt, True, True)
                    check_screen_bounds(self.screen, list_players[0])
                # Multiplayer
                elif self.play_mode == 1:
                    player_control(list_players[0], dt, True, False)
                    player_control(list_players[1], dt, False, True)
                    check_screen_bounds(self.screen, list_players[0])
                    check_screen_bounds(self.screen, list_players[1])
                    check_player_collision(list_players[0], list_players[1])
            # -------------------------------------------------------------------------------------------- 
            # PAUSE screen
            else:
                # screen and player
                self.screen.blit(self.background_image, (0, 0))
                [player.draw() for player in list_players]

                # Game paused text
                paused_text = text_big.render('Game Paused', True, (255, 255, 255))
                paused_text_rect = paused_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 30))
                self.screen.blit(paused_text, paused_text_rect)

                # Press 'P' text
                press_text = text.render("Press 'P' to unpause", True, (255, 255, 255))
                press_text_rect = press_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 30))
                self.screen.blit(press_text, press_text_rect)
                pygame.display.flip()

            # flip() the display to put work on screen
            pygame.display.flip()

            # Limits FPS to 60
            dt = clock.tick(60) / 1000

        # --------------------------------------------------------------------------------------------
        # GAME OVER SCREEN 
        self.screen.blit(self.background_image, (0, 0))
                         
        # Stop music and fadeout
        pygame.mixer.music.fadeout(2500)

        # Singleplayer
        if self.play_mode == 0:

            # Draw dead player
            list_players[0].draw_dead()

            # Game over text
            game_over = text_big.render('Game Over!', True, (255, 255, 255))
            game_over_rect = game_over.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 30))
            self.screen.blit(game_over, game_over_rect)

            # Points text
            points_final = text.render(f'Points: {list_players[0].points}', True, (255, 255, 255))
            points_final_rect = points_final.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 30))
            self.screen.blit(points_final, points_final_rect)

        # Multiplayer
        elif self.play_mode == 1:
        
            if list_players[0].size <= list_players[0].min_size:
                list_players[0].draw_dead()
                list_players[1].draw()
                game_over = text_big.render('Player 1 Lost!', True, (255, 255, 255))
                game_over_rect = game_over.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 30))
                self.screen.blit(game_over, game_over_rect)

            elif list_players[1].size <= list_players[1].min_size:
                list_players[0].draw()
                list_players[1].draw_dead()
                game_over = text_big.render('Player 2 Lost!', True, (255, 255, 255))
                game_over_rect = game_over.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 30))
                self.screen.blit(game_over, game_over_rect)

        # Put work on screen
        pygame.display.flip()

        # Sleep to show end screen
        sleep(3)
