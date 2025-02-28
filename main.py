import pygame
import sys
from random import choice, randint
from functions.game_files_loader import *
from functions.game_funcs import rot_center
from classes.circle_nom import CircleNom

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle Nom")
pygame.display.set_icon(pygame.image.load(resource_path('image/others/icon.ico')))

# Screen modes
screen_modes = ["Windowed", "Fullscreen"]
current_screen_mode = 0

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (0, 125, 255)

# Fonts
font = pygame.font.SysFont('Comic Sans MS', 36)
font_big = pygame.font.SysFont('Comic Sans MS', 60)

# Menu options
menu_items = ["Play", "Options", "Quit"]
options_items = ["Volume", "Difficulty", "Play Mode", "Display Mode", "Back"]

# Difficulty levels
difficulties = ["Easy", "Medium", "Hard"]
current_difficulty = 0

# Play mode options
play_modes = ["Singleplayer", "Multiplayer"]
current_play_mode = 0

# Set volume for all sounds
def set_sound_volume(volume):
    """
    Set the volume for all game sounds.

    Args:
        volume (float): The volume level to set (0.0 to 1.0).
    """
    pygame.mixer.music.set_volume(volume)
    for sound in main_menu_clicks:
        sound.set_volume(volume)
    for sound in eat_sounds:
        sound.set_volume(volume)
    for sound in dagger_sounds:
        sound.set_volume(volume)
    for sound in hit_sounds:
        sound.set_volume(volume)

# Volume options
volume_levels = ["0", "10", "20", "30", "40", "50",
                    "60", "70", "80", "90", "100"]
current_volume = 5
set_sound_volume(current_volume / 10)

# Current selected item for the main menu
selected_item = 0

# Current selected item for the options menu
selected_option = 0

# Angle for rotation
angle = 0

# Select random background index
background_image = choice(background_images)

# Select random player images index
player_images_index = randint(0, len(player_images)-1)

# Set end event for autoplaying
pygame.mixer.music.set_endevent(pygame.USEREVENT)

# Start game function
def start_game():
    """
    Start the Circle Nom game.
    """
    global player_images_index
    global background_image
    
    # Select player image from lists
    player_image = player_images[player_images_index]
    player_image_dead = player_images_dead[player_images_index]
    
    game = CircleNom(screen, current_difficulty, current_play_mode,
                     eat_sounds, theme_songs, player_image, player_image_dead,
                     prey_images, prey_aura, background_image, health_bar,
                     dagger_images, dagger_sounds, hit_sounds)
    
    # Start Circle Nom
    game.start()
    
    # New random player images index and background image
    player_images_index = randint(0, len(player_images)-1)
    background_image = choice(background_images)

# Toggle screen mode function
def toggle_screen_mode():
    """
    Toggle between windowed and fullscreen modes.
    """
    main_menu_clicks[1].play()
    global current_screen_mode, screen
    current_screen_mode = (current_screen_mode + 1) % len(screen_modes)
    if current_screen_mode == 1:  # Fullscreen
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:  # Windowed
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Draw player and aura
def draw_aura():
    """
    Draw the player and its aura on the screen.
    """
    global player_images_index
    global angle # Global angle for continuous rotation
    
    player_position = pygame.Vector2(640, 140)
    player_scale = [180, 180]

    # Rotate and draw player aura
    rotated_aura = rot_center(player_aura, angle, player_position)
    screen.blit(rotated_aura[0], rotated_aura[1])

    # Draw player
    player_image = pygame.transform.smoothscale(player_images[player_images_index], player_scale)
    screen.blit(player_image, player_position - pygame.Vector2(player_image.get_width() / 2, player_image.get_height() / 2))

    # Increment the angle for continuous rotation
    angle = (angle % 360) - 0.1

