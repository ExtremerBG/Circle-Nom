from circle_nom.systems.asset_loader import *

################################################################################

# PYGAME WINDOW ICON
icon = load_image('assets/images/icon/icon.ico')

################################################################################

# EAT SOUNDS
eat_sounds = load_sounds(traverse_folder('assets/sounds/effects/player/eat/'), 6)

################################################################################

# GAME THEME SONGS
game_themes = load_playlist(traverse_folder('assets/sounds/themes/in_game/'), 16)

################################################################################

# PLAYER IMAGES
player_image = load_image('assets/images/player/alive/player_alive_image.png')
player_image_dead = load_image('assets/images/player/dead/player_dead_image.png')

player_eat_sequence = load_images(traverse_folder('assets/images/player/eat_sequence/'), 6)
player_accessories = (
    # const XY offset from player topleft, pygame image pairs
    (pygame.Vector2(x=0, y=0), load_image('assets/images/player/accessories/none.png')),
    (pygame.Vector2(x=90, y=70), load_image('assets/images/player/accessories/glasses.png')),
    (pygame.Vector2(x=90, y=3), load_image('assets/images/player/accessories/fedora.png')),
    (pygame.Vector2(x=90, y=-8), load_image('assets/images/player/accessories/propeller_hat.png')),
    (pygame.Vector2(x=90, y=70), load_image('assets/images/player/accessories/3d_glasses.png')),
)

################################################################################

# PREY IMAGES
prey_images = load_images(traverse_folder('assets/images/prey/alive/'), 11)

################################################################################

# PREY AURA
prey_aura = load_image('assets/images/prey/aura/prey_aura_image.png')

################################################################################

# BACKGROUNDS
background_images = load_images(traverse_folder('assets/images/backgrounds/'), 10)

################################################################################

# HUNGER BAR
health_bar = load_images(traverse_folder('assets/images/bar/'), 2)

################################################################################

# DAGGER                                            
dagger_images = load_images(traverse_folder('assets/images/dagger/'), 7)

################################################################################

# DAGGER FLY SOUNDS
dagger_sounds = load_sounds(traverse_folder('assets/sounds/effects/dagger/fly'), 5)

################################################################################

# PLAYER HIT SOUNDS
hit_sounds = load_sounds(traverse_folder('assets/sounds/effects/player/hit/'), 5)

################################################################################

# PLAYER AURA
player_aura = load_image('assets/images/player/aura/player_aura_image.png')

################################################################################

# MENU THEME SONGS
menu_themes = load_playlist(traverse_folder('assets/sounds/themes/menu/'), 2)

################################################################################

# MAIN MENU CLICKS
menu_clicks = {
    "UPDOWN": load_sound('assets/sounds/effects/menu/menu_click_up_down.mp3'),
    "LEFTRIGHT": load_sound('assets/sounds/effects/menu/menu_click_left_right.mp3'),
    "UNKNOWN": load_sound('assets/sounds/effects/menu/menu_click_unknown.mp3')
}

################################################################################

# DASH IMAGES
dash_images = {
    "AVAIL": load_image('assets/images/player/dash/dash_available_image.png'),
    "UNAVAIL": load_image('assets/images/player/dash/dash_unavailable_image.png')
}

################################################################################

# DASH SOUNDS
dash_sounds = load_sounds(traverse_folder('assets/sounds/effects/player/dash/'), 4)
    
################################################################################

# FLAME SEQUENCE
flame_sequence = load_images(traverse_folder('assets/images/flame_sequence'), 6)

################################################################################

# Cursor image
cursor_surface = load_image('assets/images/cursor/cursor_image.png')

################################################################################

# Comic Sans MS Font
comic_sans_ms = resource_path("assets/fonts/comic_sans_ms.ttf")

################################################################################