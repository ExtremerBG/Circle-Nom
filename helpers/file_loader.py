from helpers.functions import load_images, load_sounds, resource_path, safe_load_image
import pygame

pygame.mixer.init()

################################################################################

# EAT SOUNDS
paths = (
    'sound/effects/player/eat/player_eat_1.mp3',
    'sound/effects/player/eat/player_eat_2.mp3',
    'sound/effects/player/eat/player_eat_3.mp3',
    'sound/effects/player/eat/player_eat_4.mp3',
    'sound/effects/player/eat/player_eat_5.mp3'
)
eat_sounds = load_sounds(paths)

################################################################################

# THEME SONGS
theme_songs = (
    resource_path('sound/themes/in_game/in_game_theme_1.mp3'),
    resource_path('sound/themes/in_game/in_game_theme_2.mp3'),
    resource_path('sound/themes/in_game/in_game_theme_3.mp3'),
    resource_path('sound/themes/in_game/in_game_theme_4.mp3'),
    resource_path('sound/themes/in_game/in_game_theme_5.mp3'),
    resource_path('sound/themes/in_game/in_game_theme_6.mp3'),
    resource_path('sound/themes/in_game/in_game_theme_7.mp3'),
    resource_path('sound/themes/in_game/in_game_theme_8.mp3'),
    resource_path('sound/themes/in_game/in_game_theme_9.mp3'),
    resource_path('sound/themes/in_game/in_game_theme_10.mp3'),
    resource_path('sound/themes/in_game/in_game_theme_11.mp3'),
    resource_path('sound/themes/in_game/in_game_theme_12.mp3'),
    resource_path('sound/themes/in_game/in_game_theme_13.mp3'),
    resource_path('sound/themes/in_game/in_game_theme_14.mp3'),
    resource_path('sound/themes/in_game/in_game_theme_15.mp3')
)

################################################################################

# PLAYER IMAGES
paths = (
    'image/player/alive/player_alive_image_1.png',
    'image/player/alive/player_alive_image_2.png',
    'image/player/alive/player_alive_image_3.png'
)
player_images = load_images(paths)

paths = (
    'image/player/dead/player_dead_image_1.png',
    'image/player/dead/player_dead_image_2.png',
    'image/player/dead/player_dead_image_3.png'
)
player_images_dead = load_images(paths)

# Error message if lengths of player lists are different
if len(player_images) != len(player_images_dead):
    raise ValueError("Lengths of player images lists are different!")

################################################################################

# PREY IMAGES
paths = (
    'image/prey/prey_image_1.png',
    'image/prey/prey_image_2.png',
    'image/prey/prey_image_3.png',
    'image/prey/prey_image_4.png',
    'image/prey/prey_image_5.png',
    'image/prey/prey_image_6.png',
    'image/prey/prey_image_7.png',
    'image/prey/prey_image_8.png',
    'image/prey/prey_image_9.png',
    'image/prey/prey_image_10.png',
    'image/prey/prey_image_11.png'
)
prey_images = load_images(paths)

################################################################################

# PREY AURA
prey_aura = safe_load_image(resource_path('image/prey/prey_aura_image.png'))

################################################################################

# BACKGROUNDS
paths = (
    'image/backgrounds/background_image_1.jpg',
    'image/backgrounds/background_image_2.jpg',
    'image/backgrounds/background_image_3.jpg',
    'image/backgrounds/background_image_4.jpg',
    'image/backgrounds/background_image_5.jpg',
    'image/backgrounds/background_image_6.jpg',
    'image/backgrounds/background_image_7.jpg',
    'image/backgrounds/background_image_8.jpg',
    'image/backgrounds/background_image_9.jpg',
    'image/backgrounds/background_image_10.jpg',
)
background_images = load_images(paths)

################################################################################

# HUNGER BAR
paths = (
    'image/bar/bar_inner_image.png',
    'image/bar/bar_outer_image.png'
)
health_bar = load_images(paths)

################################################################################

# DAGGER
paths = (
    'image/dagger/dagger_image_1.png',
    'image/dagger/flame_dagger_right.gif',
    'image/dagger/flame_dagger_left.gif',
    'image/dagger/flame_dagger_up.gif',
    'image/dagger/flame_dagger_down.gif'
)                                                    
dagger_images = load_images(paths)

################################################################################

# DAGGER FLY SOUNDS
paths = (
    'sound/effects/dagger/fly/dagger_fly_1.mp3',
    'sound/effects/dagger/fly/dagger_fly_2.mp3',
    'sound/effects/dagger/fly/dagger_fly_3.mp3',
    'sound/effects/dagger/fly/dagger_fly_4.mp3',
    'sound/effects/dagger/fly/dagger_fly_5.mp3'
)
dagger_sounds = load_sounds(paths)

################################################################################

# PLAYER HIT SOUNDS
paths = (
    'sound/effects/player/hit/player_hit_1.mp3',
    'sound/effects/player/hit/player_hit_2.mp3',
    'sound/effects/player/hit/player_hit_3.mp3',
    'sound/effects/player/hit/player_hit_4.mp3',
    'sound/effects/player/hit/player_hit_5.mp3'
)
hit_sounds = load_sounds(paths)

################################################################################

# PLAYER AURA
player_aura = safe_load_image(resource_path('image/player/aura/player_aura_image.png'))

################################################################################

# MAIN MENU THEMES
main_menu_themes = (
    resource_path('sound/themes/menu/menu_theme_1.mp3'),
    resource_path('sound/themes/menu/menu_theme_2.mp3')
)

################################################################################

# MAIN MENU CLICKS
paths = (
    'sound/effects/menu/menu_click_up_down.mp3',
    'sound/effects/menu/menu_click_left_right.mp3',
    'sound/effects/menu/menu_click_unknown.mp3'
)
main_menu_clicks = load_sounds(paths)

################################################################################

# DASH IMAGES
paths = (
    'image/player/dash/dash_unavailable_image.png',
    'image/player/dash/dash_available_image.png'
)
dash_images = load_images(paths)

################################################################################

# DASH SOUNDS
paths = (
    'sound/effects/player/dash/player_dash_1.mp3',
    'sound/effects/player/dash/player_dash_2.mp3',
    'sound/effects/player/dash/player_dash_3.mp3',
    'sound/effects/player/dash/player_dash_4.mp3'
)
dash_sounds = load_sounds(paths)
    
################################################################################