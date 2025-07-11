# Emko/ExtremerBG was here

# Circle Nom Game

# Importing modules
from circle_nom.helpers.asset_bank import COMIC_SANS_MS
import circle_nom.systems.asset_loader as asset_loader
import circle_nom.helpers.player_utils as player_utils
import circle_nom.helpers.other_utils as other_utils
from circle_nom.helpers.asset_bank import *
import circle_nom.helpers.debug as debug
from circle_nom.systems.timer import *
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
    
    def __init__(self,
                 screen: pygame.Surface, 
                 timer: Timer,
                 fps_cap: int, 
                 difficulty: int,
                 play_mode: int,
                 player_accessory: tuple[pygame.Vector2, pygame.Surface] | None,
                 background_image: pygame.Surface
                 ) -> None:
        """
        Initializes the Circle Nom game with settings and assets given from the Menu.

        Args:
            screen (pygame.Surface): The screen object, declared in main.
            timer (Timer): The timer object, declared in main.
            fps_cap (int): The FPS the game should run at, selected in the Menu.
            difficulty (int): The game difficulty level, selected in the Menu.
            play_mode (int): The game mode, selected in the Menu. Can be 0 - Singleplayer or 1 - Multiplayer.
            player_accessory (tuple[pygame.Vector2, pygame.Surface] | None): The player's accessory data pair, randomly chosen in the Menu.
            background_image (pygame.Surface): The game's background image, randomly chosen in the Menu.
        """
        # -- Main Objects: declared in Main --
        self.screen = screen
        self.game_timer = timer
        
        # -- Menu Settings: set in the Menus --
        if type(fps_cap) in (int, float):
            self.FPS_CAP = fps_cap
        else:
            logger.error(msg="Invalid fps cap. Falling back to 120.")
            self.FPS_CAP = 120
        
        if difficulty in (0, 1, 2):
            self.DIFFICULTY = difficulty
        else:
            logger.error(msg="Invalid difficulty level. Falling back to 1 - Medium.")
            self.DIFFICULTY = 1
        
        if play_mode in (0, 1):
            self.PLAY_MODE = play_mode
        else:
            logger.error("Invalid play mode level. Falling back to 0 - Singleplayer.")
            self.PLAY_MODE = 0
        
        # -- Menu Randoms: chosen in the Menu --
        self.PLAYER_ACCESSORY = player_accessory
        self.BACKGROUND_IMAGE = background_image

    def start(self) -> None:
        """
        Starts the Circle Nom game.
        """
        # Calculate game object counts based on the play mode
        PLAYER_COUNT = self.PLAY_MODE + 1       # 1 or 2 players
        PREY_COUNT = (self.PLAY_MODE  + 1) * 2  # 2 or 4 preys
        DAGGER_COUNT = self.PLAY_MODE  + 1      # 1 or 2 daggers
        
        def music_player(index:int) -> str:
            """
            Plays music from the game_themes list with the given index. Returns the song name.
            
            Args:
                index (int): The index of the song to play.
            """
            if type(index) != int:
                raise ValueError("Index must be integer!")
            
            pygame.mixer.music.unload()
            song_name, song_path = GAME_THEMES[song_index % len(GAME_THEMES)]
            asset_loader.load_music(song_path)
            pygame.mixer.music.play()
            return song_name

        def eat_prey(player: Player, prey: Prey, EASTER_MODE:bool) -> None:
            """
            Checks if player is near a prey object.

            Args:
                player (class Player): The player to check with.
                prey (class Prey): The prey to check with.
                EASTER_MODE (bool): Bool if EASTER_MODE mode is on.
            """
            # Compare XY coords of player & prey with the player's eat tolerance
            if isclose(player.eat_pos.x, prey.position.x, abs_tol=player.eat_tol) and \
                isclose(player.eat_pos.y, prey.position.y, abs_tol=player.eat_tol) and \
                    prey.eatable and player.can_eat:
                
                # Normal eating
                if not EASTER_MODE:

                    # Bonus size, speed & points for aura'd food
                    if prey.aura:
                        player.size += 20
                        player.speed += 15
                        player.speed_before_dash += 15
                        player.points += 3
                    else:
                        player.size += 12
                        player.speed += 5
                        player.speed_before_dash += 5
                        player.points += 1

                # Easter eating
                else:

                    # Bonus points for aura'd food
                    if prey.aura:
                        player.size += 12
                        player.speed += 10
                        player.speed_before_dash += 10
                        player.points += 2
                    else:
                        player.size += 6
                        player.speed += 5
                        player.speed_before_dash += 5
                        player.points += 1
                        
                # Play eat random sound
                choice(EAT_SOUNDS).play()

                # Reset player and prey
                prey.reset_prey()
                player.reset_eat_attributes()
        
        def dagger_hit(player: Player, dagger: Dagger) -> None:
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

                # First reset dagger & player
                dagger.reset_dagger()
                player.reset_hurt_attributes()

                # if player is hit dagger spawn will have a grace period
                dagger.grace_spawn(uniform(1, 2))

                # Play random sound 
                choice(HIT_SOUNDS).play()
        
        # Difficulty selector - Adjusts prey balancing attributes
        # Easy
        if self.DIFFICULTY == 0:
            Prey.set_spawned_duration(new_duration=1.6)
        # Medium
        elif self.DIFFICULTY == 1:
            Prey.set_spawned_duration(new_duration=1.0)
          # Hard
        elif self.DIFFICULTY == 2:
            Prey.set_spawned_duration(new_duration=0.6)

        # Declaring player
        # 10% Chance of reversing Player/Prey for easter egg
        tuple_players: tuple[Player] = []
        EASTER_MODE = randint(1, 10) == 10
        
        # Normal mode
        if not EASTER_MODE:
            # Player/s declaration
            tuple_players: tuple[Player] = other_utils.declare_objects(
                PLAYER_COUNT, 
                Player, self.screen, self.game_timer, EASTER_MODE,
                PLAYER_IMAGE, PLAYER_IMAGE_DEAD, PLAYER_EAT_SEQUENCE, self.PLAYER_ACCESSORY
            )

        # Easter mode
        else:            
            # Player/s declaration
            TEMP_easter_player_image = choice(PREY_IMAGES)
            tuple_players: tuple[Player] = other_utils.declare_objects(
                PLAYER_COUNT, 
                Player, self.screen, self.game_timer, EASTER_MODE,
                TEMP_easter_player_image, TEMP_easter_player_image, None, None
            ) # Dont use player eat sequence and player accessory for easter mode
            
            # Create a new temporary prey images list
            TEMP_prey_images = []

            # Add all player images to prey list instead
            TEMP_prey_images.append(pygame.transform.smoothscale(PLAYER_IMAGE, (64, 64)))
            TEMP_prey_images.append(pygame.transform.smoothscale(PLAYER_IMAGE_DEAD, (64, 64)))
                
            # Different dash cooldown in easter mode
            for player in tuple_players: player.set_dash_cd(cd=0.6)

        # Health bar declaration
        health_bar = HealthBar(HEALTH_BAR, self.screen)
        
        # Preys declaration
        if not EASTER_MODE:
            tuple_preys:tuple[Prey] = other_utils.declare_objects(
                PREY_COUNT, Prey, self.screen, self.game_timer,
                PREY_IMAGES, PREY_AURA
            )
        else:
            tuple_preys:tuple[Prey] = other_utils.declare_objects(
                PREY_COUNT, Prey, self.screen, self.game_timer,
                TEMP_prey_images, PREY_AURA
            )

        # Dagger/s declaration
        tuple_daggers:tuple[Dagger] = other_utils.declare_objects(
            DAGGER_COUNT, Dagger, self.screen, self.game_timer,
            DAGGER_IMAGES, DAGGER_SOUNDS, FLAME_SEQUENCE
        )
        
        # Dagger initial grace period
        for dagger in tuple_daggers:
            dagger.grace_spawn(uniform(3, 4))
            
        # Fonts
        FONT_SMALL = pygame.Font(COMIC_SANS_MS, 15)
        FONT = pygame.Font(COMIC_SANS_MS, 30)
        FONT_BIG = pygame.Font(COMIC_SANS_MS, 60)
        
        # Play random theme song from list
        song_index = randint(0, len(GAME_THEMES) - 1)
        song_name, song_path = GAME_THEMES[song_index]
        asset_loader.load_music(song_path)
        pygame.mixer.music.play()
        
        # Colours
        WHITE = (255, 255, 255)
        
        # Clock for framerate
        clock = pygame.time.Clock()

        # Delta time
        dt = 0.00
        
        # Pause - Skips over game loop, excluding event checker and pause screen
        paused = False

        # Running - Keeps the entire game loop running
        running = True
        
        # Start game_timer before entering game loop
        self.game_timer.start()
        
        # ------------------------------------------------------------------------------------------------
        # MAIN LOOP - HOUSES THE EVENT CHECKER, GAME LOOP, PAUSE AND GAME OVER SCREENS
        while running:

            # --------------------------------------------------------------------------------------------
            # EVENT CHECKER - MUST ALWAYS RUN
            for event in pygame.event.get():
                    
                # Quit Window / Alt + F4
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
            # GAME LOOP - CAN BE PAUSED
            if not paused:         
                # Fill the screen with background image to wipe away anything from last frame
                self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))

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
                    player.size -= player_utils.get_size_reduct(player, dt)  
                    
                    # Player speed decrease
                    player.speed -= 5 * dt
                    
                    # Draw player with image/image_hit
                    player.draw(dt)
                    
                    # Iterate over preys
                    for prey in tuple_preys:
                        
                        # Draw prey
                        prey.draw(dt)
                        
                        # Try to eat prey
                        eat_prey(player, prey, EASTER_MODE)
                    
                    # Check if player is hit by dagger
                    for dagger in tuple_daggers:
                        dagger_hit(player, dagger)
                    
                    # Game over
                    if player.size <= player.MIN_SIZE:
                        running = False
                        
                # Debug functions - use by setting enable to True
                debug.player(players=tuple_players, player_n=0, screen=self.screen, enable=False)
                debug.prey(preys=tuple_preys, prey_n=0, screen=self.screen, enable=False)
                debug.dagger(daggers=tuple_daggers, dagger_n=0, screen=self.screen, enable=False) 

                # FPS Text display
                other_utils.draw_fps(self.screen, clock, FONT_SMALL)
                
                # Time elapsed display
                self.screen.blit(FONT_SMALL.render(f"Time elapsed: {self.game_timer.get_formatted_time()}", True, WHITE), (10, 50))

                # Song name display
                self.screen.blit(FONT_SMALL.render(song_name, True, WHITE), (10, 695))
                
                # Dash image display
                # Singleplayer
                if self.PLAY_MODE == 0:
                    if tuple_players[0].dash_available:
                        self.screen.blit(DASH_IMAGES["AVAIL"], (1234, 18))
                    else:
                        self.screen.blit(DASH_IMAGES["UNAVAIL"], (1234, 18))
                # Multiplayer
                elif self.PLAY_MODE == 1:
                    # Player 1
                    if tuple_players[0].dash_available:
                        self.screen.blit(DASH_IMAGES["AVAIL"], (472, 18))
                    else:
                        self.screen.blit(DASH_IMAGES["UNAVAIL"], (472, 18))
                    # Player 2
                    if tuple_players[1].dash_available:
                        self.screen.blit(DASH_IMAGES["AVAIL"], (1234, 18))
                    else:
                        self.screen.blit(DASH_IMAGES["UNAVAIL"], (1234, 18))

                # Points text display - only for singleplayer
                if self.PLAY_MODE == 0:
                    points_text = FONT.render(f'Points: {tuple_players[0].points}', True, WHITE)
                    self.screen.blit(points_text, (10, 10))
                
                # Health bar display
                # Singleplayer
                if self.PLAY_MODE == 0:
                    health_bar.draw("Health:", tuple_players[0].size, tuple_players[0].MAX_SIZE, tuple_players[0].MIN_SIZE, (950, 20))
                
                # Multiplayer
                elif self.PLAY_MODE == 1:   
                    health_bar.draw("Player 1 Health:", 
                                    tuple_players[0].size, tuple_players[0].MAX_SIZE, tuple_players[0].MIN_SIZE, 
                                    coords=(188, 20))
                    health_bar.draw("Player 2 Health:", 
                                    tuple_players[1].size, tuple_players[1].MAX_SIZE, tuple_players[1].MIN_SIZE, 
                                    coords=(950, 20))

                # Controls for Player/s
                # Singleplayer
                if self.PLAY_MODE == 0:
                    
                    # Enable both control options for singleplayer since we have only one player
                    player_utils.control_movement(tuple_players[0], dt, arrows=True, wasd=True)
                    player_utils.check_bounds(self.screen, tuple_players[0]) # Keeps player in screen area
                
                # Multiplayer
                elif self.PLAY_MODE == 1:
                    # Player 1 gets only WASD controls
                    player_utils.control_movement(player=tuple_players[0], dt=dt, arrows=False, wasd=True)
                    player_utils.check_bounds(screen=self.screen, player=tuple_players[0])
                    
                    # Player 2 gets ARROWS controls
                    player_utils.control_movement(player=tuple_players[1], dt=dt, arrows=True, wasd=False)
                    player_utils.check_bounds(screen=self.screen, player=tuple_players[1])
                    
                    # This checks if both players are near eachother and pushes them appart if they are
                    player_utils.check_collision(player_1=tuple_players[0], player_2=tuple_players[1], dt=dt)
                    
            # -------------------------------------------------------------------------------------------- 
            # PAUSE SCREEN
            else:
                # Pause the game_timer
                self.game_timer.stop()
                
                # Screen and player
                self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))
                for player in tuple_players: player.draw()

                # Game paused text
                paused_text = FONT_BIG.render('Game Paused', True, WHITE)
                paused_text_rect = paused_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 30))
                self.screen.blit(paused_text, paused_text_rect)

                # Press 'P' text
                press_text = FONT.render("Press 'P' to unpause", True, WHITE)
                press_text_rect = press_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 30))
                self.screen.blit(press_text, press_text_rect)
                
            # flip() the display to put work on screen
            pygame.display.flip()

            # Limit FPS to cap. Set delta time.
            dt = clock.tick(self.FPS_CAP) / 1000

        # --------------------------------------------------------------------------------------------
        # GAME OVER SCREEN
        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))
                                 
        # Stop music and fadeout
        pygame.mixer.music.fadeout(2500)

        # Singleplayer case
        if self.PLAY_MODE == 0:

            # Draw dead player
            tuple_players[0].draw_dead()

            # Game over text
            game_over = FONT_BIG.render('Game Over!', True, WHITE)
            game_over_rect = game_over.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 40))
            self.screen.blit(game_over, game_over_rect)

            # Points text
            points_final = FONT.render(f'Points: {tuple_players[0].points}', True, WHITE)
            points_final_rect = points_final.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 60))
            self.screen.blit(points_final, points_final_rect)
            
        # Multiplayer case
        elif self.PLAY_MODE == 1:
            
            # Case if player 1 died first (his size is < than the minumum)
            if tuple_players[0].size <= tuple_players[0].MIN_SIZE:
                tuple_players[0].draw_dead()
                tuple_players[1].draw(dt)
                game_over = FONT_BIG.render('Player 1 Lost!', True, WHITE)
                game_over_rect = game_over.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 30))
                self.screen.blit(game_over, game_over_rect)
                
            # Case if player 2 died first (his size is < than the minumum)
            elif tuple_players[1].size <= tuple_players[1].MIN_SIZE:
                tuple_players[0].draw(dt)
                tuple_players[1].draw_dead()
                game_over = FONT_BIG.render('Player 2 Lost!', True, WHITE)
                game_over_rect = game_over.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 30))
                self.screen.blit(game_over, game_over_rect)
            
            # On the off chance that somehow both players died at the same time
            else:
                # Game over text
                game_over = FONT_BIG.render('Game Over!', True, WHITE)
                game_over_rect = game_over.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 30))
                self.screen.blit(game_over, game_over_rect)
                for player in tuple_players: player.draw_dead()
                
                
        # Draw time survived text for both singleplayer and multiplayer cases
        time_survived = FONT.render(f'Time survived: {self.game_timer.get_formatted_time()}', True, WHITE)
        time_survived_rect = time_survived.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 20))
        self.screen.blit(time_survived, time_survived_rect)

        # Put work on screen
        pygame.display.flip()

        # Sleep to show end screen
        sleep(3)
        
        # Reset the game_timer object before returning to Menu
        self.game_timer.reset()
        return # <- we go back to the caller