# Select and update options menu
def show_options():
    """
    Display and handle the options menu.
    """
    global selected_option
    global current_volume
    global current_difficulty
    global current_play_mode
    global current_screen_mode

    # Main loop for options menu
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                # Enter key
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if options_items[selected_option] == "Back":
                        main_menu_clicks[0].play()
                        return  # Exit options menu
                
                # Backspace key
                elif event.key == pygame.K_BACKSPACE:
                    main_menu_clicks[0].play()
                    return # Exit options menu
                
                # Escape key
                elif event.key == pygame.K_ESCAPE:
                    main_menu_clicks[0].play()
                    return # Exit options menu
                
                # Movement down
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    main_menu_clicks[0].play()
                    selected_option = (selected_option + 1) % len(options_items)

                # Movement up
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    main_menu_clicks[0].play()
                    selected_option = (selected_option - 1) % len(options_items)

                # Movement right 
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:

                    # Volume
                    if selected_option == 0:
                        main_menu_clicks[1].play()
                        current_volume = (current_volume + 1) % len(volume_levels)
                        set_sound_volume(current_volume / 10)
                    # Difficulty
                    elif selected_option == 1:
                        main_menu_clicks[1].play()
                        current_difficulty = (current_difficulty + 1) % len(difficulties)
                    # Play mode
                    elif selected_option == 2:
                        main_menu_clicks[1].play()
                        current_play_mode = (current_play_mode + 1) % len(play_modes)
                    # Screen mode
                    elif selected_option == 3:
                        main_menu_clicks[1].play()
                        toggle_screen_mode()

                # Movement left
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:

                    # Volume
                    if selected_option == 0:
                        main_menu_clicks[1].play()
                        current_volume = (current_volume - 1) % len(volume_levels)
                        set_sound_volume(current_volume / 10)
                    # Difficulty
                    elif selected_option == 1:
                        main_menu_clicks[1].play()
                        current_difficulty = (current_difficulty - 1) % len(difficulties)
                    # Play mode
                    elif selected_option == 2:
                        main_menu_clicks[1].play()
                        current_play_mode = (current_play_mode - 1) % len(play_modes)
                    # Screen mode
                    elif selected_option == 3:
                        main_menu_clicks[1].play()
                        toggle_screen_mode()


                # Invalid key presses
                # Special case if selected option is 1, 2 or 3 - play invalid key press sounds for all keys except W, S, A, D, ↑, ↓, ←, →
                if selected_option in [1, 2, 3] and event.key not in [pygame.K_w, pygame.K_UP, pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT, pygame.K_s, pygame.K_DOWN]:
                    main_menu_clicks[2].play()
                
                # Special case if selected option is 4 - play invalid key press sound for all keys except Enter, Backspace and Escape
                elif selected_option == 4 and event.key not in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_BACKSPACE, pygame.K_ESCAPE, pygame.K_DOWN, pygame.K_UP, pygame.K_w, pygame.K_s]:
                    main_menu_clicks[2].play()

            # Music replay
            if event.type == pygame.USEREVENT:
                pygame.mixer.music.load(choice(main_menu_themes))
                pygame.mixer.music.play()

        # Draw the options menu
        draw_options()

