from helpers.functions import resource_path
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
temp: list[pygame.mixer.Sound] = []
for path in directories:
    temp.append(pygame.mixer.Sound(path))
eat_sounds = tuple(temp)

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
temp: list[pygame.Surface] = []
for path in directories:
    temp.append(pygame.image.load(path))
player_images = tuple(temp)

directories = [
    resource_path('image/player_dead/player_image_1_dead.png'),
    resource_path('image/player_dead/player_image_2_dead.png'),
    resource_path('image/player_dead/player_image_3_dead.png')
]
temp: list[pygame.Surface] = []
for path in directories:
    temp.append(pygame.image.load(path))
player_images_dead = tuple(temp)

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
temp: list[pygame.Surface] = []
for path in directories:
    temp.append(pygame.image.load(path))
prey_images = tuple(temp)

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
temp: list[pygame.Surface] = []
for path in directories:
    temp.append(pygame.image.load(path))
background_images = tuple(temp)

################################################################################

# HUNGER BAR
directories = [
    resource_path('image/bar/hunger_bar_inner.png'),
    resource_path('image/bar/hunger_bar_outer.png')
]
temp: list[pygame.Surface] = []
for path in directories:
    temp.append(pygame.image.load(path))
health_bar = tuple(temp)

################################################################################

# DAGGER
directories = [
    resource_path('image/dagger/flame_dagger_right.gif'), # GIF-PYGAME FILE!
    resource_path('image/dagger/flame_dagger_left.gif'), # GIF-PYGAME FILE!
    resource_path('image/dagger/flame_dagger_up.gif'), # GIF-PYGAME FILE!
    resource_path('image/dagger/flame_dagger_down.gif'), # GIF-PYGAME FILE!
    resource_path('image/dagger/dagger_image_1.png') # PYGAME FILE
]                                                    # pop the only pygame file from end
temp: list[pygame.Surface|gif_pygame.GIFPygame] = [pygame.image.load(directories.pop())]
for path in directories:
    temp.append(gif_pygame.load(path))
dagger_images = tuple(temp)

################################################################################

# DAGGER FLY SOUNDS
directories = [
    resource_path('sound/effects/dagger/fly/whoosh_1.mp3'),
    resource_path('sound/effects/dagger/fly/whoosh_2.mp3'),
    resource_path('sound/effects/dagger/fly/whoosh_3.mp3'),
    resource_path('sound/effects/dagger/fly/whoosh_4.mp3'),
    resource_path('sound/effects/dagger/fly/whoosh_5.mp3')
]
temp: list[pygame.mixer.Sound] = []
for path in directories:
    temp.append(pygame.mixer.Sound(path))
dagger_sounds = tuple(temp)

################################################################################

# PLAYER-DAGGER HIT SOUNDS
directories = [
    resource_path('sound/effects/dagger/hit/dagger_ouch_1.mp3'),
    resource_path('sound/effects/dagger/hit/dagger_ouch_2.mp3'),
    resource_path('sound/effects/dagger/hit/dagger_ouch_3.mp3'),
    resource_path('sound/effects/dagger/hit/dagger_ouch_4.mp3'),
    resource_path('sound/effects/dagger/hit/dagger_ouch_5.mp3')
]
temp: list[pygame.mixer.Sound] = []
for path in directories:
    temp.append(pygame.mixer.Sound(path))
hit_sounds = tuple(temp)

################################################################################

# PLAYER AURA
player_aura = pygame.image.load(resource_path('image/menu/aura.png'))

################################################################################

# MAIN MENU THEMES
main_menu_themes = [
    resource_path('sound/menu/menu_theme_song_1.mp3'),
    resource_path('sound/menu/menu_theme_song_2.mp3')
]

################################################################################

# MAIN MENU CLICKS
directories = [
    resource_path('sound/menu/menu_click_up_down.mp3'),
    resource_path('sound/menu/menu_click_left_right.mp3'),
    resource_path('sound/menu/menu_click_unknown.mp3')
]
temp: list[pygame.mixer.Sound] = []
for path in directories:
    temp.append(pygame.mixer.Sound(path))
main_menu_clicks = tuple(temp)

################################################################################

# DASH IMAGES
directories = [
    resource_path('image/dash/dash_unavailable.png'),
    resource_path('image/dash/dash_available.png')
]
temp: list[pygame.Surface] = []
for path in directories:
    temp.append(pygame.image.load(path))
dash_images = tuple(temp)

################################################################################

# DASH SOUNDS
directories = [
    resource_path('sound/effects/dash/whoosh_1.mp3'),
    resource_path('sound/effects/dash/whoosh_2.mp3'),
    resource_path('sound/effects/dash/whoosh_3.mp3'),
    resource_path('sound/effects/dash/whoosh_4.mp3')
]
temp: list[pygame.mixer.Sound] = []
for path in directories:
    temp.append(pygame.mixer.Sound(path))
dash_sounds = tuple(temp)
    
################################################################################