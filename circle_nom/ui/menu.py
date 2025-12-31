# Importing modules

# Circle Nom Engine (the core game)
from circle_nom.core.engine import CircleNom

# Game Systems & Helpers
from circle_nom.systems.asset_loader import AssetLoader 
from circle_nom.systems.oscillator import Oscillator
import circle_nom.helpers.other_utils as other_utils
from circle_nom.helpers.asset_bank import AssetBank
from circle_nom.systems.logging import get_logger
from circle_nom.systems.timer import Timer

# Builtins & Third-party
from random import choice, randint
from typing import Union
import webbrowser
import pygame
import sys

class Menu:
    
    # Get Pygame window size
    WIDTH, HEIGHT = pygame.display.get_window_size()
    
    # Logger reference
    _LOGGER = get_logger(name=__name__)
    
    # Game asset bank
    _AB = AssetBank()
    
    # Game asset loader
    _AL = AssetLoader()
    
    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    LIME = (50, 205, 50)
    YELLOW = (255, 255, 0)
    GOLD = (255, 169, 0)
    LIGHT_PURPLE = (118, 127, 248)
    PURPLE = (224, 64, 251)
    ELECTRIC_PINK = (255, 54, 166)
    LIGHT_BLUE = (0, 125, 255)
    
    # Fonts
    FONT_SMALL = pygame.Font(_AB.comic_sans_ms, 15)
    FONT = pygame.Font(_AB.comic_sans_ms, 40)
    FONT_BIG = pygame.Font(_AB.comic_sans_ms, 65)
    
    # Main Menu items - Item and RGB Values
    MAIN_MENU_ITEMS = (
        ("Play", GREEN), 
        ("Options", LIGHT_BLUE),
        ("Quit", RED))
    
    # Credits items - Item and RGB Values
    CREDITS_ITEMS = (
        ("Made by Emanuil Hadzhivasilev", GOLD),
        ("Circle Nom's GitHub Page", PURPLE),
        ("Back", LIGHT_BLUE)
    )
    
    # Option items - Item and RGB/HEX Values
    VOL_LEVELS = (
        ("0", "#0075ff"), ("10", "#03cffe"), ("20", "#06fcd3"), ("30", "#08fb7c"), 
        ("40", "#0bfa29"), ("50", "#44f80e"), ("60", "#97f710"), ("70", "#e8f613"), 
        ("80", "#f4b316"), ("90", "#f36618"), ("100", "#f21b1b")
    )
    
    DIFF_MODES = (("Easy", "#00ff00"), ("Medium", "#ffff00"), ("Hard", "#ff9500"), ("Impossible", "#ff0000"))
    FPS_CAPS = (
        ("30", "#ff0000"), ("60", "#ff0039"), ("75", "#ff075f"), ("120", "#ff207d"), 
        ("144", "#ff2a9a"), ("240", "#ff2db8"), ("360", "#ff22dd"), ("Unlimited", "#f942ff")
    )
    PLAY_MODES = (("Singleplayer", "#94f21c"), ("Multiplayer", "#0acffa"))
    SCREEN_MODES = (("Windowed", "#fa0a35"), ("Fullscreen", "#adff00"))
    VSYNC_MODES = (("Off", "#ff0000"), ("On", "#00ff00"))
    
    # Aura and Player in Menu consts
    AURA_MENU_POS = pygame.Vector2(WIDTH / 2, HEIGHT / 5)
    PLAYER_MENU_SCALE = (180, 180)
    
    # Menus clicks sound cooldown const (85 ms)
    CLICK_TIMER_CD = 0.085
    
    # Project's GitHub page link, used in Credits
    CIRCLE_NOM_GITHUB_PAGE = "https://github.com/ExtremerBG/Circle-Nom"
    
    # Thank you note, used in Credits
    THANK_YOU = FONT_SMALL.render(text="Thank you for playing Circle Nom!", antialias=True, color=WHITE)
    
    # Game version number, used in Main
    GAME_VER = FONT_SMALL.render(text="v.4.1.0", antialias=True, color=WHITE)
    
    def __init__(self, screen: pygame.Surface) -> None:
        
        """
        Initializes the Menus for the Circle Nom game. This should be your way to normally launch the core game, \n
        which is located in the engine.py file. These Menus support a variety of options to fine tune your experience.
        
        Args:
            screen (pygame.Surface): The Pygame screen object, declared in main.
        """
        
        # Create a new Timer and start it
        self.menu_timer = Timer(name="MenuTimerThread")
        self.menu_timer.start()
        
        # Pygame clock for framerate
        self.clock = pygame.time.Clock()
            
        # Delta time
        self.dt = 0.00
        
        # Setup pygame screen
        self.screen = screen
        self._setup_screen()
        self._get_new_rand_images()
        
        # Inititial setting values
        self.current_volume = 5
        self.current_fps_cap = 3
        self.current_difficulty = 0
        self.current_play_mode = 0
        self.current_screen_mode = 0
        self.current_vsync_mode = 0
        
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
                "VSync": self.VSYNC_MODES[self.current_vsync_mode],
                "Back": None
            }
        
        # Inititial selected item for menus
        self.selected_menu_item = 0
        self.selected_options_item = 0
        self.selected_credits_item = 0
        self.is_title_selected = False
        
        # Aura rotation angle
        self.player_aura_angle = 0

        # Load random menu theme song
        self.song_name, self.song_path = choice(self._AB.menu_themes)
        self._AL.load_music(self.song_path)
        
        # End event for music autoplay
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        
        # Menu last click timestamp - used for setting a cooldown on menu clicks
        self.last_click_timestamp = 0
        
        # Oscillating values, used for colour shifting and selected item movement
        self.sine_colours_shift = Oscillator(a_min=0, a_max=1, period=1.8, pattern="sine")
        self.sine_movement_offset = Oscillator(a_min=-3, a_max=3, period=1.2, pattern="triangle")
        
        # Log the Menu init
        self._LOGGER.info("Circle Nom Menus initialized successfully.")
        
    @property
    def fps_cap(self) -> int:
        """Get the fps cap value."""
        return self._fps_cap
    
    @fps_cap.setter
    def fps_cap(self, value) -> None:
        """
        Cap pygame's FPS with the given value.
        
        Args:
            value (str): The fps value. Tries to convert to int. If it fails, value = 0 (no limit).
        """
        try:
            self._fps_cap = int(value)
        except ValueError:
            self._fps_cap = 0
            
    def _get_new_rand_images(self) -> None:
        """Select a random background image, player image index and refresh associated vars."""
        self.background_image = choice(self._AB.background_images)
        if randint(0, 5) == 0: # 20% chance to choose random accessory
            self.player_accessory = choice(self._AB.player_accessories)
        else:
            self.player_accessory = None
        self.player_menu_image = pygame.transform.smoothscale(self._AB.player_image, self.PLAYER_MENU_SCALE)
        self.player_blit_pos = self.AURA_MENU_POS - pygame.Vector2(self.player_menu_image.width / 2, self.player_menu_image.height / 2)
        self._normalize_background_image()
        
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
        for sound in self._AB.menu_click_sounds.values(): sound.set_volume(volume)
        for sound in self._AB.player_eat_sounds: sound.set_volume(volume)
        for sound in self._AB.dagger_sounds: sound.set_volume(volume)
        for sound in self._AB.player_hit_sounds: sound.set_volume(volume)
        for sound in self._AB.dash_sounds: sound.set_volume(volume)
        
    def _play_menu_click(self, type: str) -> None:
        """
        Play a Menu click sound with a given type.
        
        Args:
            type (str): The given click type. Can be either LEFTRIGHT, UPDOWN or UNKNOWN.
        """
        if type not in self._AB.menu_click_sounds.keys(): 
            self._LOGGER.warning(f"Invalid Menus click type. Can be one of {self._AB.menu_click_sounds.keys()}.")
            return
        
        # Play sound only if cooldown is passed
        if self.menu_timer.get_time() - self.last_click_timestamp > self.CLICK_TIMER_CD:
            self.last_click_timestamp = self.menu_timer.get_time()
            self._AB.menu_click_sounds[type].play()
            
    def _normalize_background_image(self) -> None:
        """Normalize the background image to match the current screen resolution."""
        size_factor = ((self.screen.width / self.background_image.width), 
                       (self.screen.height /self.background_image.height))
        self.background_image = pygame.transform.smoothscale_by(self.background_image, size_factor)
        
    def _setup_screen(self) -> None:
        """Setup the pygame screen and background image with its size, icon, captions and others."""
        pygame.display.set_icon(self._AB.icon)
        pygame.display.set_caption("Circle Nom")
        pg_cursor = pygame.cursors.Cursor((8, 8), self._AB.cursor)
        pygame.mouse.set_cursor(pg_cursor)
        
    def _toggle_screen_modes(self) -> None:
        """Toggle between the different screen modes - Windowed/Fullscreen and VSync Off/On."""
        # Quits and re-inits display to avoid weird bug where VSync toggles freeze the screen
        pygame.display.quit()
        pygame.display.init()
        # Set display modes based on what screen mode is selected
        if self.current_screen_mode == 1: # Fullscreen
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN, vsync=self.current_vsync_mode)
        else:                             # Windowed
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), vsync=self.current_vsync_mode)
        # Call setup screen again since the custom icon and stuff was reset
        self._setup_screen()
            
    def _draw_menu_player(self) -> None:
        """Draw the player, aura and the optional accessory on the screen."""
        
        # Rotate and draw aura
        aura = other_utils.rot_center(self._AB.player_aura, self.player_aura_angle, self.AURA_MENU_POS)
        self.screen.blit(aura[0], aura[1])
        
        # Increment aura for rotation
        self.player_aura_angle = (self.player_aura_angle % 360) - 24 * self.dt
        
        # Draw player on top of aura
        self.screen.blit(self.player_menu_image, self.player_blit_pos)
        
        # Draw accessory on top of player if exist
        if self.player_accessory:
            self.screen.blit(
                self.player_accessory[1], 
                self.player_blit_pos + self.player_accessory[0] - pygame.Vector2(
                    self.player_accessory[1].width / 2, self.player_accessory[1].height / 2
                )
            )
        
    def _options_movement_horizontal(self, move_step: int) -> None:
        """
        Handle moving horizontally in the options menu.
        
        Args:
            move_step (int): The step to move with. Typically either -1 or 1.
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
            self._toggle_screen_modes()
            
        # VSync mode
        elif self.selected_options_item == 5:
            self.current_vsync_mode = (self.current_vsync_mode + move_step) % len(self.VSYNC_MODES)
            self._toggle_screen_modes()
            
        self._play_menu_click("LEFTRIGHT")
            
    def _calc_menu_item_pos(self, text_width: Union[int, float], text_height: Union[int, float], 
                            index: int) -> tuple[Union[int, float], Union[int, float]]:
        """
        Calculate centered X, Y coordinates with its index for Y offset. Used for menu ITEMS only.
        
        Args:
            text_width (int | float): The text width, usually calculated with text.width.
            text_height (int | float): The text height, usually calculated with text.height.
            index (int): The text index in the menu items list. Used to calculate the Y offset.
            
        Returns:
            tuple(int, int): A tuple containing the calculated X and Y coordinates.
        """
        return self.WIDTH // 2 - text_width // 2, self.HEIGHT // 1.9 - text_height // 2 + index * 45
    
    def _calc_menu_title_pos(self, title: pygame.Surface) -> tuple[int, int]:
        """
        Calculate centered X, Y coordinates of the given text Surface. Used for menu TITLES ONLY.
        
        Args:
            title (pygame.Surface): The given rendered title surface.
            
        Returns:
            tuple(int, int): A tuple containing the calculated X and Y coordinates.
        """
        return self.WIDTH // 2 - title.width // 2, self.HEIGHT // 2 - title.height // 2 - 60
    
    def _render_gradient_title(self, title: str, colour1: tuple[int, int, int], 
                             colour2: tuple[int, int, int]) -> pygame.Surface:
        """
        Render a title that changes colours from colour1 to colour2 smoothly.
        
        Args:
            title (str): The title string to render.
            colour1 tuple: Tuple containing RGB values for colour 1.
            colour2 tuple: Tuple containing RGB values for colour 2.
            step (int): The step speed between colours. Higher is faster and vice-versa.
            
        Returns:
            pygame.Surface: The rendered title surface.
        """
        fade = self.sine_colours_shift.update(self.dt)
        r = int(colour1[0] * (1 - fade) + colour2[0] * fade)
        g = int(colour1[1] * (1 - fade) + colour2[1] * fade)
        b = int(colour1[2] * (1 - fade) + colour2[2] * fade)
        
        # Render text with the generated colour
        return self.FONT_BIG.render(title, True, (r, g, b))
        
    def _draw_credits(self) -> list[pygame.Rect]:
        """
        Display the credits menu on the screen.
        
        Returns:
            list(pygame.Rect): List of pygame Rects representing the credits items.
        """
        self.screen.blit(self.background_image, (0, 0))
        self._draw_menu_player()
        
        # Draw credits items & add rects
        index = 0
        credits_rects = []
        for item in self.CREDITS_ITEMS:
            
            # Calculate offset if item is selected
            if index == self.selected_credits_item:
                x_offset = self.sine_movement_offset.update(self.dt)
                text = self.FONT.render(item[0], True, item[1])
            else:
                x_offset = 0
                text = self.FONT.render(item[0], True, self.WHITE)
            
            # Calculate text position, create Rect and display text
            x, y = self._calc_menu_item_pos(text.width, text.height, index)
            x += x_offset
            credits_rects.append(pygame.Rect(x, y, text.width, text.height))
            self.screen.blit(text, (x, y))
            index += 1
                
        # Draw song name
        other_utils.draw_music_name(self.screen, self.song_name, self.FONT_SMALL)
        
        # Draw thank you note
        self.screen.blit(self.THANK_YOU, ((self.screen.width - self.THANK_YOU.width - 10), self.screen.height - 25))
        
        # Draw gradient title
        title = self._render_gradient_title("Credits", self.GREEN, self.LIME)
        self.screen.blit(title, self._calc_menu_title_pos(title))
        
        # Update display
        pygame.display.flip()
        
        # Limit fps and get dt
        self.dt = self.clock.tick(self.fps_cap) / 1000
        
        # Return generated options items rects
        return credits_rects
        
    def _launch_credits(self) -> None:
        """Launch the Credits Menu."""
        self._LOGGER.info("Credits Menu launched.")
        
        # Credits loop
        while True:
            
            # Rects from draw credits menu - used with mousepos
            item_rects = self._draw_credits()
            mousepos = pygame.mouse.get_pos()
            
            # Pygame event checker
            for event in pygame.event.get():
                
                # Exit condition if user closes window
                if event.type == pygame.QUIT:
                    sys.exit() # force exit | pygame.quit() throws errors
                    
                # Mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    
                    # Highlight item under mouse
                    for idx, rect in enumerate(item_rects):
                        
                        # Check if mousepos collides with a different credits item
                        if rect.collidepoint(mousepos):
                            if self.selected_credits_item != idx:
                                self.selected_credits_item = idx
                                self._play_menu_click("UPDOWN")
                            
                            # Break for if the collided item is the same
                            else: break
                
                # Mouse key events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Left click
                    if event.button == 1:
                        
                        # Author item
                        if self.selected_credits_item == 0:
                            choice(self._AB.player_eat_sounds).play()
                        
                        # GitHub page item
                        elif self.selected_credits_item == 1:
                            webbrowser.open(self.CIRCLE_NOM_GITHUB_PAGE)
                        
                        # Back item
                        elif self.selected_credits_item == 2:
                            self._play_menu_click("UPDOWN")
                            return # Return to main menu
                        
                    # Right click
                    elif event.button == 3:
                        # Author item
                        if self.selected_credits_item == 0:
                            choice(self._AB.player_hit_sounds).play()
                    
                # Keyboard events
                elif event.type == pygame.KEYDOWN:
                    
                    # Enter
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        
                        # Author item
                        if self.selected_credits_item == 0:
                            choice(self._AB.player_eat_sounds).play()
                            
                        # GitHub page item
                        elif self.selected_credits_item == 1:
                            webbrowser.open(self.CIRCLE_NOM_GITHUB_PAGE)
                            
                        # Back item
                        elif self.selected_credits_item == 2:
                            self._play_menu_click("UPDOWN")
                            return # Return to main menu
                        
                    # Backspace or Escape
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                        self._play_menu_click("UPDOWN")
                        return # Exit credits menu
                        
                    # Movement up - W, ↑
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        self._play_menu_click("UPDOWN")
                        self.selected_credits_item = (self.selected_credits_item - 1) % len(self.CREDITS_ITEMS)
                        
                    # Movement down - S, ↓
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self._play_menu_click("UPDOWN")
                        self.selected_credits_item = (self.selected_credits_item + 1) % len(self.CREDITS_ITEMS)
                            
                # Music end event - Choose new one
                elif event.type == pygame.USEREVENT:
                    self.song_name, self.song_path = choice(self._AB.menu_themes)
                    self._AL.load_music(self.song_path)
                    pygame.mixer.music.play()
    
    def _draw_options(self) -> list[pygame.Rect]:
        """
        Display the options menu on the screen.
        
        Returns:
            list(pygame.Rect): List of pygame Rects representing the options items.
        """
        self.screen.blit(self.background_image, (0, 0))
        self._draw_menu_player()

        # Update options items
        self.options_items["Volume"] = self.VOL_LEVELS[self.current_volume]
        self.options_items["FPS Cap"] = self.FPS_CAPS[self.current_fps_cap]
        self.options_items["Difficulty"] = self.DIFF_MODES[self.current_difficulty]
        self.options_items["Mode"] = self.PLAY_MODES[self.current_play_mode]
        self.options_items["Display"] = self.SCREEN_MODES[self.current_screen_mode]
        self.options_items["VSync"] = self.VSYNC_MODES[self.current_vsync_mode]
        
        # Draw options items & add rects
        index = 0
        option_rects = []
        for key, value in self.options_items.items():
            
            # Key colours - LIGHT_BLUE/WHITE <=> selected/deselected
            # Calculate offset if key is the selected one
            if index == self.selected_options_item:
                x_offset = self.sine_movement_offset.update(self.dt)
                key_colour = self.LIGHT_BLUE
                
            else:
                x_offset = 0
                key_colour = self.WHITE
                
            # Case for all options with horizontal movement
            if value is not None:
                # Render texts and set colour for value
                key_text = self.FONT.render(f"{key}: ", True, key_colour)
                # value holds tuple("TEXT", (255, 255, 0)) - containing text and rgb value
                value_text = self.FONT.render(f"< {value[0]} >", True, value[1])
                
                # Calculate text position
                total_width = key_text.width + value_text.width
                total_height = max(key_text.height, value_text.height)
                x, y = self._calc_menu_item_pos(total_width, total_height, index)
                x += x_offset
                
                # Blit both texts & create rect
                self.screen.blit(key_text, (x, y))
                self.screen.blit(value_text, (x + key_text.width, y))
                
            # Case for Back option (no horizontal movement)
            else:
                # Render text & calculate position
                key_text = self.FONT.render(f"{key}", True, key_colour)
                total_width = key_text.width
                total_height = key_text.height
                x, y = self._calc_menu_item_pos(key_text.width, key_text.height, index)
                x += x_offset
                
                # Blit and create rect
                self.screen.blit(key_text, (x, y))
            
            # Append created rect from item for returning & increment index
            option_rects.append(pygame.Rect(x, y, total_width, total_height))
            index += 1
                
        # Draw song name
        other_utils.draw_music_name(self.screen, self.song_name, self.FONT_SMALL)
        
        # Draw FPS
        other_utils.draw_fps(self.screen, self.clock, self.FONT_SMALL)
        
        # Draw gradient title
        title = self._render_gradient_title("Options", self.LIGHT_BLUE, self.LIGHT_PURPLE)
        self.screen.blit(title, self._calc_menu_title_pos(title))
        
        # Update display
        pygame.display.flip()
        
        # Limit fps and get dt
        self.dt = self.clock.tick(self.fps_cap) / 1000
        
        # Return generated options items rects
        return option_rects
    
    def _launch_options(self) -> None:
        """Launch the Options Menu."""
        self._LOGGER.info("Options Menu launched.")
        
        # Options loop
        while True:
            
            # Rects from draw options menu - used with mousepos
            item_rects = self._draw_options()
            mousepos = pygame.mouse.get_pos()
            
            # Pygame event checker
            for event in pygame.event.get():
                
                # Exit condition if user closes window
                if event.type == pygame.QUIT:
                    sys.exit() # force exit | pygame.quit() throws errors
                    
                # Mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    
                    # Highlight item under mouse
                    for idx, rect in enumerate(item_rects):
                        
                        # Check if mousepos collides with a different options item
                        if rect.collidepoint(mousepos):
                            if self.selected_options_item != idx:
                                self.selected_options_item = idx
                                self._play_menu_click("UPDOWN")
                            
                            # Break for if the collided item is the same
                            else: break
                
                # Mouse key events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                        
                    # Left click on Back option
                    if event.button == 1 and self.selected_options_item == 6: # Back is located at index 6
                        self._play_menu_click("UPDOWN")
                        return # Return to main menu
                    
                    # Right click horizontal options - go right
                    elif event.button == 3 and self.selected_options_item in (0, 1, 2, 3, 4, 5):
                        self._options_movement_horizontal(move_step=1)
                        
                    # Left click on horizontal options - go left
                    elif event.button == 1 and self.selected_options_item in (0, 1, 2, 3, 4, 5):
                        self._options_movement_horizontal(move_step=-1)
                    
                # Keyboard events
                elif event.type == pygame.KEYDOWN:
                    
                    # Enter
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if self.selected_options_item == 6: # Back is located at index 6
                            self._play_menu_click("UPDOWN")
                            return # Return to main menu
                        
                    # Backspace or Escape
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                        self._play_menu_click("UPDOWN")
                        return # Return to main menu
                        
                    # Movement up - W, ↑
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        self._play_menu_click("UPDOWN")
                        self.selected_options_item = (self.selected_options_item - 1) % len(self.options_items)
                        
                    # Movement down - S, ↓
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self._play_menu_click("UPDOWN")
                        self.selected_options_item = (self.selected_options_item + 1) % len(self.options_items)
                        
                    # Movement right - D, →
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self._options_movement_horizontal(move_step=1)
                            
                    # Movement left - A, ←
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self._options_movement_horizontal(move_step=-1)
                            
                # Music end event - Choose new one
                elif event.type == pygame.USEREVENT:
                    self.song_name, self.song_path = choice(self._AB.menu_themes)
                    self._AL.load_music(self.song_path)
                    pygame.mixer.music.play()
    
    def _draw_main_menu(self) -> tuple[list[pygame.Rect], pygame.Rect]:
        """
        Display the main menu on the screen.
        
        Returns:
            tuple[list[pygame.Rect], pygame.Rect]: List of pygame Rects representing the menu items and the title rect.
        """
        self.screen.blit(self.background_image, (0, 0))
        self._draw_menu_player()
        
        # Set colours for menu items & last selected index for smooth transition
        main_menu_rects = []
        for index, item in enumerate(self.MAIN_MENU_ITEMS):
            
            # Draw menu item with its colour if its selected & calculate offset
            if self.selected_menu_item == index and not self.is_title_selected:
                x_offset = self.sine_movement_offset.update(self.dt)
                text = self.FONT.render(item[0], True, item[1])
                
            else:
                x_offset = 0
                text = self.FONT.render(item[0], True, self.WHITE)
            
            # Calculate text position, create Rect and display text
            x, y = self._calc_menu_item_pos(text.width, text.height, index)
            x += x_offset # add x_offset to x, can be ether -4 <-> 4 or 0
            main_menu_rects.append(pygame.Rect(x, y, text.width, text.height))
            self.screen.blit(text, (x, y))
        
        # Draw song name
        other_utils.draw_music_name(self.screen, self.song_name, self.FONT_SMALL)
        
        # Draw game version
        self.screen.blit(self.GAME_VER, ((self.screen.width - self.GAME_VER.width - 10), self.screen.height - 25))
        
        # Render gradient title
        title = self._render_gradient_title("Circle Nom", self.GOLD, self.YELLOW)
        title_pos = self._calc_menu_title_pos(title)
        title_rect = pygame.Rect(title_pos[0], title_pos[1], title.width, title.height)
        
        # Check if title is selected
        if self.is_title_selected:
            x_offset = self.sine_movement_offset.update(self.dt)
            title_pos = (title_pos[0] + x_offset, title_pos[1])
            
        # Draw title
        self.screen.blit(title, title_pos)
        
        # Update display
        pygame.display.flip()
        
        # Limit fps and get dt
        self.dt = self.clock.tick(self.fps_cap) / 1000
        
        # Return generated menu items rects
        return main_menu_rects, title_rect
    
    def launch_main_menu(self) -> None:
        """Launch the Main Menu."""
        self._LOGGER.info("Main Menu launched.")
        
        # Functions list for the main menu - None is a placeholder for return, since sys.exit breaks the profiler
        MAIN_MENU_FUNCTIONS = [self.start_game, self._launch_options, None]
        
        # Play menu theme
        pygame.mixer.music.play()
        
        # Main menu loop
        while True:
            
            # Rects from draw options menu - used with mousepos
            item_rects, title_rect = self._draw_main_menu()
            mousepos = pygame.mouse.get_pos()
            
            # Pygame event checker
            for event in pygame.event.get():
                
                # Exit condition if user closes window
                if event.type == pygame.QUIT:
                    sys.exit() # force exit | pygame.quit() throws errors
                    
                # Mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    
                    # Check if mouse is over title
                    if title_rect.collidepoint(mousepos):
                        if not self.is_title_selected:
                            self.is_title_selected = True
                            self._play_menu_click("UPDOWN")
                    else:
                        if self.is_title_selected:
                            self.is_title_selected = False
                            self._play_menu_click("UPDOWN")
                    
                    # Highlight item under mouse
                    for idx, rect in enumerate(item_rects):
                        
                        # Check if mousepos collides with a different menu item
                        if rect.collidepoint(mousepos):
                            if self.selected_menu_item != idx:
                                self.selected_menu_item = idx
                                if self.is_title_selected:
                                    self.is_title_selected = False
                                    self._play_menu_click("UPDOWN")
                                self._play_menu_click("UPDOWN")
                            
                            # Break for if the collided item is the same
                            else: break
                
                # Mouse key events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Left click
                    if event.button == 1:
                        # Check if title was clicked
                        if title_rect.collidepoint(mousepos):
                            self._play_menu_click("UPDOWN")
                            self._launch_credits()
                        else:
                            self._play_menu_click("UPDOWN")
                            action = MAIN_MENU_FUNCTIONS[self.selected_menu_item]
                            if not action: return # None is the return placeholder in ref list
                            action()
                    
                # Key events
                if event.type == pygame.KEYDOWN:
                    
                    # Enter
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        self._play_menu_click("UPDOWN")
                        if self.is_title_selected:
                            self._launch_credits()
                        else:
                            action = MAIN_MENU_FUNCTIONS[self.selected_menu_item]
                            if not action: return # None is the return placeholder in ref list
                            action()
                    
                    # Backspace
                    elif event.key == pygame.K_BACKSPACE:
                        self._play_menu_click("UPDOWN")
                        return # Exit main menu & program
                    
                    # Escape
                    elif event.key == pygame.K_ESCAPE:
                        self._play_menu_click("UPDOWN")
                        return # Exit main menu & program
                    
                    # Movement up - W, ↑ 
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        if not self.is_title_selected:
                            self._play_menu_click("UPDOWN")
                            self.selected_menu_item = (self.selected_menu_item - 1) % len(self.MAIN_MENU_ITEMS)
                        
                    # Movement down - S, ↓ 
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if not self.is_title_selected:
                            self._play_menu_click("UPDOWN")
                            self.selected_menu_item = (self.selected_menu_item + 1) % len(self.MAIN_MENU_ITEMS)

                # Music end event - Choose new one
                elif event.type == pygame.USEREVENT:
                    self.song_name, self.song_path = choice(self._AB.menu_themes)
                    self._AL.load_music(self.song_path)
                    pygame.mixer.music.play()
                    
    def start_game(self) -> None:
        """Start the Circle Nom game."""
        
        # Stop the Menu timer before entering the game
        self.menu_timer.stop()
        
        # Declare a new Circle Nom game object
        game = CircleNom(
            screen=self.screen,
            fps_cap=self.fps_cap, difficulty=self.current_difficulty,play_mode=self.current_play_mode, 
            player_accessory=self.player_accessory, background_image=self.background_image
        )
        
        # Start the Circle Nom game
        game.start()
        
        # Delete the old Circle Nom instance
        del game
        
        # After game finishes, get new random images
        self._get_new_rand_images()
        
        # Start the Menu timer again after finishing the Game
        self.menu_timer.start()