from random import uniform, randint
from typing import Any, Callable
import pygame

def declare_objects(count: int, func: Callable, *args: Any) -> tuple:
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

def rand_screen_pos(screen: pygame.Surface) -> pygame.Vector2:
    """
    Generate a random position on the screen with a bias towards screen edges.
    
    Args:
        screen (pygame.Surface): Reference to the game screen.

    Returns:
        Vector2: A pygame.Vector2 obj containing the x and y coordinates of the random position.
    """
    MARGIN = 100
    WIDTH = screen.width
    HEIGHT = screen.height
    
    # 4/5 Times should return screen position closer to one of the screen edges
    bias_edge = randint(0, 100)
    
    # Return closer to top left
    if bias_edge <= 20:
        return pygame.Vector2(x=uniform(MARGIN, WIDTH / 3), y=uniform(MARGIN, HEIGHT / 3))
    
    # Return closer to top right
    elif bias_edge > 20 and bias_edge <= 40:
        return pygame.Vector2(x=uniform(WIDTH - WIDTH / 3, WIDTH - MARGIN), y=uniform(MARGIN, HEIGHT / 3))
    
    # Return closer to bottom left
    elif bias_edge > 40 and bias_edge <= 60:
        return pygame.Vector2(x=uniform(MARGIN, HEIGHT - HEIGHT / 3), y=uniform(HEIGHT - HEIGHT / 3, HEIGHT - MARGIN))
    
    # Return closer to bottom right
    elif bias_edge > 60 and bias_edge <= 80:
        return pygame.Vector2(x=uniform(WIDTH - WIDTH / 3, WIDTH - MARGIN), y=uniform(HEIGHT - HEIGHT / 3, HEIGHT - MARGIN))

    # Return closer to center
    else:
        return pygame.Vector2(x=uniform(WIDTH / 3, WIDTH - WIDTH / 3), y=uniform(HEIGHT / 3, HEIGHT - HEIGHT / 3))

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

def draw_fps(screen: pygame.Surface, clock: pygame.Clock, font: pygame.Font) -> None:
    """
    Draw rounded FPS onto screen from the pygame Clock.
    
    Args:
        screen (pygame.Surface): The game screen.
        clock (pygame.Clock): The game clock.
        font (pygame.Font): The font to draw the fps text with.
    """
    fps = round(clock.get_fps())
    if fps >= 29:
        fps_display = font.render(f'FPS: {fps}', True, (255, 255, 255))
        screen.blit(fps_display, ((screen.width - fps_display.width - 10), screen.height - 25))
    else:
        fps_display = font.render(f'FPS: {fps}', True, (255, 0, 0))
        screen.blit(fps_display, ((screen.width - fps_display.width - 10), screen.height - 25))
    
def draw_music_name(screen: pygame.Surface, music_name: str, font: pygame.Font) -> None:
    """
    Draw music name onto the screen.
    
    Args:
        screen (pygame.Surface): The game screen.
        music_name (str): The music name.
        font (pygame.Font): The font to draw the music name with.
    """
    pos = 10, screen.height - 25
    screen.blit(font.render(text=music_name, antialias=True, color="WHITE"), pos)