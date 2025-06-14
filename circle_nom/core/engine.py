# Emko/ExtremerBG was here

# Circle Nom Game

# Importing modules
from circle_nom.helpers.asset_bank import COMIC_SANS_MS
from circle_nom.systems.asset_loader import *
from circle_nom.helpers.player_utils import *
from circle_nom.helpers.other_utils import *
from circle_nom.systems.debug import *
from circle_nom.ui.health_bar import *
from circle_nom.models.dagger import *
from circle_nom.models.player import *
from circle_nom.models.prey import *
from random import randint, choice
from math import isclose
from time import sleep
import pygame
import sys

class CircleNom():
    
    def __init__(self, screen:pygame.Surface, fps_cap:int, difficulty:int,
                 play_mode:int, eat_sounds:tuple[pygame.mixer.Sound],
                 game_themes:tuple[tuple[str, str]], player_image:pygame.Surface,
                 player_image_dead:pygame.Surface, player_accessory: tuple[pygame.Vector2, pygame.Surface] | None,
                 player_eat_sequence: list[pygame.Surface], prey_images:tuple[pygame.Surface], 
                 prey_aura:pygame.Surface, background_image:pygame.Surface, 
                 health_bar:tuple[pygame.Surface], dagger_images:tuple[pygame.Surface], 
                 dagger_sounds:tuple[pygame.mixer.Sound], flame_sequence:tuple[pygame.Surface], 
                 hit_sounds:tuple[pygame.mixer.Sound], dash_images:dict[str: pygame.Surface]
                 ) -> None:
        """
        Initializes the Circle Nom game with its various assets and settings.

        Args:
            screen (pygame.Surface): The game screen.
            fps_cap (int): The FPS the game should run at.
            difficulty (int): The game difficulty level.
            play_mode (int): The game mode: 0 for Singleplayer, 1 for Multiplayer.
            eat_sounds (tuple[pygame.mixer.Sound]): Tuple of sounds to play when eating prey.
            game_themes (tuple[tuple[str, str]]): Tuple with tuples consisting of (name, file path).
            player_image (pygame.Surface): The player's image.
            player_image_dead (pygame.Surface): The player's dead image.
            player_accessory (tuple(pygame.Vector2, pygame.Surface)|None): The player's accessory data pair.
            player_eat_sequence (list(pygame.Surface)): The player's eat sequence animation.
            prey_images (tuple[pygame.Surface]): Tuple of prey images.
            prey_aura (pygame.Surface): The aura image for prey.
            background_image (pygame.Surface): The background image for the game.
            health_bar (tuple[pygame.Surface]): Tuple of health bar images.
            dagger_images (tuple[pygame.Surface]): Tuple of dagger images.
            dagger_sounds (tuple[pygame.mixer.Sound]): Tuple of sounds to play when a dagger is used.
            flame_sequence (tuple[pygame.Surface]): Tuple of flame images.
            hit_sounds (tuple[pygame.mixer.Sound]): Tuple of sounds to play when the player is hit.
            dash_images (dict[str: pygame.Surface]): Dictionary of dash icon images.
        """
        self.screen = screen
        self.fps_cap = fps_cap
        self.difficulty = difficulty
        self.play_mode = play_mode
        self.player_count = play_mode + 1 # 1 or 2 players
        self.prey_count = (play_mode + 1) * 2 # 2 or 4 preys
        self.dagger_count = play_mode + 1 # 1 or 2 daggers
        self.eat_sounds = eat_sounds
        self.game_themes = game_themes
        self.player_image = player_image
        self.player_image_dead = player_image_dead
        self.player_accessory = player_accessory
        self.player_eat_sequence = player_eat_sequence
        self.prey_images = prey_images
        self.prey_aura = prey_aura
        self.background_image = background_image
        self.health_bar = health_bar
        self.dagger_images = dagger_images
        self.dagger_sounds = dagger_sounds
        self.flame_sequence = flame_sequence
        self.hit_sounds = hit_sounds
        self.dash_images = dash_images

    def start(self) -> None:
        """
        Starts the Circle Nom game.
        """

        def music_player(index:int) -> str:
            """
            Plays music from the game_themes list with the given index. Returns the song name.
            
            Args:
                index (int): The index of the song to play.
            """
            if type(index) != int:
                raise ValueError("Index must be integer!")
            
            pygame.mixer.music.unload()
            song_name, song_path = self.game_themes[song_index % len(self.game_themes)]
            load_music(song_path)
            pygame.mixer.music.play()
            return song_name

        def eat_prey(player:Player, prey:Prey, easter:bool) -> None:
            """
            Checks if player is near a prey object.

            Args:
                player (class Player): The player to check with.
                prey (class Prey): The prey to check with.
                easter (bool): Bool if easter mode is on.
            """
            if isclose(player.eat_pos.x, prey.position.x, abs_tol=player.eat_tol) and \
                isclose(player.eat_pos.y, prey.position.y, abs_tol=player.eat_tol) and prey.eatable and player.can_eat:
                # player.can_eat can also be used here, which is false during the eating animation,
                # but im not sure if feels good to play with it - more testing might be required.
                
                # Normal eating
                if not easter:

                    # Bonus size, speed & points for aura'd food
                    if prey.aura:
                        player.size += 20
                        player.speed += 15
                        player.last_speed += 15
                        player.points += 3
                    else:
                        player.size += 12
                        player.speed += 5
                        player.last_speed += 5
                        player.points += 1

                # Easter eating
                else:

                    # Bonus points for aura'd food
                    if prey.aura:
                        player.size += 12
                        player.speed += 10
                        player.last_speed += 10
                        player.points += 2
                    else:
                        player.size += 6
                        player.speed += 5
                        player.last_speed += 5
                        player.points += 1

                # Play eat random sound
                choice(self.eat_sounds).play()

                # Set eat text to show & remove ow
                player.nom_txt_counter = 30
                player.ow_txt_counter = 0

                # Reset prey
                prey.reset_prey()
        
        def dagger_hit(player:Player, dagger:Dagger) -> None:
            """
            Checks if player is hit by a dagger object.
            Args:
                player (class Player): The player to check with.
                dagger (class Dagger): The dagger to check with.
            """

            if isclose(player.hit_pos.x, dagger.position.x, abs_tol=player.hit_tol) and \
                isclose(player.hit_pos.y, dagger.position.y, abs_tol=player.hit_tol):

                # Bigger penalty if its a flaming dagger
                if dagger.flame:
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
                choice(self.hit_sounds).play()

        # Check if play_mode is valid
        if self.play_mode not in [0, 1]:
            raise ValueError("Invalid play mode!\n 0 - Singleplayer\n 1 - Multiplayer")
        
        # Difficulty selector - Adjusts prey despawn timers:
        # 0 - Easy
        # 1 - Medium
        # 2 - Hard
        if self.difficulty == 0:
            Prey.DESPAWN = 110
        elif self.difficulty == 1:
            Prey.DESPAWN = 90
        elif self.difficulty == 2:
            Prey.DESPAWN = 70
        else:
            raise ValueError(f"Invalid difficulty!")

        # Declaring player
        # 10% Chance of reversing Player/Prey for easter egg
        tuple_players: tuple[Player] = []
        easter = randint(1, 10) == 10
        
        # Normal mode
        if not easter:
            
            # Player/s declaration
            tuple_players: tuple[Player] = declare_objects(
                self.player_count, Player, self.player_image, self.player_image_dead,
                self.player_eat_sequence, self.player_accessory, easter, self.screen
            )

        # Easter mode
        else:
    
            # Random prey_images_index for prey image
            prey_images_index = randint(0, len(self.prey_images) - 1)
            tuple_players: tuple[Player] = declare_objects(
                self.player_count, Player, self.prey_images[prey_images_index], self.prey_images[prey_images_index],
                None, None, easter, self.screen
            ) # Dont use player eat sequence and player accessory for easter mode
            
            # Resets prey list
            self.prey_images = []

            # Add all player images to prey list instead
            prey_image = pygame.transform.smoothscale(self.player_image, (64, 64))
            self.prey_images.append(prey_image)
            prey_image = pygame.transform.smoothscale(self.player_image_dead, (64, 64))
            self.prey_images.append(prey_image)
                
            # Different dash cooldown in easter mode
            for player in tuple_players: player.dash_cd(30)

        # Health bar declaration
        health_bar = HealthBar(self.health_bar, self.screen)
        
        # Preys declaration
        tuple_preys:tuple[Prey] = declare_objects(self.prey_count, Prey, self.prey_images, self.prey_aura, self.screen)

        # Dagger/s declaration
        tuple_daggers:tuple[Dagger] = declare_objects(self.dagger_count, Dagger, self.dagger_images, self.dagger_sounds, self.flame_sequence, self.screen)
        
        # Dagger initial grace period
        for dagger in tuple_daggers:
            dagger.grace_spawn(randint(60, 90))
            
        # Clock for framerate
        clock = pygame.time.Clock()

        # Delta time
        dt = 0

        # Fonts
        font = pygame.Font(COMIC_SANS_MS, 30)
        font_big = pygame.Font(COMIC_SANS_MS, 60)
        font_small = pygame.Font(COMIC_SANS_MS, 15)
        
        # Play random theme song from list
        song_index = randint(0, len(self.game_themes) - 1)
        song_name, song_path = self.game_themes[song_index]
        load_music(song_path)
        pygame.mixer.music.play()
        
        # Colours
        WHITE = (255, 255, 255)

        # Pause - Skips over game loop, excluding event checker and pause screen
        paused = False

        # Main game loop
        running = True
        while running:

            # --------------------------------------------------------------------------------------------
            # EVENT CHECKER - MUST ALWAYS RUN.
            for event in pygame.event.get():
                    
                # QUIT WINDOW / ALT + F4
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Music auto queue
                if event.type == pygame.USEREVENT:
                    song_index += 1
                    song_name = music_player(song_index)

                # Key event checker - part of EVENT CHECKER
                if event.type == pygame.KEYDOWN:
                    
                    # Escape
                    if event.key == pygame.K_ESCAPE:
                        running = False # break gameloop
                        
                    # Game pause/unpause - P
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
                            song_name = music_player(song_index)

                        # Backward in list songs
                        elif event.key == pygame.K_q:
                            song_index -= 1
                            song_name = music_player(song_index)
            # --------------------------------------------------------------------------------------------

            # ACTUAL GAME LOOP
            if not paused:         
                # Fill the screen with background image to wipe away anything from last frame
                self.screen.blit(self.background_image, (0, 0))

                # Iterate over daggers
                for dagger in tuple_daggers:
                    
                    # Play dagger sound if its on screen
                    if 0 <= dagger.position.x <= self.screen.get_width() and \
                        0 <= dagger.position.y <= self.screen.get_height():
                        dagger.play_sound()
                    
                    # Draw dagger
                    dagger.draw(dt)

                # Iterate over players
                for player in tuple_players:
                    
                    # Player size decrease
                    player.size -= player_size_reduct(player, dt)  
                    
                    # Player speed decrease
                    player.speed -= 6 * dt
                    
                    # Player draw hit text and use image_hit
                    if player.ow_txt_counter > 0:
                        player.draw_hit = True
                    else:
                        player.draw_hit = False

                    # Draw player with image/image_hit
                    player.draw(dt)
                    
                    # Iterate over preys
                    for prey in tuple_preys:
                        
                        # Draw prey
                        prey.draw(dt)
                        
                        # Try to eat prey
                        eat_prey(player, prey, easter)
                    
                    # Check if player is hit by dagger
                    for dagger in tuple_daggers:
                        dagger_hit(player, dagger)
                    
                    # Game over
                    if player.size <= player.MIN_SIZE:
                        running = False

                # Set True to use Player debug console prints and dots
                player_debug(tuple_players, 0, self.screen, False)

                # Set True to use Prey debug console prints and dot
                prey_debug(tuple_preys, 0, self.screen, False)
                
                # Set True to use Dagger debug console prints and dot
                dagger_debug(tuple_daggers, 0, self.screen, False) 

                # FPS Text display
                draw_fps(self.screen, clock, font_small)

                # Song name display
                self.screen.blit(font_small.render(song_name, True, WHITE), (10, 695))
                
                # Dash image display
                # Singleplayer
                if self.play_mode == 0:
                    if tuple_players[0].dash_available:
                        self.screen.blit(self.dash_images["AVAIL"], (1234, 18))
                    else:
                        self.screen.blit(self.dash_images["UNAVAIL"], (1234, 18))
                # Multiplayer
                elif self.play_mode == 1:
                    # Player 1
                    if tuple_players[0].dash_available:
                        self.screen.blit(self.dash_images["AVAIL"], (472, 18))
                    else:
                        self.screen.blit(self.dash_images["UNAVAIL"], (472, 18))
                    # Player 2
                    if tuple_players[1].dash_available:
                        self.screen.blit(self.dash_images["AVAIL"], (1234, 18))
                    else:
                        self.screen.blit(self.dash_images["UNAVAIL"], (1234, 18))

                # Points text display - only for singleplayer
                if self.play_mode == 0:
                    points_text = font.render(f'Points: {tuple_players[0].points}', True, WHITE)
                    self.screen.blit(points_text, (10, 10))
                
                # Health bar display
                # Singleplayer
                if self.play_mode == 0:
                    health_bar.draw("Health:", tuple_players[0].size, tuple_players[0].MAX_SIZE, tuple_players[0].MIN_SIZE, (950, 20))
                # Multiplayer
                elif self.play_mode == 1:

                    # Player 1
                    health_bar.draw("Player 1 Health:", tuple_players[0].size, tuple_players[0].MAX_SIZE, tuple_players[0].MIN_SIZE, (188, 20))
                    
                    # Player 2
                    health_bar.draw("Player 2 Health:", tuple_players[1].size, tuple_players[1].MAX_SIZE, tuple_players[1].MIN_SIZE, (950, 20))

                # Controls for Player/s
                # Singleplayer
                if self.play_mode == 0:
                    player_control(tuple_players[0], dt, True, True)
                    player_check_bounds(self.screen, tuple_players[0])
                # Multiplayer
                elif self.play_mode == 1:
                    player_control(tuple_players[0], dt, False, True)
                    player_control(tuple_players[1], dt, True, False)
                    player_check_bounds(self.screen, tuple_players[0])
                    player_check_bounds(self.screen, tuple_players[1])
                    player_check_collision(tuple_players[0], tuple_players[1], dt)
                    
            # -------------------------------------------------------------------------------------------- 
            # PAUSE screen
            else:
                # screen and player
                self.screen.blit(self.background_image, (0, 0))
                for player in tuple_players: player.draw(dt)

                # Game paused text
                paused_text = font_big.render('Game Paused', True, WHITE)
                paused_text_rect = paused_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 30))
                self.screen.blit(paused_text, paused_text_rect)

                # Press 'P' text
                press_text = font.render("Press 'P' to unpause", True, WHITE)
                press_text_rect = press_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 30))
                self.screen.blit(press_text, press_text_rect)
                pygame.display.flip()

            # flip() the display to put work on screen
            pygame.display.flip()

            # Limit FPS to cap. Set delta time.
            dt = clock.tick(self.fps_cap) / 1000

        # --------------------------------------------------------------------------------------------
        # GAME OVER SCREEN 
        self.screen.blit(self.background_image, (0, 0))
                         
        # Stop music and fadeout
        pygame.mixer.music.fadeout(2500)

        # Singleplayer
        if self.play_mode == 0:

            # Draw dead player
            tuple_players[0].draw_dead()

            # Game over text
            game_over = font_big.render('Game Over!', True, WHITE)
            game_over_rect = game_over.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 30))
            self.screen.blit(game_over, game_over_rect)

            # Points text
            points_final = font.render(f'Points: {tuple_players[0].points}', True, WHITE)
            points_final_rect = points_final.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 30))
            self.screen.blit(points_final, points_final_rect)

        # Multiplayer
        elif self.play_mode == 1:
        
            if tuple_players[0].size <= tuple_players[0].MIN_SIZE:
                tuple_players[0].draw_dead()
                tuple_players[1].draw(dt)
                game_over = font_big.render('Player 1 Lost!', True, WHITE)
                game_over_rect = game_over.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 30))
                self.screen.blit(game_over, game_over_rect)

            elif tuple_players[1].size <= tuple_players[1].MIN_SIZE:
                tuple_players[0].draw(dt)
                tuple_players[1].draw_dead()
                game_over = font_big.render('Player 2 Lost!', True, WHITE)
                game_over_rect = game_over.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 30))
                self.screen.blit(game_over, game_over_rect)
                
            else:
                # Game over text
                game_over = font_big.render('Game Over!', True, WHITE)
                game_over_rect = game_over.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 30))
                self.screen.blit(game_over, game_over_rect)
                for player in tuple_players: player.draw_dead()

        # Put work on screen
        pygame.display.flip()

        # Sleep to show end screen
        sleep(3)