from models.circle_nom import CircleNom
from random import choice, randint
from helpers.file_loader import *
from helpers.functions import *
from math import sin
import pygame
import sys

class Menu:
    
    # Colors
    WHITE = 255, 255, 255
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    YELLOW = 255, 255, 0
    GOLD = 255, 169, 0
    LIGHT_PURPLE = 118, 127, 248
    LIGHT_BLUE = 0, 125, 255
    BLACK = 0, 0, 0
    LIGHT_GREY_ALPHA = 110, 110, 110, 96
    
    # Fonts
    FONT_SMALL = pygame.font.SysFont('Comic Sans MS', 15)
    FONT = pygame.font.SysFont('Comic Sans MS', 40)
    FONT_BIG = pygame.font.SysFont('Comic Sans MS', 65)
    
    # Main Menu items - Item and RGB Values
    MAIN_MENU_ITEMS = (("Play", GREEN), ("Options", LIGHT_BLUE), ("Quit", RED))
    
    # Option items - Item and RGB/HEX Values
    VOL_LEVELS = (
        ("0", "#0075ff"), ("10", "#03cffe"), ("20", "#06fcd3"), ("30", "#08fb7c"), 
        ("40", "#0bfa29"), ("50", "#44f80e"), ("60", "#97f710"), ("70", "#e8f613"), 
        ("80", "#f4b316"), ("90", "#f36618"), ("100", "#f21b1b")
    )
    
    DIFF_MODES = (("Easy", GREEN), ("Medium", YELLOW), ("Hard", RED))
    FPS_CAPS = (
        ("30", "#ff0000"), ("60", "#ff0039"), ("75", "#ff075f"), ("120", "#ff207d"), 
        ("144", "#ff2a9a"), ("240", "#ff2db8"), ("360", "#ff22dd"), ("Unlimited", "#f942ff")
    )
    PLAY_MODES = (("Singleplayer", "#94f21c"), ("Multiplayer", "#0acffa"))
    SCREEN_MODES = (("Windowed", "#fa0a35"), ("Fullscreen", (173, 255, 0)))
    
    def __init__(self, screen: pygame.Surface) -> None:  
        
        # Pygame clock for framerate
        self.clock = pygame.time.Clock()
            
        # Delta time
        self.dt = 0
            
        # FPS limiter
        self._fps_cap = 60
        
        # Setup pygame screen
        self.screen = screen
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Circle Nom")
        self.WIDTH, self.HEIGHT = pygame.display.get_window_size()
        
        # Inititial setting values
        self.current_volume = 5
        self.current_fps_cap = 3
        self.current_difficulty = 1
        self.current_play_mode = 0
        self.current_screen_mode = 0
        
        # Set settings based on initial values
        self._set_sound_vol(self.current_volume, len(self.VOL_LEVELS) - 1)
        self.fps_cap = self.FPS_CAPS[self.current_fps_cap][0]
        
        # Options items dictionary based on Initial setting values
        self.options_items = {
                "Volume": self.VOL_LEVELS[self.current_volume], 
                "FPS Cap": self.FPS_CAPS[self.current_fps_cap], 
                "Difficulty": self.DIFF_MODES[self.current_difficulty], 
                "Mode": self.PLAY_MODES[self.current_play_mode], 
                "Display": self.SCREEN_MODES[self.current_screen_mode],
                "Back": None
            }
        
        # Inititial selected item for menus
        self.selected_menu_item = 0
        self.selected_options_item = 5
        
        # Random background image and player image index
        self.background_image = choice(background_images)
        self.player_image_index = randint(0, len(player_images) - 1)
        
        # Player aura method var and consts
        self.player_aura_angle = 0
        self.PLAYER_POS = pygame.Vector2(self.WIDTH / 2, self.HEIGHT / 5.14)
        self.PLAYER_SCALE = (180, 180)
        self.PLAYER_IMG = pygame.transform.smoothscale(player_images[self.player_image_index], self.PLAYER_SCALE)
        self.PLAYER_BLIT_POS = self.PLAYER_POS - pygame.Vector2(self.PLAYER_IMG.get_width() / 2, self.PLAYER_IMG.get_height() / 2)
        
        # Load random menu theme song
        self.song_name, self.song_path = choice(menu_themes)
        load_music(self.song_path)
        
        # End event for music autoplay
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        # Create a cursor from the image
        pg_cursor = pygame.cursors.Cursor((8, 8), cursor_surface)  # Hotspot at (16, 16)
        pygame.mouse.set_cursor(pg_cursor)
        
        # Title timer - used for smooth colour shift
        self.menu_title_timer = 0
        
        
    @property
    def fps_cap(self):
        """
        Get the fps cap.
        """
        return self._fps_cap
    
    @fps_cap.setter
    def fps_cap(self, value):
        """
        Cap the pygame's FPS with the given value.
        
        Args:
            value (str): The fps value. Takes string and converts to int. If it fails, value = 0 (no limit).
        """
        try:
            self._fps_cap = int(value)
        except ValueError:
            self._fps_cap = 0
        
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
        for sound in menu_clicks.values(): sound.set_volume(volume)
        for sound in eat_sounds: sound.set_volume(volume)
        for sound in dagger_sounds: sound.set_volume(volume)
        for sound in hit_sounds: sound.set_volume(volume)
        for sound in dash_sounds: sound.set_volume(volume)
    
    def _toggle_screen_mode(self) -> None:
        """
        Toggle between windowed and fullscreen modes.
        """
        if self.current_screen_mode == 1: # Fullscreen
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        else: # Windowed
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            
    def _draw_player_and_aura(self) -> None:
        """
        Draw the player and its aura on the screen.
        """
        # Rotate and draw aura
        aura = rot_center(player_aura, self.player_aura_angle, self.PLAYER_POS)
        self.screen.blit(aura[0], aura[1])
        
        # Increment aura for rotation
        self.player_aura_angle = (self.player_aura_angle % 360) - 24 * self.dt
        
        # Draw player on top of aura
        self.screen.blit(self.PLAYER_IMG, self.PLAYER_BLIT_POS)
        
    def _cursor_click_menu_item(self, item_pos: tuple, item_size: tuple) -> bool:
        """
        Check if cursor is clicking on a menu item.
        """
        mousepos = pygame.mouse.get_pos()
        rect = pygame.Rect(item_pos, item_size)
        
        if rect.collidepoint(mousepos):
            pygame.draw.rect(self.screen, color=self.GREEN, rect=rect)
            return True
        else:
            pygame.draw.rect(self.screen, color=self.RED, rect=rect)
            return False
        
    def _options_movement_horizontal(self, move_step: int):
        """
        Handle moving horizontally in the options menu.
        """
        
        # Volume
        if self.selected_options_item == 0:
            self.current_volume = (self.current_volume + move_step) % len(self.VOL_LEVELS)
            self._set_sound_vol(self.current_volume, len(self.VOL_LEVELS) - 1)
                            
        # FPS Cap
        elif self.selected_options_item == 1:
            self.current_fps_cap = (self.current_fps_cap + move_step) % len(self.FPS_CAPS)
            self.fps_cap = self.FPS_CAPS[self.current_fps_cap][0]
                            
        # Difficulty
        elif self.selected_options_item == 2:
            self.current_difficulty = (self.current_difficulty + move_step) % len(self.DIFF_MODES)
                            
        # Play mode
        elif self.selected_options_item == 3:
            self.current_play_mode = (self.current_play_mode + move_step) % len(self.PLAY_MODES)
                            
        # Screen mode
        elif self.selected_options_item == 4:
            self.current_screen_mode = (self.current_screen_mode + move_step) % len(self.SCREEN_MODES)
            self._toggle_screen_mode()
        
        # Play sounds - options that have horizontal - LEFTRIGHT, others - UNKNOWN  
        if self.selected_options_item in (0, 1, 2, 3, 4):
            menu_clicks["LEFTRIGHT"].play()
        else:
            menu_clicks["UNKNOWN"].play()
            
            
    def _calc_menu_item_pos(self, text_width: int, text_height: int, index: int) -> tuple[int, int]:
        """
        Calculate centered X, Y coordinates with its index for Y offset. Used for menu ITEMS only.
        """
        return self.WIDTH // 2 - text_width // 2, self.HEIGHT // 2 - text_height // 2 + index * 45
    
    def _calc_menu_title_pos(self, title: pygame.Surface) -> tuple[int, int]:
        """
        Calculate centered X, Y coordinates of the given text Surface. Used for menu TITLES ONLY.
        """
        return self.WIDTH // 2 - title.get_width() // 2, self.HEIGHT // 2 - title.get_height() // 2 - 76
    
    def _render_gradient_title(self, title: str, colour1: tuple[int, int, int], 
                             colour2: tuple[int, int, int]) -> pygame.Surface:
        """
        Draw a title that changes colours from colour1 -> colour2 smoothly.
        """
        # Update time for smooth transition
        self.menu_title_timer += 3 * self.dt  # Speed control
        
        # Smoothly interpolate colors using a sine wave
        fade = (sin(self.menu_title_timer) + 1) / 2  # Oscillates between 0 and 1
        r = int(colour1[0] * (1 - fade) + colour2[0] * fade)
        g = int(colour1[1] * (1 - fade) + colour2[1] * fade)
        b = int(colour1[2] * (1 - fade) + colour2[2] * fade)
        
        # Render text with the generated colour
        return self.FONT_BIG.render(title, True, (r, g, b))
    
    def _launch_options(self) -> None:
        """
        Launch the options menu.
        """
        # Sound timer for limiting click sounds
        mouse_sound_timer = menu_clicks["UPDOWN"].get_length()
        while True:
            
            # Rects from draw options menu - used with mousepos
            item_rects = self._draw_options()
            mousepos = pygame.mouse.get_pos()
            
            # Pygame event checker
            for event in pygame.event.get():
                
                # Exit condition if user closes window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
                # Mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    
                    # Highlight item under mouse
                    for idx, rect in enumerate(item_rects):
                        if rect.collidepoint(mousepos):
                            if self.selected_options_item != idx:
                                self.selected_options_item = idx
                                if mouse_sound_timer <= 0:
                                    menu_clicks["UPDOWN"].play()
                                    mouse_sound_timer = menu_clicks["UPDOWN"].get_length()
                            break
                
                # Mouse key events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                        
                    # Left click on Back option
                    if event.button == 1 and self.selected_options_item == 5: # Back is located at index 5
                        menu_clicks["UPDOWN"].play()
                        return
                    
                    # Right click on Back option
                    elif event.button == 3 and self.selected_options_item == 5:
                        menu_clicks["UNKNOWN"].play()
                    
                    # Right click horizontal options
                    elif event.button == 3 and self.selected_options_item in (0, 1, 2, 3, 4):
                        self._options_movement_horizontal(move_step=1)
                        
                    # Left click on horizontal options
                    elif event.button == 1 and self.selected_options_item in (0, 1, 2, 3, 4):
                        self._options_movement_horizontal(move_step=-1)
                    
                # Keyboard events
                elif event.type == pygame.KEYDOWN:
                    
                    # Enter
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if self.selected_options_item == 5: # Back is located at index 5
                            menu_clicks["UPDOWN"].play()
                            return # Exit options menu
                        
                    # Backspace or Escape
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                        menu_clicks["UPDOWN"].play()
                        return # Exit options menu
                        
                    # Movement up - W, ↑
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        menu_clicks["UPDOWN"].play()
                        self.selected_options_item = (self.selected_options_item - 1) % len(self.options_items)
                        
                    # Movement down - S, ↓
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        menu_clicks["UPDOWN"].play()
                        self.selected_options_item = (self.selected_options_item + 1) % len(self.options_items)
                        
                    # Movement right - D, →
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self._options_movement_horizontal(move_step=1)
                            
                    # Movement left - A, ←
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self._options_movement_horizontal(move_step=-1)
                            
                # Music end event - Replay
                elif event.type == pygame.USEREVENT:
                    self.song_name, self.song_path = choice(menu_themes)
                    load_music(self.song_path)
                    pygame.mixer.music.play()
                        
            mouse_sound_timer -= 4 * self.dt
    
    def _draw_options(self) -> list[pygame.Rect]:
        """
        Display the options menu on the screen.
        """
        self.screen.blit(self.background_image, (0, 0))
        self._draw_player_and_aura()
        draw_fps(self.screen, self.clock, self.FONT_SMALL)

        # Update options items
        self.options_items["Volume"] = self.VOL_LEVELS[self.current_volume]
        self.options_items["FPS Cap"] = self.FPS_CAPS[self.current_fps_cap]
        self.options_items["Difficulty"] = self.DIFF_MODES[self.current_difficulty]
        self.options_items["Mode"] = self.PLAY_MODES[self.current_play_mode]
        self.options_items["Display"] = self.SCREEN_MODES[self.current_screen_mode]
        
        # Draw options items & add rects
        index = 0
        option_rects = []
        for key, value in self.options_items.items():
            
            # Key colours - LIGHT_BLUE/WHITE <=> selected/deselected
            key_colour = self.LIGHT_BLUE if index == self.selected_options_item else self.WHITE
             
            # Case for all options with horizontal movement
            if value is not None:

                # Render texts and set colour for value
                key_text = self.FONT.render(f"{key}: ", True, key_colour)
                # value holds tuple("TEXT", (255, 255, 0)) - containing text and rgb value
                value_text = self.FONT.render(f"< {value[0]} >", True, value[1])
                
                # Calculate text position
                total_width = key_text.get_width() + value_text.get_width()
                total_height = max(key_text.get_height(), value_text.get_height())
                x, y = self._calc_menu_item_pos(total_width, total_height, index)
                
                # Blit both texts & create rect
                self.screen.blit(key_text, (x, y))
                self.screen.blit(value_text, (x + key_text.get_width(), y))
                item_rect = pygame.Rect(x, y, total_width, total_height)
                
            # Case for Back option (no horizontal movement)
            else:
                # Render text & calculate position
                key_text = self.FONT.render(f"{key}", True, key_colour)
                x, y = self._calc_menu_item_pos(key_text.get_width(), key_text.get_height(), index)
                
                # Blit and create rect
                self.screen.blit(key_text, (x, y))
                item_rect = pygame.Rect(x, y, total_width, total_height)
            
            # Append created rect from item for returning & increment index
            option_rects.append(item_rect)
            index += 1
                
        # Draw song name
        self.screen.blit(self.FONT_SMALL.render(self.song_name, True, self.WHITE), (10, 695))
        
        # Draw gradient title
        title = self._render_gradient_title("Options", self.LIGHT_BLUE, self.LIGHT_PURPLE)
        self.screen.blit(title, self._calc_menu_title_pos(title))
        
        # Update display
        pygame.display.flip()
        
        # Limit FPS to 60. Set delta time.
        self.dt = self.clock.tick(self.fps_cap) / 1000
        return option_rects
        
    def _draw_main_menu(self) -> list[pygame.Rect]:
        """
        Display the main menu on the screen.
        """
        self.screen.blit(self.background_image, (0, 0))
        self._draw_player_and_aura()
        draw_fps(self.screen, self.clock, self.FONT_SMALL)
        
        # Set colours for menu items
        main_menu_rects = []
        for index, item in enumerate(self.MAIN_MENU_ITEMS):
                
            # Draw menu item with its colour if its selected
            if self.selected_menu_item == index:
                text = self.FONT.render(item[0], True, item[1])
            else:
                # Draw with white colour if not
                text = self.FONT.render(item[0], True, self.WHITE)
            
            # Calculate text position, create Rect and display text
            x, y = self._calc_menu_item_pos(text.get_width(), text.get_height(), index)
            item_rect = pygame.Rect(x, y, text.get_width(), text.get_height())
            main_menu_rects.append(item_rect)
            self.screen.blit(text, (x, y))
                
        # Draw title
        title = self.FONT_BIG.render("Circle Nom", True, self.WHITE)
        self.screen.blit(title, self._calc_menu_title_pos(title))
        
        # Draw song name
        self.screen.blit(self.FONT_SMALL.render(self.song_name, True, self.WHITE), (10, 695))
        
        # Draw gradient title
        title = self._render_gradient_title("Circle Nom", self.GOLD, self.YELLOW)
        self.screen.blit(title, self._calc_menu_title_pos(title))

        # Update display
        pygame.display.flip()
        
        # Limit FPS to 60. Set delta time.
        self.dt = self.clock.tick(self.fps_cap) / 1000
        return main_menu_rects
    
    def _start_game(self) -> None:
        """
        Start the Circle Nom game.
        """
        # Select player images from lists
        player_image = player_images[self.player_image_index]
        player_image_dead = player_images_dead[self.player_image_index]
        
        # Define Circle Nom
        game = CircleNom(
            self.screen, self.fps_cap, self.current_difficulty, self.current_play_mode,
            eat_sounds, game_themes, player_image, player_image_dead,
            prey_images, prey_aura, self.background_image, health_bar,
            dagger_images, dagger_sounds, flame_sequence, hit_sounds, dash_images
        )
        
        # Start Circle Nom
        game.start()
        
        # New random player images index and background image
        self.player_image_index = randint(0, len(player_images) - 1)
        self.background_image = choice(background_images)
    
    def launch_main(self) -> None:
        """
        Launch the main menu.
        """
        # Functions list for the main menu
        MAIN_MENU_FUNCTIONS = [self._start_game, self._launch_options, sys.exit]
        
        # Play menu theme
        pygame.mixer.music.play()
        
        # Sound timer for limiting click sounds
        mouse_sound_timer = menu_clicks["UPDOWN"].get_length()
        while True:
            
            # Rects from draw options menu - used with mousepos
            item_rects = self._draw_main_menu()
            mousepos = pygame.mouse.get_pos()
            
            # Pygame event checker
            for event in pygame.event.get():
                
                # Exit condition if user closes window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
                # Mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    
                    # Highlight item under mouse
                    for idx, rect in enumerate(item_rects):
                        if rect.collidepoint(mousepos):
                            if self.selected_menu_item != idx:
                                self.selected_menu_item = idx
                                if mouse_sound_timer <= 0:
                                    menu_clicks["UPDOWN"].play()
                                    mouse_sound_timer = menu_clicks["UPDOWN"].get_length()
                            break
                
                # Mouse key events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Left click
                    if event.button == 1:
                        menu_clicks["UPDOWN"].play()
                        MAIN_MENU_FUNCTIONS[self.selected_menu_item]()
                    
                # Key events
                elif event.type == pygame.KEYDOWN:
                    
                    # Enter
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        menu_clicks["UPDOWN"].play()
                        MAIN_MENU_FUNCTIONS[self.selected_menu_item]()
                    
                    # Backspace
                    elif event.key == pygame.K_BACKSPACE:
                        menu_clicks["UPDOWN"].play()
                        return # Exit options menu
                    
                    # Escape
                    elif event.key == pygame.K_ESCAPE:
                        menu_clicks["UPDOWN"].play()
                        return # Exit options menu
                    
                    # Movement up - W, ↑ 
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        menu_clicks["UPDOWN"].play()
                        self.selected_menu_item = (self.selected_menu_item - 1) % len(self.MAIN_MENU_ITEMS)
                        
                    # Movement down - S, ↓ 
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        menu_clicks["UPDOWN"].play()
                        self.selected_menu_item = (self.selected_menu_item + 1) % len(self.MAIN_MENU_ITEMS)
                    
                    # Play sound for invalid key press
                    else:
                        menu_clicks["UNKNOWN"].play()

                # Music replay
                if event.type == pygame.USEREVENT:
                    self.song_name, self.song_path = choice(menu_themes)
                    load_music(self.song_path)
                    pygame.mixer.music.play()
                    
            mouse_sound_timer -= 4 * self.dt