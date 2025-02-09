import pygame
import sys
from functions.game_files_loader import *
from functions.game_funcs import rand_num, rot_center
from classes.CircleNom import CircleNom

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
menu_items = ["Start", "Options", "Quit"]
options_items = ["Difficulty", "Screen Mode", "Back"]

# Difficulty levels
difficulties = ["Easy", "Medium", "Hard"]
current_difficulty = 0

# Current selected item for the main menu
selected_item = 0

# Current selected item for the options menu
selected_option = 0

# Angle for rotation
angle = 0

# Select random background
background_image = background_images[rand_num(len(background_images))]

# Select random player image index
player_image_index = rand_num(len(player_images))

# Set end event for autoplaying
pygame.mixer.music.set_endevent(pygame.USEREVENT)

# Start game function
def start_game():
    global player_image_index
    game = CircleNom(
        screen=screen,
        difficulty=current_difficulty,
        eat_sounds=eat_sounds,
        theme_songs=theme_songs,
        player_image_index=player_image_index,
        player_images=player_images,
        player_images_dead=player_images_dead,
        prey_aura=prey_aura,
        prey_images=prey_images,
        background_image=background_image,
        hunger_bar=hunger_bar,
        dagger_images=dagger_images,
        dagger_sounds=dagger_sounds,
        hit_sounds=hit_sounds
    )
    # Start Circle Nom
    game.start()
    # Select different random player image index
    player_image_index = rand_num(len(player_images))


# Draw the options menu
def draw_options():

    # global angle for rotating aura
    global angle

    # Draw background
    screen.blit(background_image, (0, 0))

    # Draw player and aura
    draw_aura()

    # Update options display
    options_items[0] = f"Difficulty: {difficulties[current_difficulty]}"
    options_items[1] = f"Display mode: {screen_modes[current_screen_mode]}"

    # Draw options title
    title = font_big.render("Options", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - title.get_height() // 2 - 76))

    # Draw options items
    for index, item in enumerate(options_items):
        # Set the base color for the item
        base_color = WHITE if index != selected_option else LIGHT_BLUE
        text = font.render(item, True, base_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + index * 40))

        # Draw the difficulty part in its color
        if index == 0:  # Difficulty item
            difficulty_color = [GREEN, YELLOW, RED][current_difficulty]
            difficulty_text = font.render(difficulties[current_difficulty], True, difficulty_color)
            # Calculate the position for the difficulty text
            difficulty_x = WIDTH // 2 - text.get_width() // 2 + font.size("Difficulty: ")[0]
            screen.blit(difficulty_text, (difficulty_x, HEIGHT // 2 - text.get_height() // 2 + index * 40))

        # Draw the screen mode part in its color
        if index == 1:  # Screen Mode item
            screen_mode_color = LIGHT_BLUE if index == selected_option else WHITE
            screen_mode_text = font.render("Display mode: ", True, screen_mode_color)
            screen.blit(screen_mode_text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + index * 40))
            mode_text = font.render(screen_modes[current_screen_mode], True, WHITE)
            mode_x = WIDTH // 2 - text.get_width() // 2 + font.size("Display mode: ")[0]
            screen.blit(mode_text, (mode_x, HEIGHT // 2 - text.get_height() // 2 + index * 40))

    # Update the display
    pygame.display.flip()

# Toggle screen mode function
def toggle_screen_mode():
    main_menu_clicks[1].play()
    global current_screen_mode, screen
    current_screen_mode = (current_screen_mode + 1) % len(screen_modes)
    if current_screen_mode == 1:  # Fullscreen
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:  # Windowed
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_aura():
    
    # Global angle for continuous rotation
    global angle

    player_position = pygame.Vector2(640, 140)
    player_scale = [180, 180]

    # Rotate and draw player aura
    rotated_aura = rot_center(player_aura, angle, player_position)
    screen.blit(rotated_aura[0], rotated_aura[1])

    # Draw player
    player_image = pygame.transform.smoothscale(player_images[player_image_index], player_scale)
    screen.blit(player_image, player_position - pygame.Vector2(player_image.get_width() / 2, player_image.get_height() / 2))

    # Increment the angle for continuous rotation
    angle = (angle % 360) - 0.1

def draw_menu():

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
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + index * 40))
    
    # Update the display
    pygame.display.flip()

# Main menu functions
def show_options():
    global selected_option
    global current_difficulty
    global current_screen_mode

    # Main loop for options menu
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    main_menu_clicks[0].play()
                    selected_option = (selected_option + 1) % len(options_items)

                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    main_menu_clicks[0].play()
                    selected_option = (selected_option - 1) % len(options_items)

                elif event.key == pygame.K_RETURN:
                    if options_items[selected_option] == "Back":
                        main_menu_clicks[0].play()
                        return  # Exit options menu
                    
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:

                    if selected_option == 0:
                        main_menu_clicks[1].play()
                        current_difficulty = (current_difficulty + 1) % len(difficulties)
                        
                    elif selected_option == 1:
                        main_menu_clicks[1].play()
                        toggle_screen_mode()
                    
                    elif selected_option == 2:
                        main_menu_clicks[2].play()

                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:

                    if selected_option == 0:
                        main_menu_clicks[1].play()
                        current_difficulty = (current_difficulty - 1) % len(difficulties)

                    elif selected_option == 1:
                        main_menu_clicks[1].play()
                        toggle_screen_mode()

                    elif selected_option == 2:
                        main_menu_clicks[2].play()

                else:
                    main_menu_clicks[2].play()

            # Music replay
            if event.type == pygame.USEREVENT:
                pygame.mixer.music.load(main_menu_themes[rand_num(len(main_menu_themes))])
                pygame.mixer.music.play()

        # Draw the options menu
        draw_options()

menu_functions = [start_game, show_options, sys.exit]

def main():
    global selected_item
    global score

    # Play menu theme
    pygame.mixer.music.load(main_menu_themes[rand_num(len(main_menu_themes))])
    pygame.mixer.music.play()
    
    # Main loop for main menu
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    main_menu_clicks[0].play()
                    selected_item = (selected_item + 1) % len(menu_items)

                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    main_menu_clicks[0].play()
                    selected_item = (selected_item - 1) % len(menu_items)
                    
                elif event.key == pygame.K_RETURN:
                    main_menu_clicks[0].play()
                    score = menu_functions[selected_item]()

                else:
                    main_menu_clicks[2].play()

             # Music replay
            if event.type == pygame.USEREVENT:
                pygame.mixer.music.load(main_menu_themes[rand_num(len(main_menu_themes))])
                pygame.mixer.music.play()

        # Draw the main menu
        draw_menu()

# Call function main()
if __name__ == "__main__":
    main()