# Draw the options menu
def draw_options():
    """
    Draw the options menu on the screen.
    """
    # global angle for rotating aura
    global angle

    # Draw background
    screen.blit(background_image, (0, 0))

    # Draw player and aura
    draw_aura()

    # Update options display
    options_items[0] = f"Volume: {volume_levels[current_volume]}"
    options_items[1] = f"Difficulty: {difficulties[current_difficulty]}"
    options_items[2] = f"Play mode: {play_modes[current_play_mode]}"
    options_items[3] = f"Display mode: {screen_modes[current_screen_mode]}"

    # Draw options title
    title = font_big.render("Options", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - title.get_height() // 2 - 76))

    # Draw options items
    for index, item in enumerate(options_items):
        # Set the base color for the item
        base_color = WHITE if index != selected_option else LIGHT_BLUE
        text = font.render(item, True, base_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + index * 42))

        if index == 0: # Volume item
            volume_color = LIGHT_BLUE if index == selected_option else WHITE
            volume_text = font.render("Volume: ", True, volume_color)
            screen.blit(volume_text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + index * 42))
            volume_level_text = font.render(volume_levels[current_volume], True, WHITE)
            volume_x = WIDTH // 2 - text.get_width() // 2 + font.size("Volume: ")[0]
            screen.blit(volume_level_text, (volume_x, HEIGHT // 2 - text.get_height() // 2 + index * 42))

        # Draw the difficulty part in its color
        if index == 1:  # Difficulty item
            difficulty_color = [GREEN, YELLOW, RED][current_difficulty]
            difficulty_text = font.render(difficulties[current_difficulty], True, difficulty_color)
            # Calculate the position for the difficulty text
            difficulty_x = WIDTH // 2 - text.get_width() // 2 + font.size("Difficulty: ")[0]
            screen.blit(difficulty_text, (difficulty_x, HEIGHT // 2 - text.get_height() // 2 + index * 42))

            # Draw the play mode part in its color
        if index == 2:  # Play Mode item
            play_mode_color = LIGHT_BLUE if index == selected_option else WHITE
            play_mode_text = font.render("Play mode: ", True, play_mode_color)
            screen.blit(play_mode_text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + index * 42))
            mode_text = font.render(play_modes[current_play_mode], True, WHITE)
            mode_x = WIDTH // 2 - text.get_width() // 2 + font.size("Play mode: ")[0]
            screen.blit(mode_text, (mode_x, HEIGHT // 2 - text.get_height() // 2 + index * 42))

        # Draw the screen mode part in its color
        if index == 3:  # Screen Mode item
            screen_mode_color = LIGHT_BLUE if index == selected_option else WHITE
            screen_mode_text = font.render("Display mode: ", True, screen_mode_color)
            screen.blit(screen_mode_text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + index * 42))
            mode_text = font.render(screen_modes[current_screen_mode], True, WHITE)
            mode_x = WIDTH // 2 - text.get_width() // 2 + font.size("Display mode: ")[0]
            screen.blit(mode_text, (mode_x, HEIGHT // 2 - text.get_height() // 2 + index * 42))


    # Update the display
    pygame.display.flip()

# Draw the main menu
def draw_menu():
    """
    Draw the main menu on the screen.
    """
    # Draw background
    screen.blit(background_image, (0, 0))

    # Draw player and aura
    draw_aura()

    # Draw menu items
    for index, item in enumerate(menu_items):
        # Color change
        if index == selected_item == 0:
            color = GREEN
        elif index == selected_item == 1:
            color = LIGHT_BLUE
        elif index == selected_item == 2:
            color = RED
        else:
            color = WHITE

        # Draw title
        title = font_big.render("Circle Nom", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - title.get_height() // 2 - 76))

        # Draw items
        text = font.render(item, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + index * 42))
    
    # Update the display
    pygame.display.flip()

menu_functions = [start_game, show_options, sys.exit]

def main():
    """
    Main function to run the game.
    """
    global selected_item
    global score

    # Play menu theme
    pygame.mixer.music.load(choice(main_menu_themes))
    pygame.mixer.music.play()
    
    # Main loop for main menu
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                # Enter key
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    main_menu_clicks[0].play()
                    score = menu_functions[selected_item]()
                
                # Backspace key
                elif event.key == pygame.K_BACKSPACE:
                    main_menu_clicks[0].play()
                    return # Exit options menu
                
                # Escape key
                elif event.key == pygame.K_ESCAPE:
                    main_menu_clicks[0].play()
                    return # Exit options menu
                
                # Movement down
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    main_menu_clicks[0].play()
                    selected_item = (selected_item + 1) % len(menu_items)

                # Movement up
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    main_menu_clicks[0].play()
                    selected_item = (selected_item - 1) % len(menu_items)
                
                # Play sound for invalid key press
                else:
                    main_menu_clicks[2].play()

             # Music replay
            if event.type == pygame.USEREVENT:
                pygame.mixer.music.load(choice(main_menu_themes))
                pygame.mixer.music.play()

        # Draw the main menu
        draw_menu()

# Call function main()
if __name__ == "__main__":
    main()
