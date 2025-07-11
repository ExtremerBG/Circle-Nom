from circle_nom.systems.timer import Timer
import pygame

# Pygame screen size constants
WIDTH, HEIGHT = 1280, 720

# Display init
pygame.display.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Font & mixer init
pygame.font.init()
pygame.mixer.init()

# Import profiler and Menu class after pygame import & inits
from circle_nom.helpers.profile import profile
from circle_nom.ui.menu import Menu

# Create a new Timer thread
timer = Timer(name="TimerThread", debug=False)

# Set True to enable performance profiling
profile(enable=False, func=Menu(screen=screen, timer=timer).launch_main_menu)