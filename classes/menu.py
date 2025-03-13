import pygame
import sys
from random import choice, randint
from functions.game_files_loader import *
from functions.game_funcs import rot_center
from classes.circle_nom import CircleNom

class Menu: 
    
    # Init pygame
    pygame.init()
    
    # Screen dimentions and modes
    WIDTH, HEIGHT = 1280, 720
    SCREEN_MODES = ["Windowed", "Fullscreen"]
    
    # Colors
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    LIGHT_BLUE = (0, 125, 255)
    
    # Fonts
    FONT = pygame.font.SysFont('Comic Sans MS', 36)
    FONT_BIG = pygame.font.SysFont('Comic Sans MS', 60)
    
    # Main Menu items
    MAIN_MENU_ITEMS = ["Play", "Options", "Quit"]
    
    # Option items
    DIFF_MODES = ["Easy", "Medium", "Hard"]
    PLAY_MODES = ["Singleplayer", "Multiplayer"]
    VOL_LEVELS = ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]    
    
    def __init__(self):  
        
        # Init screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Circle Nom")
        pygame.display.set_icon(pygame.image.load(resource_path('image/others/icon.ico')))
        
        # Init setting values
        self.current_screen_mode = 0
        self.current_difficulty = 0
        self.current_play_mode = 0
        self.current_volume = 5
        self._set_sound_vol(self.current_volume, len(self.VOL_LEVELS) - 1)
        
        # Init options items - WARN: this list will change - check _draw_options()
        self.options_items = ["Volume", "Difficulty", "Play Mode", "Display Mode", "Back"]
        
        # Init selected item for menus
        self.selected_menu_item = 0
        self.selected_options_item = 0
        
        # Angle for player aura rotation
        self.player_aura_angle = 0
        
        # Random background image and player image index
        self.background_image = choice(background_images)
        self.player_image_index = randint(0, len(player_images) - 1)
        
        # End event for music autoplay
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        
    def _set_sound_vol(self, volume:int|float, max_volume:int|float) -> None:
        """
        Set the volume for all game sounds.

        Args:
            volume (int|float): The volume level to set.
            max_volume (int|float): The volume level ceiling.
        """
        # Normalize volume
        volume /= max_volume
        
        # Set volumes
        pygame.mixer.music.set_volume(volume)
        for sound in main_menu_clicks: sound.set_volume(volume)
        for sound in eat_sounds: sound.set_volume(volume)
        for sound in dagger_sounds: sound.set_volume(volume)
        for sound in hit_sounds: sound.set_volume(volume)
    
    def _toggle_screen_mode(self) -> None:
        """
        Toggle between windowed and fullscreen modes.
        """
        main_menu_clicks[1].play()
        self.current_screen_mode = (self.current_screen_mode + 1) % len(self.SCREEN_MODES)
        if self.current_screen_mode == 1: # Fullscreen
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        else: # Windowed
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            
    def _draw_player_and_aura(self) -> None:
        """
        Draw the player and its aura on the screen.
        """
        player_pos = pygame.Vector2(640, 140)
        player_scale = (180, 180)
        
        # Rotate and draw aura
        aura = rot_center(player_aura, self.player_aura_angle, player_pos)
        self.screen.blit(aura[0], aura[1])
        
        # Increment aura for rotation
        self.player_aura_angle = (self.player_aura_angle % 360) - 0.1
        
        # Draw player on top of aura
        player = pygame.transform.smoothscale(player_images[self.player_image_index], player_scale)
        self.screen.blit(player, player_pos - pygame.Vector2(player.get_width()/2, player.get_height()/2))
        
    def _launch_options(self) -> None:
        """
        Launch the options menu.
        """
        # Main loop
        while True:
            
            # Pygame event checker
            for event in pygame.event.get():
                
                # Exit condition if user closes window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                # Key events
                elif event.type == pygame.KEYDOWN:
                    
                    # Enter
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if self.options_items[self.selected_options_item] == "Back":
                            main_menu_clicks[0].play()
                            return # Exit options menu
                        
                    # Backspace
                    elif event.key == pygame.K_BACKSPACE:
                        main_menu_clicks[0].play()
                        return # Exit options menu
                    
                    # Escape
                    elif event.key == pygame.K_ESCAPE:
                        main_menu_clicks[0].play()
                        return # Exit options menu
                        
                    # Movement up - W, ↑
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        main_menu_clicks[0].play()
                        self.selected_options_item = (self.selected_options_item - 1) % len(self.options_items)
                        
                    # Movement down - S, ↓
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        main_menu_clicks[0].play()
                        self.selected_options_item = (self.selected_options_item + 1) % len(self.options_items)
                        
                    # Movement right - D, →
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        
                        # Volume
                        if self.selected_options_item == 0:
                            main_menu_clicks[1].play()
                            self.current_volume = (self.current_volume + 1) % len(self.VOL_LEVELS)
                            self._set_sound_vol(self.current_volume, len(self.VOL_LEVELS) - 1)
                            
                        # Difficulty
                        elif self.selected_options_item == 1:
                            main_menu_clicks[1].play()
                            self.current_difficulty = (self.current_difficulty + 1) % len(self.DIFF_MODES)
                            
                        # Play mode
                        elif self.selected_options_item == 2:
                            main_menu_clicks[1].play()
                            self.current_play_mode = (self.current_play_mode + 1) % len(self.PLAY_MODES)
                            
                        # Screen mode
                        elif self.selected_options_item == 3:
                            main_menu_clicks[1].play()
                            self._toggle_screen_mode()
                            
                    # Movement left - A, ←
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:

                        # Volume
                        if self.selected_options_item == 0:
                            main_menu_clicks[1].play()
                            self.current_volume = (self.current_volume - 1) % len(self.VOL_LEVELS)
                            self._set_sound_vol(self.current_volume, len(self.VOL_LEVELS) - 1)
                            
                        # Difficulty
                        elif self.selected_options_item == 1:
                            main_menu_clicks[1].play()
                            self.current_difficulty = (self.current_difficulty - 1) % len(self.DIFF_MODES)
                            
                        # Play mode
                        elif self.selected_options_item == 2:
                            main_menu_clicks[1].play()
                            self.current_play_mode = (self.current_play_mode - 1) % len(self.PLAY_MODES)
                            
                        # Screen mode
                        elif self.selected_options_item == 3:
                            main_menu_clicks[1].play()
                            self._toggle_screen_mode()
                            
                    # Invalid key presses
                    # Special case if selected option is 1, 2 or 3 - play invalid key press sounds for all keys except W, S, A, D, ↑, ↓, ←, →
                    if self.selected_options_item in [1, 2, 3] and event.key not in [pygame.K_w, pygame.K_UP, pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT, pygame.K_s, pygame.K_DOWN]:
                        main_menu_clicks[2].play()
                            
                    # Special case if selected option is 4 - play invalid key press sound for all keys except Enter, Backspace and Escape
                    elif self.selected_options_item == 4 and event.key not in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_BACKSPACE, pygame.K_ESCAPE, pygame.K_DOWN, pygame.K_UP, pygame.K_w, pygame.K_s]:
                        main_menu_clicks[2].play()
                            
                # Music replay
                elif event.type == pygame.USEREVENT:
                    pygame.mixer.music.load(choice(main_menu_themes))
                    pygame.mixer.music.play()
                        
            # Draw options
            self._draw_options()  
    
    def _draw_options(self):
        """
        Display the options menu on the screen.
        """
        # Draw background, player and title
        self.screen.blit(self.background_image, (0, 0))
        self._draw_player_and_aura()
        title = self.FONT_BIG.render("Options", True, self.WHITE)
        self.screen.blit(title, (self.WIDTH // 2 - title.get_width() // 2, self.HEIGHT // 2 - title.get_height() // 2 - 76))
        
        # Update options items
        self.options_items[0] = f"Volume: {self.VOL_LEVELS[self.current_volume]}"
        self.options_items[1] = f"Difficulty: {self.DIFF_MODES[self.current_difficulty]}"
        self.options_items[2] = f"Play Mode: {self.PLAY_MODES[self.current_play_mode]}"
        self.options_items[3] = f"Display Mode: {self.SCREEN_MODES[self.current_screen_mode]}"
        
        # Draw options items
        for index, item in enumerate(self.options_items):
            
            # Item base colours - LIGHT_BLUE/WHITE <=> selected/deselected
            base_colour = self.WHITE if index != self.selected_options_item else self.LIGHT_BLUE
            
            # Render and display
            text = self.FONT.render(item, True, base_colour)
            self.screen.blit(text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT // 2 - text.get_height() // 2 + index * 42))
            
            # Volume
            if index == 0:
                volume_colour = self.LIGHT_BLUE if index == self.selected_options_item else self.WHITE
                volume_text = self.FONT.render("Volume: ", True, volume_colour)
                self.screen.blit(volume_text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT // 2 - text.get_height() // 2 + index * 42))
                volume_level_text = self.FONT.render(self.VOL_LEVELS[self.current_volume], True, self.WHITE)
                volume_x = self.WIDTH // 2 - text.get_width() // 2 + self.FONT.size("Volume: ")[0]
                self.screen.blit(volume_level_text, (volume_x, self.HEIGHT // 2 - text.get_height() // 2 + index * 42))
                
            # Difficulty
            elif index == 1:
                difficulty_colour = [self.GREEN, self.YELLOW, self.RED][self.current_difficulty]
                difficulty_text = self.FONT.render(self.DIFF_MODES[self.current_difficulty], True, difficulty_colour)
                difficulty_x = self.WIDTH // 2 - text.get_width() // 2 + self.FONT.size("Difficulty: ")[0]
                self.screen.blit(difficulty_text, (difficulty_x, self.HEIGHT // 2 - text.get_height() // 2 + index * 42))
                
            # Play Mode
            elif index == 2:
                play_mode_color = self.LIGHT_BLUE if index == self.selected_options_item else self.WHITE
                play_mode_text = self.FONT.render("Play Mode: ", True, play_mode_color)
                self.screen.blit(play_mode_text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT // 2 - text.get_height() // 2 + index * 42))
                mode_text = self.FONT.render(self.PLAY_MODES[self.current_play_mode], True, self.WHITE)
                mode_x = self.WIDTH // 2 - text.get_width() // 2 + self.FONT.size("Play Mode: ")[0]
                self.screen.blit(mode_text, (mode_x, self.HEIGHT // 2 - text.get_height() // 2 + index * 42))
            
            # Display Mode 
            elif index == 3:
                screen_mode_color = self.LIGHT_BLUE if index == self.selected_options_item else self.WHITE
                screen_mode_text = self.FONT.render("Display Mode: ", True, screen_mode_color)
                self.screen.blit(screen_mode_text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT // 2 - text.get_height() // 2 + index * 42))
                mode_text = self.FONT.render(self.SCREEN_MODES[self.current_screen_mode], True, self.WHITE)
                mode_x = self.WIDTH // 2 - text.get_width() // 2 + self.FONT.size("Display Mode: ")[0]
                self.screen.blit(mode_text, (mode_x, self.HEIGHT // 2 - text.get_height() // 2 + index * 42))
                 
        # Update display
        pygame.display.flip()
        
    def _draw_main_menu(self):
        """
        Display the main menu on the screen.
        """
        # Draw background and player
        self.screen.blit(self.background_image, (0, 0))
        self._draw_player_and_aura()
        
        # Set colours for menu items
        for index, item in enumerate(self.MAIN_MENU_ITEMS):
            
            # Play
            if index == self.selected_menu_item == 0:
                colour = self.GREEN
            
            # Options
            elif index == self.selected_menu_item == 1:
                colour = self.LIGHT_BLUE
                
            # Exit
            elif index == self.selected_menu_item == 2:
                colour = self.RED
                
            # Default
            else:
                colour = self.WHITE
                
            # Draw menu items
            text = self.FONT.render(item, True, colour)
            self.screen.blit(text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT // 2 - text.get_height() // 2 + index * 42))
                
        # Draw title
        title = self.FONT_BIG.render("Circle Nom", True, self.WHITE)
        self.screen.blit(title, (self.WIDTH // 2 - title.get_width() // 2, self.HEIGHT // 2 - title.get_height() // 2 - 76))

        # Update display
        pygame.display.flip()
    
    def _start_game(self):
        """
        Start the Circle Nom game.
        """
        # Select player images from lists
        player_image = player_images[self.player_image_index]
        player_image_dead = player_images_dead[self.player_image_index]
        
        # Define Circle Nom
        game = CircleNom(
            self.screen, self.current_difficulty, self.current_play_mode,
            eat_sounds, theme_songs, player_image, player_image_dead,
            prey_images, prey_aura, self.background_image, health_bar,
            dagger_images, dagger_sounds, hit_sounds
        )
        
        # Start Circle Nom
        game.start()
        
        # New random player images index and background image
        self.player_image_index = randint(0, len(player_images) - 1)
        self.background_image = choice(background_images)
    
    def launch(self):
        """
        Launch the main menu.
        """
        # Functions list for the main menu
        MAIN_MENU_FUNCTIONS = [self._start_game, self._launch_options, sys.exit]
        
        # Play menu theme
        pygame.mixer.music.load(choice(main_menu_themes))
        pygame.mixer.music.play()
        
        # Main loop for main menu
        while True:
            
            # Pygame event checker
            for event in pygame.event.get():
                
                # Exit condition if user closes window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                # Key events
                elif event.type == pygame.KEYDOWN:
                    
                    # Enter
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        main_menu_clicks[0].play()
                        MAIN_MENU_FUNCTIONS[self.selected_menu_item]()
                    
                    # Backspace
                    elif event.key == pygame.K_BACKSPACE:
                        main_menu_clicks[0].play()
                        return # Exit options menu
                    
                    # Escape
                    elif event.key == pygame.K_ESCAPE:
                        main_menu_clicks[0].play()
                        return # Exit options menu
                    
                    # Movement up - W, ↑ 
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        main_menu_clicks[0].play()
                        self.selected_menu_item = (self.selected_menu_item - 1) % len(self.MAIN_MENU_ITEMS)
                        
                    # Movement down - S, ↓ 
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        main_menu_clicks[0].play()
                        self.selected_menu_item = (self.selected_menu_item + 1) % len(self.MAIN_MENU_ITEMS)
                    
                    # Play sound for invalid key press
                    else:
                        main_menu_clicks[2].play()

                # Music replay
                if event.type == pygame.USEREVENT:
                    pygame.mixer.music.load(choice(main_menu_themes))
                    pygame.mixer.music.play()
                    
            # Draw main menu
            self._draw_main_menu()