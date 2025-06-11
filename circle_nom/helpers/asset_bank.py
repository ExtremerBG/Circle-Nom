from circle_nom.systems.asset_loader import *

################################################################################

# PYGAME WINDOW ICON
ICON = load_image('assets/images/icon/icon.ico')

################################################################################

# PLAYER EAT SOUNDS
EAT_SOUNDS = load_sounds(traverse_folder('assets/sounds/effects/player/eat/'), 6)

################################################################################

# IN-GAME THEME SONGS
GAME_THEMES = load_playlist(traverse_folder('assets/sounds/themes/in_game/'), 16)

################################################################################

# PLAYER IMAGES
PLAYER_IMAGE = load_image('assets/images/player/alive/player_alive_image.png')
PLAYER_IMAGE_DEAD = load_image('assets/images/player/dead/player_dead_image.png')

# PLAYER EAT SEQUENCE ANIMATION
PLAYER_EAT_SEQUENCE = load_images(traverse_folder('assets/images/player/eat_sequence/'), 10)

# PLAYER ACCESSORIES
PLAYER_ACCESSORIES = (
    # const XY offset from player topleft, pygame image pairs
    (pygame.Vector2(x=90, y=70), load_image('assets/images/player/accessories/glasses.png')),
    (pygame.Vector2(x=90, y=3), load_image('assets/images/player/accessories/fedora.png')),
    (pygame.Vector2(x=90, y=-8), load_image('assets/images/player/accessories/propeller_hat.png')),
    (pygame.Vector2(x=90, y=70), load_image('assets/images/player/accessories/3d_glasses.png')),
    (pygame.Vector2(x=88, y=100), load_image('assets/images/player/accessories/blonde_wig.png')),
    (pygame.Vector2(x=110, y=88), load_image('assets/images/player/accessories/moustache_n_monacle.png')),
)

################################################################################

# PREY IMAGES
PREY_IMAGES = load_images(traverse_folder('assets/images/prey/alive/'), 11)

################################################################################

# PREY AURA IMAGE
PREY_AURA = load_image('assets/images/prey/aura/prey_aura_image.png')

################################################################################

# BACKGROUNDS
BACKGROUND_IMAGES = load_images(traverse_folder('assets/images/backgrounds/'), 10)

################################################################################

# HEALTH BAR IMAGES
HEALTH_BAR = {
    "OUTER": load_image('assets/images/bar/bar_outer_image.png'),
    "INNER": load_image('assets/images/bar/bar_inner_image.png')
}

################################################################################

# DAGGER IMAGES                                       
DAGGER_IMAGES = load_images(traverse_folder('assets/images/dagger/'), 7)

################################################################################

# DAGGER FLY SOUNDS
DAGGER_SOUNDS = load_sounds(traverse_folder('assets/sounds/effects/dagger/fly'), 5)

################################################################################

# PLAYER HIT SOUNDS
HIT_SOUNDS = load_sounds(traverse_folder('assets/sounds/effects/player/hit/'), 5)

################################################################################

# PLAYER AURA IMAGE
PLAYER_AURA = load_image('assets/images/player/aura/player_aura_image.png')

################################################################################

# MENU THEME SONGS
MENU_THEMES = load_playlist(traverse_folder('assets/sounds/themes/menu/'), 2)

################################################################################

# MAIN MENU CLICK SOUNDS
MENU_CLICKS = {
    "UPDOWN": load_sound('assets/sounds/effects/menu/menu_click_up_down.mp3'),
    "LEFTRIGHT": load_sound('assets/sounds/effects/menu/menu_click_left_right.mp3'),
    "UNKNOWN": load_sound('assets/sounds/effects/menu/menu_click_unknown.mp3')
}

################################################################################

# PLAYER DASH ABILITY IMAGES
DASH_IMAGES = {
    "AVAIL": load_image('assets/images/player/dash/dash_available_image.png'),
    "UNAVAIL": load_image('assets/images/player/dash/dash_unavailable_image.png')
}

################################################################################

# PLAYER DASH ABILITY SOUNDS
DASH_SOUNDS = load_sounds(traverse_folder('assets/sounds/effects/player/dash/'), 4)
    
################################################################################

# DAGGER FLAME SEQUENCE ANIMATION
FLAME_SEQUENCE = load_images(traverse_folder('assets/images/flame_sequence'), 6)

################################################################################

# CURSOR IMAGE
CURSOR = load_image('assets/images/cursor/cursor_image.png')

################################################################################

# COMIC SANS MS FONT
COMIC_SANS_MS = resource_path("assets/fonts/comic_sans_ms.ttf")

################################################################################