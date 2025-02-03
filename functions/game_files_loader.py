from functions.game_funcs import resource_path
import gif_pygame
import pygame

pygame.mixer.init()

################################################################################

# EAT SOUNDS
directories = [
    resource_path('sounds/nom_1.mp3'),
      resource_path('sounds/nom_2.mp3'),
       resource_path('sounds/nom_3.mp3'),
        resource_path('sounds/nom_4.mp3'),
          resource_path('sounds/nom_5.mp3')
]
eat_sounds:list[pygame.mixer.Sound] = []
for path in directories:
    eat_sounds.append(pygame.mixer.Sound(path))

################################################################################

# THEME SONGS - LOADED IN MAIN FILE
theme_songs = [
    resource_path('sounds/theme_song_1.mp3'),
      resource_path('sounds/theme_song_2.mp3'),
        resource_path('sounds/theme_song_3.mp3'),
          resource_path('sounds/theme_song_4.mp3'),
            resource_path('sounds/theme_song_5.mp3')
]

################################################################################

# PLAYER IMAGES
directories = [
    resource_path('images/player_image_1.png'),
      resource_path('images/player_image_2.png'),
        resource_path('images/player_image_3.png')
]
player_images:list[pygame.Surface] = []
for path in directories:
    player_images.append(pygame.image.load(path))

directories = [
    resource_path('images/player_image_1_dead.png'),
      resource_path('images/player_image_2_dead.png'),
        resource_path('images/player_image_3_dead.png')
]
player_images_dead:list[pygame.Surface] = []
for path in directories:
    player_images_dead.append(pygame.image.load(path))
  
# Error message if lengths of player lists are different
if len(player_images) != len(player_images_dead):
    raise ValueError("Lenghts of player images lists are different!")

################################################################################

# PREY IMAGES
directories = [
    resource_path('images/glowing_sandwich.png'), # GIF PYGAME FILE!
      resource_path('images/prey_image_1.png'),
        resource_path('images/prey_image_2.png'),
          resource_path('images/prey_image_3.png'),
            resource_path('images/prey_image_4.png'),
              resource_path('images/prey_image_5.png'),
                resource_path('images/prey_image_6.png'),
                  resource_path('images/prey_image_7.png'),
                    resource_path('images/prey_image_8.png'),
                      resource_path('images/prey_image_9.png'),
                        resource_path('images/prey_image_10.png')
]
prey_images = []
prey_images.append(gif_pygame.load(directories[0]))
for i in range(1, len(directories)-1):
    prey_images.append(pygame.image.load(directories[i]))

################################################################################

# BACKGROUNDS
directories = [
    resource_path('images/background_image_1.jpg'),
      resource_path('images/background_image_2.jpg'),
        resource_path('images/background_image_3.jpg')
]
background_images:list[pygame.Surface] = []
for path in directories:
    background_images.append(pygame.image.load(path))

################################################################################

# HUNGER BAR
directories = [
    resource_path('images/hunger_bar_inner.png'),
      resource_path('images/hunger_bar_outer.png')
]
hunger_bar:list[pygame.Surface] = []
for path in directories:
    hunger_bar.append(pygame.image.load(path))

################################################################################