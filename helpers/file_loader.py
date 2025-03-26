from helpers.functions import *

################################################################################

# PYGAME WINDOW ICON
icon = load_image(resource_path('image/icon/icon.ico'))

################################################################################

# EAT SOUNDS
eat_sounds = load_sounds(traverse_folder('sound/effects/player/eat/'), 5)

################################################################################

# GAME THEME SONGS
game_themes = load_playlist(traverse_folder('sound/themes/in_game/'), 15)

################################################################################

# PLAYER IMAGES
player_images = load_images(traverse_folder('image/player/alive/'), 3)
player_images_dead = load_images(traverse_folder('image/player/dead/'), 3)

################################################################################

# PREY IMAGES
prey_images = load_images(traverse_folder('image/prey/alive/'), 11)

################################################################################

# PREY AURA
prey_aura = load_image(resource_path('image/prey/aura/prey_aura_image.png'))

################################################################################

# BACKGROUNDS
background_images = load_images(traverse_folder('image/backgrounds/'), 10)

################################################################################

# HUNGER BAR
health_bar = load_images(traverse_folder('image/bar/'), 2)

################################################################################

# DAGGER                                            
dagger_images = load_images(traverse_folder('image/dagger/'), 7)

################################################################################

# DAGGER FLY SOUNDS
dagger_sounds = load_sounds(traverse_folder('sound/effects/dagger/fly'), 5)

################################################################################

# PLAYER HIT SOUNDS
hit_sounds = load_sounds(traverse_folder('sound/effects/player/hit/'), 5)

################################################################################

# PLAYER AURA
player_aura = load_image(resource_path('image/player/aura/player_aura_image.png'))

################################################################################

# MENU THEME SONGS
menu_themes = load_playlist(traverse_folder('sound/themes/menu/'), 2)

################################################################################

# MAIN MENU CLICKS
menu_clicks = {
    "UPDOWN": load_sound('sound/effects/menu/menu_click_up_down.mp3'),
    "LEFTRIGHT": load_sound('sound/effects/menu/menu_click_left_right.mp3'),
    "UNKNOWN": load_sound('sound/effects/menu/menu_click_unknown.mp3'),
}

################################################################################

# DASH IMAGES
dash_images = load_images(traverse_folder('image/player/dash/'), 2)

################################################################################

# DASH SOUNDS
dash_sounds = load_sounds(traverse_folder('sound/effects/player/dash/'), 4)
    
################################################################################

# FLAME SEQUENCE
flame_sequence = load_images(traverse_folder('image/flame_sequence'), 6)

################################################################################