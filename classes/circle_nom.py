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

    def __init__(self, screen, difficulty, eat_sounds, 
                 theme_songs, player_images, player_image_index, 
                 player_images_dead, prey_images, prey_aura,
                 background_image, hunger_bar, 
                 dagger_images, dagger_sounds, 
                 hit_sounds):
        
        self.screen:pygame.Surface = screen
        self.difficulty:int = difficulty
        self.eat_sounds = eat_sounds
        self.theme_songs = theme_songs
        self.player_image_index = player_image_index
        self.player_images = player_images
        self.player_images_dead = player_images_dead
        self.prey_aura = prey_aura
        self.prey_images = prey_images
        self.background_image = background_image
        self.hunger_bar = hunger_bar
        self.dagger_images = dagger_images
        self.dagger_sounds = dagger_sounds
        self.hit_sounds = hit_sounds

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
                    # Bonus size, speed & points for aura'd food
                    if prey.aura:
                        player.size += 20
                        player.speed += 15
                        points += 3
                    else:
                        player.size += 12
                        player.speed += 5
                        points += 1
                # Easter eating
                else:
                    # Bonus points for aura'd food
                    if prey.aura:
                        points += 3
                    else:
                        player.size += 10
                        player.speed += 6
                        points += 1

                # Play eat random sound
                self.eat_sounds[rand_num(len(self.eat_sounds))].play()

                # Set eat text to show & remove ow
                player.nom_txt_counter = 30
                player.ow_txt_counter = 0

                # Reset prey
                prey.reset_prey()

            return points
        
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

        # Get Player image and its dead counterpart
        player_image = self.player_images[self.player_image_index]
        player_image_dead = self.player_images_dead[self.player_image_index]

        # Declaring player
        # 10% Chance of reversing Player/Prey for easter egg
        easter = randint(1, 10)
        if easter == 10:
            # Turn on easter mode
            easter = True
            num = rand_num(len(self.prey_images))

            # Check if the image is glowing_sandwich
            if num > 0:
                player_1 = Player(self.prey_images[num], self.prey_images[num], easter, self.screen)

            # If it is, set player images to another image, since gif_pygame doesn't support code below
            else:
                player_1 = Player(self.prey_images[1], self.prey_images[1], easter, self.screen)
            
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
            easter = False
            player_1 = Player(player_image, player_image_dead, easter, self.screen)

        # Prey declaration
        prey_1 = Prey(self.prey_images, self.prey_aura, self.screen)
        prey_2 = Prey(self.prey_images, self.prey_aura, self.screen)

        # Health bar declaration
        bar = HealthBar(self.hunger_bar, self.screen)

        # Dagger declaration
        dagger_1 = Dagger(self.dagger_images, self.screen)

        # Initial points
        points = 0

        # Pause - Skips over entire game loop, except the event checker.
        paused = False

        # Main game loop
        running = True

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

                # Draw player
                player_1.draw()

                # Play dagger sound if its on screen
                if 0 <= dagger_1.coords[0] <= self.screen.get_width() and 0 <= dagger_1.coords[1] <= self.screen.get_height():
                    dagger_1.play_sound()

                # Player speed decrease
                player_1.speed -= 0.1

                # Player size decrease
                if grace_period <= 0:
                    player_1.size -= 0.15
                else:
                    player_1.size -= 0.10
                    grace_period -= 1

                # Player draw Ow! text & Draw hit red overlay
                if player_1.ow_txt_counter > 0:
                    player_1.draw_text("Ow!")
                    if not easter:
                        player_1.draw_hit()
                
                # Draw prey 1
                prey_1.draw()
                
                # Draw prey 2
                prey_2.draw()
                    
                # Draw dagger
                dagger_1.draw()
                
                # Trying to eat prey_1 and prey_2
                points = eat_prey(player_1, prey_1, easter, points)
                points = eat_prey(player_1, prey_2, easter, points)

                # Check if player_1 is hit by dagger
                dagger_hit(player_1, dagger_1)

                # Player draw Nom! text
                if player_1.nom_txt_counter > 0:
                    player_1.draw_text("Nom!")

                # Game over
                if player_1.size <= player_1.min_size:
                    running = False

                # Set True to use Player debug console prints and dots
                player_debug(player_1, self.screen, False)

                # Set True to use Prey debug console prints and dot
                prey_debug(prey_1, self.screen, False)
                prey_debug(prey_2, self.screen, False)

                # FPS Text display
                fps = round(clock.get_fps())
                if fps > 55:
                    fps_display = text_small.render(f'FPS: {fps}', True, (255, 255, 255))
                    self.screen.blit(fps_display, (1220, 695))
                else:
                    fps_display = text_small.render(f'FPS: {fps}', True, (255, 0, 0))
                    self.screen.blit(fps_display, (1220, 695))

                # Points text display
                points_text = text.render(f'Points: {points}', True, (255, 255, 255))
                self.screen.blit(points_text, (10, 10))

                # Song name display
                song_name = text_small.render(f"{get_song_name(song_index, self.theme_songs)}", True, (255, 255, 255))
                self.screen.blit(song_name, (10, 695))

                # Health bar display
                bar.draw(player_1.size, player_1.max_size, player_1.min_size, (1000, 21))
                health_txt = text.render('Health:', True, (255, 255, 255))
                self.screen.blit(health_txt, (930, 10))

                # Controls for Player 1
                player_control(player_1, dt, True, False)

                # Check if player is in screen bounds
                check_bounds(self.screen, player_1)

            # -------------------------------------------------------------------------------------------- 
            # PAUSE screen
            else:
                # screen and player
                self.screen.blit(self.background_image, (0, 0))
                player_1.draw()

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

        pygame.mixer.music.fadeout(2500)

        # Draw game end screen
        self.screen.blit(self.background_image, (0, 0))
        player_1.draw_dead()

        # Game over text
        game_over = text_big.render('Game Over!', True, (255, 255, 255))
        game_over_rect = game_over.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 30))
        self.screen.blit(game_over, game_over_rect)

        # Points txt
        points_final = text.render(f'Points: {points}', True, (255, 255, 255))
        points_final_rect = points_final.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 30))
        self.screen.blit(points_final, points_final_rect)
        pygame.display.flip()

        # Sleep to show end screen
        sleep(3)