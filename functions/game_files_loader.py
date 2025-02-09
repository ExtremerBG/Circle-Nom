import gif_pygame.gif_pygame
from functions.game_funcs import resource_path
import gif_pygame
import pygame

pygame.mixer.init()

################################################################################

# EAT SOUNDS
directories = [
    resource_path('sound/effects/nom/nom_1.mp3'),
    resource_path('sound/effects/nom/nom_2.mp3'),
    resource_path('sound/effects/nom/nom_3.mp3'),
    resource_path('sound/effects/nom/nom_4.mp3'),
    resource_path('sound/effects/nom/nom_5.mp3')
]
eat_sounds: list[pygame.mixer.Sound] = []
for path in directories:
    eat_sounds.append(pygame.mixer.Sound(path))

################################################################################

# THEME SONGS
theme_songs = [
    resource_path('sound/themes/theme_song_1.mp3'),
    resource_path('sound/themes/theme_song_2.mp3'),
    resource_path('sound/themes/theme_song_3.mp3'),
    resource_path('sound/themes/theme_song_4.mp3'),
    resource_path('sound/themes/theme_song_5.mp3'),
    resource_path('sound/themes/theme_song_6.mp3'),
    resource_path('sound/themes/theme_song_7.mp3'),
    resource_path('sound/themes/theme_song_8.mp3'),
    resource_path('sound/themes/theme_song_9.mp3'),
    resource_path('sound/themes/theme_song_10.mp3'),
    resource_path('sound/themes/theme_song_11.mp3'),
    resource_path('sound/themes/theme_song_12.mp3'),
    resource_path('sound/themes/theme_song_13.mp3'),
    resource_path('sound/themes/theme_song_14.mp3'),
    resource_path('sound/themes/theme_song_15.mp3')
]

################################################################################

# PLAYER IMAGES
directories = [
    resource_path('image/player_alive/player_image_1.png'),
    resource_path('image/player_alive/player_image_2.png'),
    resource_path('image/player_alive/player_image_3.png')
]
player_images: list[pygame.Surface] = []
for path in directories:
    player_images.append(pygame.image.load(path))

directories = [
    resource_path('image/player_dead/player_image_1_dead.png'),
    resource_path('image/player_dead/player_image_2_dead.png'),
    resource_path('image/player_dead/player_image_3_dead.png')
]
player_images_dead: list[pygame.Surface] = []
for path in directories:
    player_images_dead.append(pygame.image.load(path))

# Error message if lengths of player lists are different
if len(player_images) != len(player_images_dead):
    raise ValueError("Lengths of player images lists are different!")

################################################################################

# PREY IMAGES
directories = [
    resource_path('image/prey/prey_image_1.png'),
    resource_path('image/prey/prey_image_2.png'),
    resource_path('image/prey/prey_image_3.png'),
    resource_path('image/prey/prey_image_4.png'),
    resource_path('image/prey/prey_image_5.png'),
    resource_path('image/prey/prey_image_6.png'),
    resource_path('image/prey/prey_image_7.png'),
    resource_path('image/prey/prey_image_8.png'),
    resource_path('image/prey/prey_image_9.png'),
    resource_path('image/prey/prey_image_10.png'),
    resource_path('image/prey/prey_image_11.png')
]
prey_images = []
for path in directories:
    prey_images.append(pygame.image.load(path))

################################################################################

# PREY AURA
prey_aura = pygame.image.load(resource_path('image/prey/prey_aura.png'))

################################################################################

# BACKGROUNDS
directories = [
    resource_path('image/backgrounds/background_image_1.jpg'),
    resource_path('image/backgrounds/background_image_2.jpg'),
    resource_path('image/backgrounds/background_image_3.jpg')
]
background_images: list[pygame.Surface] = []
for path in directories:
    background_images.append(pygame.image.load(path))

################################################################################

# HUNGER BAR
directories = [
    resource_path('image/bar/hunger_bar_inner.png'),
    resource_path('image/bar/hunger_bar_outer.png')
]
hunger_bar: list[pygame.Surface] = []
for path in directories:
    hunger_bar.append(pygame.image.load(path))

################################################################################

# DAGGER
directories = [
    resource_path('image/dagger/flame_dagger_right.gif'), # GIF PYGAME FILE!
    resource_path('image/dagger/flame_dagger_left.gif'), # GIF PYGAME FILE!
    resource_path('image/dagger/flame_dagger_up.gif'), # GIF PYGAME FILE!
    resource_path('image/dagger/flame_dagger_down.gif'), # GIF PYGAME FILE!
    resource_path('image/dagger/dagger_image_1.png')
]
dagger_images: list[pygame.Surface] = [pygame.image.load(directories.pop())]
for path in directories:
    dagger_images.append(gif_pygame.load(path))

################################################################################

# DAGGER FLY SOUNDS
directories = [
    resource_path('sound/effects/dagger/fly/dagger_whoosh_1.mp3'),
    resource_path('sound/effects/dagger/fly/dagger_whoosh_2.mp3'),
    resource_path('sound/effects/dagger/fly/dagger_whoosh_3.mp3'),
]
dagger_sounds: list[pygame.mixer.Sound] = []
for path in directories:
    dagger_sounds.append(pygame.mixer.Sound(path))

################################################################################

# DAGGER HIT SOUNDS
directories = [
    resource_path('sound/effects/dagger/hit/dagger_ouch_1.mp3'),
    resource_path('sound/effects/dagger/hit/dagger_ouch_2.mp3'),
    resource_path('sound/effects/dagger/hit/dagger_ouch_3.mp3'),
    resource_path('sound/effects/dagger/hit/dagger_ouch_4.mp3'),
    resource_path('sound/effects/dagger/hit/dagger_ouch_5.mp3')
]
hit_sounds: list[pygame.mixer.Sound] = []
for path in directories:
    hit_sounds.append(pygame.mixer.Sound(path))

################################################################################

# PLAYER AURA IMAGE - USED IN MENU
player_aura = pygame.image.load(resource_path('image/menu/aura.png'))

################################################################################

# MAIN MENU THEMES
main_menu_themes = [
    resource_path('sound/menu/menu_theme_song_1.mp3')
]

################################################################################

# MAIN MENU CLICKS
directories = [
    resource_path('sound/menu/menu_click_up_down.mp3'),
    resource_path('sound/menu/menu_click_left_right.mp3'),
    resource_path('sound/menu/menu_click_unknown.mp3'),
]
main_menu_clicks: list[pygame.mixer.Sound] = []
for path in directories:
    main_menu_clicks.append(pygame.mixer.Sound(path))

################################################################################