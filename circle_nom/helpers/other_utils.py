from typing import Callable
from random import uniform
import pygame

def declare_objects(count: int, func: Callable[..., any], *args: any) -> tuple:
    """
    Declares a given count of objects and returns a tuple.
            
    Usage:
        objects = declare_objects(2, Dagger, dagger_images, screen)
            
    Args:
        count (int): The number of objects to declare.
        func (Callable): The given function, method or Class to invoke.
        *args (Any): The arguments for the func.
                
    Returns:
        tuple: A tuple containing the declared objects.
    """
    return tuple(func(*args) for _ in range(count))

def rand_screen_pos() -> pygame.Vector2:
    """
    Generate a random position on the screen with a bias towards screen edges.

    Returns:
        Vector2: A pygame.Vector2 obj containing the x and y coordinates of the random position.
    """
    bias_edge = uniform(0, 100)
    
    # Return closer to top left
    if bias_edge <= 20:
        return pygame.Vector2(uniform(64, 448), uniform(36, 288))
    
    # Return closer to bottom right
    elif bias_edge > 20 and bias_edge <= 40:
        return pygame.Vector2(uniform(832, 1216), uniform(432, 648))
    
    # Return closer to bottom left
    elif bias_edge > 40 and bias_edge <= 60:
        return pygame.Vector2(uniform(64, 448), uniform(432, 648))
    
    # Return closer to top right
    elif bias_edge > 60 and bias_edge <= 80:
        return pygame.Vector2(uniform(832, 1216), uniform(36, 288))

    # Return closer to center
    else:
        return pygame.Vector2(uniform(480, 960), uniform(270, 540))

def rot_center(image: pygame.Surface, angle: int | float, xy) -> tuple[pygame.Surface, pygame.Rect]:
    """
    Rotate an image around its center.

    Args:
        image (pygame.Surface): The image to rotate.
        angle (int | float): The angle to rotate the image.
        xy (tuple): The center point to rotate around.

    Returns:
        tuple: The rotated image and its new rectangle.
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=xy).center)
    return rotated_image, new_rect

def draw_fps(screen:pygame.Surface, clock:pygame.Clock, text:pygame.Font) -> None:
    """
    Draw rounded FPS onto screen from the pygame Clock.
    
    Args:
        screen (pygame.Surface): The game screen.
        clock (pygame.Clock): The game clock.
        text (pygame.Font): The font to draw the fps text with.
    """
    fps = round(clock.get_fps())
    coords = 1205, 695
    if fps >= 29:
        fps_display = text.render(f'FPS: {fps}', True, (255, 255, 255))
        screen.blit(fps_display, coords)
    else:
        fps_display = text.render(f'FPS: {fps}', True, (255, 0, 0))
        screen.blit(fps_display, coords)