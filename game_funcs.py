import pygame
from random import randint
import sys
import os

def resource_path(relative_path):
    """ Function for absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def rand_screen_pos():
    
    """
    Function for random screen position, size is: width 1280 x height 720. \n
    Bias for return positions: 80% Chance to return closer to edge / 20% chance to return closer to middle.
    Return: output [X, Y] coordinates
    """

    bias_edge = rand_num(100)

    # Return closer to top left
    if bias_edge <= 20:
        # Debug print
        # print("TOP LEFT")
        return randint(64, 448), randint(36, 288)
    
    # Return closer to bottom right
    elif bias_edge > 20 and bias_edge <= 40:
        # Debug print
        # print("BOTTOM RIGHT")
        return randint(832, 1216), randint(432, 648)
    
    # Return closer to bottom left
    elif bias_edge > 40 and bias_edge <= 60:
        # Debug print
        # print("BOTTOM LEFT")
        return randint(64, 448), randint(432, 648)
    
    # Return closer to top right
    elif bias_edge > 60 and bias_edge <= 80:
        # Debug print
        # print("TOP RIGHT")
        return randint(832, 1216), randint(36, 288)

    # Return closer to center
    else:
        # Debug print
        # print("CENTER")
        return randint(480, 960), randint(270, 540)

def rand_num(num: int):
    """ 
    Returns a random integer from endpoints [0, num - 1] \n
    If num < 0, returns 0. \n
    Parameter 1: input number \n
    Return: output number
    """
    if num > 0:
        return randint(0, num - 1)
    else:
        return 0

def image_rotate(image, angle):
    """ 
    Rotates a given pygame image to a given angle. \n
    Parameter 1: input pygame image \n
    Parameter 2: input angle \n
    Return: rotated pygame image
    """
    return pygame.transform.rotate(image, angle)
