# Import pygame first
import pygame

# Pygame window size constants
WIDTH, HEIGHT = 1280, 720

# Display init
pygame.display.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Font & mixer init
pygame.font.init()
pygame.mixer.init()

# Import profiler and Menu class after pygame inits
from helpers.profile import profile
from models.menu import Menu

 # Set True to enable performance profiling
profile(False, Menu(screen).launch_main)