from random import randint
import pygame
import sys
import os

def resource_path(relative_path):
    """
    Generate a random number within the given limit.

    Args:
        limit (int): The upper limit for the random number.

    Returns:
        int: A random number within the limit.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def rand_screen_pos():
    
    """
    Generate a random position on the screen.

    Returns:
        tuple: A tuple containing the x and y coordinates of the random position.
    """

    bias_edge = rand_num(100)

    # Return closer to top left
    if bias_edge <= 20:
        return randint(64, 448), randint(36, 288)
    
    # Return closer to bottom right
    elif bias_edge > 20 and bias_edge <= 40:
        return randint(832, 1216), randint(432, 648)
    
    # Return closer to bottom left
    elif bias_edge > 40 and bias_edge <= 60:
        return randint(64, 448), randint(432, 648)
    
    # Return closer to top right
    elif bias_edge > 60 and bias_edge <= 80:
        return randint(832, 1216), randint(36, 288)

    # Return closer to center
    else:
        return randint(480, 960), randint(270, 540)

def rand_num(num: int) -> int:
    """
    Generate a random number within the given limit.

    Args:
        limit (int): The upper limit for the random number.

    Returns:
        int: A random number within the limit - 1.
    """
    if num > 0:
        return randint(0, num - 1)
    else:
        return 0

def image_rotate(image, angle):
    """
    Rotates the given image by the specified angle.

    Args:
        image (pygame.Surface): The image to rotate.
        angle (float): The angle to rotate the image.

    Returns:
        pygame.Surface: The rotated image.
    """
    return pygame.transform.rotate(image, angle)
