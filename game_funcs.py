import pygame
import random
import sys
import os

# Function for resource path
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Function for random screen position
def rand_screen_pos():
    
    # Screen size: width 1280 x height 720
    # Bias for return positions
    # 80% Chance to return closer to edge
    # 20% chance to return closer to middle

    bias_edge = random.randrange(1, 100)

    # Return closer to top left
    if bias_edge <= 20:
        # Debug print
        # print("TOP LEFT")
        return random.randint(64, 448), random.randint(36, 288)
    
    # Return closer to bottom right
    elif bias_edge > 20 and bias_edge <= 40:
        # Debug print
        # print("BOTTOM RIGHT")
        return random.randint(832, 1216), random.randint(432, 648)
    
    # Return closer to bottom left
    elif bias_edge > 40 and bias_edge <= 60:
        # Debug print
        # print("BOTTOM LEFT")
        return random.randint(64, 448), random.randint(432, 648)
    
    # Return closer to top right
    elif bias_edge > 60 and bias_edge <= 80:
        # Debug print
        # print("TOP RIGHT")
        return random.randint(832, 1216), random.randint(36, 288)

    # Return closer to center
    else:
        # Debug print
        # print("CENTER")
        return random.randint(480, 960), random.randint(270, 540)

# Function for random rotation
def rand_rotation():
    return random.randint(0, 360)

# Function for rotating image
def image_rotate(image, angle):
    return pygame.transform.rotate(image, angle)
