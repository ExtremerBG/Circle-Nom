# Emko/ExtremerBG was here

# Circle Nom Game

# Importing modules

# Game Systems & Helpers
from circle_nom.helpers.config_reader import ConfigReader
from circle_nom.systems.asset_loader import AssetLoader
import circle_nom.helpers.player_utils as player_utils
import circle_nom.helpers.other_utils as other_utils
from circle_nom.helpers.asset_bank import AssetBank
from circle_nom.systems.logging import get_logger
from circle_nom.systems.timer import Timer
import circle_nom.helpers.debug as debug

# Models
from circle_nom.models.player import Player
from circle_nom.models.dagger import Dagger
from circle_nom.models.prey import Prey

# Others Game elements
from circle_nom.ui.health_bar import HealthBar

# Builtins & Third-party
import random
import pygame
import math
import time
import sys

class CircleNom():
    
    # Static draw positions for different game elements - autoresized with screen resolution
    _SCREEN_SIZE = pygame.display.get_window_size()
    _TIMER_POS = (10, 50)
    _DASH_ICO_POS_1 = (_SCREEN_SIZE[0] - 46, 18)
    _DASH_ICO_POS_2 = (_SCREEN_SIZE[0] / 2.71, 18)
    _POINTS_POS = (10, 10)
    _HLT_BAR_POS_1 = pygame.Vector2(_SCREEN_SIZE[0] - 330, 20)
    _HLT_BAR_POS_2 = pygame.Vector2(188, 20)
    
    # Logger reference
    _LOGGER = get_logger(name=__name__)
    
    # Game asset bank
    _AB = AssetBank()
    
    # Game asset loader
    _AL = AssetLoader()
    
    # Fonts
    FONT_SMALL = pygame.Font(_AB.comic_sans_ms, 15)
    FONT = pygame.Font(_AB.comic_sans_ms, 30)
    FONT_BIG = pygame.Font(_AB.comic_sans_ms, 60)
    
    # Colours
    WHITE = (255, 255, 255)
    
    def __init__(self,
                 screen: pygame.Surface, 
                 fps_cap: int, 
                 difficulty: int,
                 play_mode: int,
                 player_accessory: tuple[pygame.Vector2, pygame.Surface] | None,
                 background_image: pygame.Surface
                 ) -> None:
        """
        Initializes the Circle Nom game with settings and some assets given from the Menu.

        Args:
            screen (pygame.Surface): The Pygame screen object, declared in main.
            fps_cap (int): The FPS the game should run at, selected in the Menu.
            difficulty (int): The game difficulty level, selected in the Menu. Can be 0, 1, 2 or 3 - corresponding to Easy, Medium, Hard and Impossible.
            play_mode (int): The game mode, selected in the Menu. Can be 0 or 1 - corresponding to  Singleplayer or Multiplayer.
            player_accessory (tuple[pygame.Vector2, pygame.Surface] | None): The player's accessory data pair, randomly chosen in the Menu.
            background_image (pygame.Surface): The game's background image, randomly chosen in the Menu.
        """
        # -- Main Objects: declared in Main --
        self.screen = screen
        
        # -- Menu Randoms: chosen by the Menus --
        self.PLAYER_ACCESSORY = player_accessory
        self.BACKGROUND_IMAGE = background_image
        
        # -- Menu Settings: set in the Menus --
        if type(fps_cap) in (int, float):
            self.FPS_CAP = fps_cap
        else:
            self._LOGGER.error(msg="Invalid fps cap. Falling back to 120.")
            self.FPS_CAP = 120
        
        if difficulty in (0, 1, 2, 3):
            self.DIFFICULTY = difficulty
        else:
            self._LOGGER.error(msg="Invalid difficulty level. Falling back to 1 - Medium.")
            self.DIFFICULTY = 1
        
        if play_mode in (0, 1):
            self.PLAY_MODE = play_mode
        else:
            self._LOGGER.error("Invalid play mode level. Falling back to 0 - Singleplayer.")
            self.PLAY_MODE = 0
        
        # -- Calculate game object counts based on the play mode --
        PLAYER_COUNT = self.PLAY_MODE + 1       # 1 or 2 players
        PREY_COUNT = (self.PLAY_MODE  + 1) * 2  # 2 or 4 preys
        DAGGER_COUNT = self.PLAY_MODE  + 1      # 1 or 2 daggers
        
        # -- Difficulty selector:  adjusts balancing attributes --
        # Prey
        EASY_CD, MEDIUM_CD, HARD_CD, IMPOSSIBLE_CD = ConfigReader.get_prey_difficulty()
        if self.DIFFICULTY == 0:    # Easy
            Prey.set_spawned_duration(new_duration=EASY_CD)
        elif self.DIFFICULTY == 1:  # Medium
            Prey.set_spawned_duration(new_duration=MEDIUM_CD)
        elif self.DIFFICULTY == 2:  # Hard
            Prey.set_spawned_duration(new_duration=HARD_CD)
        elif self.DIFFICULTY == 3:  # Impossible
            Prey.set_spawned_duration(new_duration=IMPOSSIBLE_CD)
            
        # Dagger
        EASY_CD, MEDIUM_CD, HARD_CD, IMPOSSIBLE_CD = ConfigReader.get_dagger_difficulty()
        if self.DIFFICULTY == 0:    # Easy
            Dagger.set_spawnrate(new_spawnrate=EASY_CD)
        elif self.DIFFICULTY == 1:  # Medium
            Dagger.set_spawnrate(new_spawnrate=MEDIUM_CD)
        elif self.DIFFICULTY == 2:  # Hard
            Dagger.set_spawnrate(new_spawnrate=HARD_CD)
        elif self.DIFFICULTY == 3:  # Impossible
            Dagger.set_spawnrate(new_spawnrate=IMPOSSIBLE_CD)
            
        # -- Engine objects: Declared in the Engine --
        self.game_timer = Timer(name="EngineTimerThread")

        # -- Declaring game models --
        # Player
        # Decide if Easter mode will be active - if it is, reverse Player/Prey images
        self.EASTER_MODE = random.randint(a=0, b=100) < ConfigReader.get_easter_chance()
        if not self.EASTER_MODE: 
            self.tuple_players: tuple[Player, ...] = other_utils.declare_objects(
                PLAYER_COUNT, 
                Player, self.screen, self.game_timer, self.EASTER_MODE,
                self._AB.player_image, self._AB.player_image_dead, self._AB.player_eat_sequence, self.PLAYER_ACCESSORY
            )
        else:            
            TEMP_easter_player_image = random.choice(self._AB.prey_images)
            self.tuple_players: tuple[Player, ...] = other_utils.declare_objects(
                PLAYER_COUNT, 
                Player, self.screen, self.game_timer, self.EASTER_MODE,
                TEMP_easter_player_image, TEMP_easter_player_image, None, None
            ) # Dont use player eat sequence and player accessory for easter mode
            
            # Create a new temporary prey images list
            TEMP_prey_images = []

            # Add all player images to prey list instead
            TEMP_prey_images.append(pygame.transform.smoothscale(self._AB.player_image, (64, 64)))
            TEMP_prey_images.append(pygame.transform.smoothscale(self._AB.player_image_dead, (64, 64)))
        
        # Preys declaration
        if not self.EASTER_MODE:
            self.tuple_preys: tuple[Prey] = other_utils.declare_objects(
                PREY_COUNT, Prey, self.screen, self.game_timer,
                self._AB.prey_images, self._AB.prey_aura
            )
        else:
            self.tuple_preys: tuple[Prey] = other_utils.declare_objects(
                PREY_COUNT, Prey, self.screen, self.game_timer,
                TEMP_prey_images, self._AB.prey_aura
            )
            
        # Health bar declaration
        self.health_bar = HealthBar(self._AB.health_bar, self.screen)

        # Dagger/s declaration
        self.tuple_daggers: tuple[Dagger] = other_utils.declare_objects(
            DAGGER_COUNT, Dagger, self.screen, self.game_timer,
            self._AB.dagger_images, self._AB.dagger_sounds, self._AB.flame_sequence
        )
        
        # Dagger/s initial grace period
        for dagger in self.tuple_daggers:
            dagger.grace_spawn(random.uniform(3, 4))
        
        # Log the Circle Nom init
        TEMP_diff_to_str = {0: "Easy", 1: "Medium", 2: "Hard", 3: "Impossible"}
        TEMP_mode_to_str = {0: "Singleplayer", 1: "Multiplayer"}
        log_str = (
            "Circle Nom game initialized successfully with " 
            f"difficulty {TEMP_diff_to_str[self.DIFFICULTY]}, play mode {TEMP_mode_to_str[self.PLAY_MODE]}, "
            f"easter mode {self.EASTER_MODE}, FPS Cap {self.FPS_CAP}."
        )
        self._LOGGER.info(log_str)
        
    def _try_eat_prey(self) -> None:
        """
        Checks if any Player is near any Prey object using the Player's eat position, eat tolerance and math.isclose. \n
        If it is, apply size, speed and points increase to the Player and reset the Prey to effectively "eat" it.
        """
        for player in self.tuple_players:
            for prey in self.tuple_preys:
                if math.isclose(player.eat_pos.x, prey.position.x, abs_tol=player.eat_tol) and \
                    math.isclose(player.eat_pos.y, prey.position.y, abs_tol=player.eat_tol) and \
                        prey.eatable and player.can_eat:
                    
                    # Bonus points for aura'd prey
                    if prey.aura:
                        player.size += 20
                        player.speed += 16
                        player.speed_before_dash += 16
                        player.points += 2
                    else:
                        player.size += 10
                        player.speed += 8
                        player.speed_before_dash += 8
                        player.points += 1
                            
                    # Play eat random sound
                    random.choice(self._AB.player_eat_sounds).play()
                    
                    # Reset player and prey
                    prey.reset_prey()
                    player.reset_eat_attributes()
                    
                    # Log the prey eat
                    self._LOGGER.info(f"Player ate prey at X {prey.position.x:.2f} Y {prey.position.y:.2f}, aura {prey.aura}.")
        
    def _try_hit_dagger(self) -> None:
        """
        Checks if any Player is near any Dagger object using the Player's hit position, hit tolerance and math.isclose. \n
        If it is, apply size, speed reductions to the Player and reset the Dagger to effectively make the Player get hit by the Dagger. 
        """
        for player in self.tuple_players:
            for dagger in self.tuple_daggers:
                if math.isclose(player.hit_pos.x, dagger.position.x, abs_tol=player.hit_tol) and \
                    math.isclose(player.hit_pos.y, dagger.position.y, abs_tol=player.hit_tol):
                        
                    # Bigger penalty if its a flaming dagger
                    if dagger.flame:
                        player.size -= 15
                        player.speed -= 5
                    else:
                        player.size -= 10
                        
                    # First reset dagger & player
                    dagger.reset_dagger()
                    player.reset_hurt_attributes()
                    
                    # If player is hit dagger spawn will have a grace period where no Dagger will spawn
                    dagger.grace_spawn(random.uniform(1, 2))
                    
                    # Play random sound 
                    random.choice(self._AB.player_hit_sounds).play()
                    
                    # Log the hit
                    self._LOGGER.info(f"Player hit with dagger at X {dagger.position.x:.2f} Y {dagger.position.y:.2f}, flame {dagger.flame}.")
                    
    def _music_player(self, index: int) -> str:
        """Plays music from the game_themes list with the given index. Returns the song name."""
        if type(index) != int:
            raise ValueError("Index must be integer!")
            
        pygame.mixer.music.unload()
        music_name, music_path = self._AB.game_themes[index % len(self._AB.game_themes)]
        self._AL.load_music(music_path)
        pygame.mixer.music.play()
        self._LOGGER.info(f"Playing music {music_name} with index {index}.")
        return music_name

    def start(self) -> None:
        """Starts the Circle Nom game."""
        # Play random theme song from the game themes
        song_index = random.randint(0, len(self._AB.game_themes) - 1)
        music_name = self._music_player(song_index)

        # Delta time from last game frame
        dt = 0.00
        
        # Pygame clock - used for limiting the FPS and calculating dt
        clock = pygame.time.Clock()
        
        # Pause - Skips over game loop, excluding event checker and pause screen
        paused = False

        # Running - Keeps the entire game loop running
        running = True
        
        # Start game_timer before entering game loop
        self.game_timer.start()
        
        # Log the start of the game
        self._LOGGER.info(f"Circle Nom started.")
        
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
                    music_name = self._music_player(song_index)

                # Key event checker - part of EVENT CHECKER
                if event.type == pygame.KEYDOWN:
                    
                    # Escape
                    if event.key == pygame.K_ESCAPE:
                        running = False # break gameloop
                        pygame.mixer.music.unpause()
                        
                    # Game pause/unpause - P
                    elif event.key == pygame.K_p:
                        paused = not paused
                        if paused:
                            self.game_timer.stop()
                            pygame.mixer.music.pause()
                        else:
                            self.game_timer.start()
                            pygame.mixer.music.unpause()

                    # Music changer - works only when game is not paused
                    if not paused:

                        # Forward in list songs
                        if event.key == pygame.K_e:
                            song_index += 1
                            music_name = self._music_player(song_index)

                        # Backward in list songs
                        elif event.key == pygame.K_q:
                            song_index -= 1
                            music_name = self._music_player(song_index)
                            
            # --------------------------------------------------------------------------------------------
            # GAME LOOP - CAN BE PAUSED
            if not paused:
                
                # Fill the screen with background image to wipe away anything from last frame
                self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))
                
                # Process all Game models in draw order Daggers -> Players -> Preys
                for dagger in self.tuple_daggers:
                    dagger.draw(dt)
                    
                    # Play sound if its on screen
                    if 0 <= dagger.position.x <= self.screen.width and \
                        0 <= dagger.position.y <= self.screen.height:
                        dagger.play_sound()
                        
                for player in self.tuple_players:
                    player.draw(dt)
                    
                    # Reduce Player size and speed
                    player.size -= player_utils.get_size_reduct(player, dt)  
                    player.speed -= 5 * dt
                    
                for prey in self.tuple_preys:
                    prey.draw(dt)
                    
                # Run the other methods required
                self._try_eat_prey()
                self._try_hit_dagger()
                    
                # After all model processing is done check if the Game is over (Player is < the minimum size)
                if player.size <= player.MIN_SIZE:
                    running = False
                        
                # Debug functions
                debug.player(players=self.tuple_players, player_n=0, screen=self.screen)
                debug.prey(preys=self.tuple_preys, prey_n=0, screen=self.screen)
                debug.dagger(daggers=self.tuple_daggers, dagger_n=0, screen=self.screen) 

                # FPS Text display
                other_utils.draw_fps(self.screen, clock, self.FONT_SMALL)
                
                # Time elapsed display
                self.screen.blit(self.FONT_SMALL.render(f"Time elapsed: {self.game_timer.get_formatted_time()}", True, self.WHITE), self._TIMER_POS)

                # Song name display
                other_utils.draw_music_name(self.screen, music_name, self.FONT_SMALL)
                
                # Dash image display
                # Singleplayer case
                if self.PLAY_MODE == 0:
                    if self.tuple_players[0].dash_available:
                        self.screen.blit(self._AB.dash_images["AVAIL"], self._DASH_ICO_POS_1)
                    else:
                        self.screen.blit(self._AB.dash_images["UNAVAIL"], self._DASH_ICO_POS_1)
                # Multiplayer case
                elif self.PLAY_MODE == 1:
                    # Player 1
                    if self.tuple_players[0].dash_available:
                        self.screen.blit(self._AB.dash_images["AVAIL"], self._DASH_ICO_POS_2)
                    else:
                        self.screen.blit(self._AB.dash_images["UNAVAIL"], self._DASH_ICO_POS_2)
                    # Player 2
                    if self.tuple_players[1].dash_available:
                        self.screen.blit(self._AB.dash_images["AVAIL"], self._DASH_ICO_POS_1)
                    else:
                        self.screen.blit(self._AB.dash_images["UNAVAIL"], self._DASH_ICO_POS_1)

                # Points text display - only for singleplayer
                if self.PLAY_MODE == 0:
                    points_text = self.FONT.render(f'Points: {self.tuple_players[0].points}', True, self.WHITE)
                    self.screen.blit(points_text, self._POINTS_POS)
                
                # Health bar display
                # Singleplayer case
                if self.PLAY_MODE == 0:
                    self.health_bar.draw("Health:", self.tuple_players[0].size, self.tuple_players[0].MAX_SIZE, self.tuple_players[0].MIN_SIZE, 
                                    coords=self._HLT_BAR_POS_1)
                
                # Multiplayer case
                elif self.PLAY_MODE == 1:   
                    self.health_bar.draw("Player 1 Health:", 
                                    self.tuple_players[0].size, self.tuple_players[0].MAX_SIZE, self.tuple_players[0].MIN_SIZE, 
                                    coords=self._HLT_BAR_POS_2)
                    self.health_bar.draw("Player 2 Health:", 
                                    self.tuple_players[1].size, self.tuple_players[1].MAX_SIZE, self.tuple_players[1].MIN_SIZE, 
                                    coords=self._HLT_BAR_POS_1)

                # Controls for Player/s
                # Singleplayer case
                if self.PLAY_MODE == 0:
                    
                    # Enable both control options for singleplayer since we have only one player
                    player_utils.control_movement(self.tuple_players[0], dt, arrows=True, wasd=True)
                    player_utils.check_bounds(self.screen, self.tuple_players[0]) # Keeps player in screen area
                
                # Multiplayer case
                elif self.PLAY_MODE == 1:
                    
                    # Player 1 gets only WASD controls
                    player_utils.control_movement(player=self.tuple_players[0], dt=dt, arrows=False, wasd=True)
                    player_utils.check_bounds(screen=self.screen, player=self.tuple_players[0])
                    
                    # Player 2 gets ARROWS controls
                    player_utils.control_movement(player=self.tuple_players[1], dt=dt, arrows=True, wasd=False)
                    player_utils.check_bounds(screen=self.screen, player=self.tuple_players[1])
                    
                    # This checks if both players are near eachother and pushes them appart if they are
                    player_utils.check_collision(player_1=self.tuple_players[0], player_2=self.tuple_players[1], dt=dt)
                    
            # -------------------------------------------------------------------------------------------- 
            # PAUSE SCREEN
            else:
                
                # Background and Player/s
                self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))
                for player in self.tuple_players: player.draw(dt)

                # Game paused text
                paused_text = self.FONT_BIG.render('Game Paused', True, self.WHITE)
                paused_text_rect = paused_text.get_rect(center=(self.screen.width / 2, self.screen.height / 2 - 30))
                self.screen.blit(paused_text, paused_text_rect)

                # Press 'P' text
                press_text = self.FONT.render("Press 'P' to unpause", True, self.WHITE)
                press_text_rect = press_text.get_rect(center=(self.screen.width / 2, self.screen.height / 2 + 30))
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
            self.tuple_players[0].draw_dead()

            # Game over text
            game_over = self.FONT_BIG.render('Game Over!', True, self.WHITE)
            game_over_rect = game_over.get_rect(center=(self.screen.width / 2, self.screen.height / 2 - 40))
            self.screen.blit(game_over, game_over_rect)

            # Points text
            points_final = self.FONT.render(f'Points: {self.tuple_players[0].points}', True, self.WHITE)
            points_final_rect = points_final.get_rect(center=(self.screen.width / 2, self.screen.height / 2 + 60))
            self.screen.blit(points_final, points_final_rect)
            
        # Multiplayer case
        elif self.PLAY_MODE == 1:
            
            # Case if Player 1 died first (his size is < than the minumum)
            if self.tuple_players[0].size <= self.tuple_players[0].MIN_SIZE:
                self.tuple_players[0].draw_dead()
                self.tuple_players[1].draw(dt)
                game_over = self.FONT_BIG.render('Player 1 Lost!', True, self.WHITE)
                game_over_rect = game_over.get_rect(center=(self.screen.width / 2, self.screen.height / 2 - 30))
                self.screen.blit(game_over, game_over_rect)
                
            # Case if Player 2 died first (his size is < than the minumum)
            elif self.tuple_players[1].size <= self.tuple_players[1].MIN_SIZE:
                self.tuple_players[0].draw(dt)
                self.tuple_players[1].draw_dead()
                game_over = self.FONT_BIG.render('Player 2 Lost!', True, self.WHITE)
                game_over_rect = game_over.get_rect(center=(self.screen.width / 2, self.screen.height / 2 - 30))
                self.screen.blit(game_over, game_over_rect)
            
            # On the off chance that somehow both Players died at the same time
            else:
                # Game over text
                game_over = self.FONT_BIG.render('Draw!', True, self.WHITE)
                game_over_rect = game_over.get_rect(center=(self.screen.width / 2, self.screen.height / 2 - 30))
                self.screen.blit(game_over, game_over_rect)
                for player in self.tuple_players: player.draw_dead()
                
        # Draw time survived text for both singleplayer and multiplayer cases
        time_survived = self.FONT.render(f'Time survived: {self.game_timer.get_formatted_time()}', True, self.WHITE)
        time_survived_rect = time_survived.get_rect(center=(self.screen.width / 2, self.screen.height / 2 + 20))
        self.screen.blit(time_survived, time_survived_rect)

        # Put work on screen
        pygame.display.flip()
        
        # Sleep to show end screen
        time.sleep(3)
        
        # Log the game end
        self._LOGGER.info(f"Circle Nom game ended. Total in-game time {self.game_timer.get_time():.2f}s, final score {player.points}.")
        
        # Reset the game_timer object before returning to caller
        self.game_timer.reset()
        return