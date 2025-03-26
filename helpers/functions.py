from typing import Callable
from random import uniform
from math import isclose
import inspect
import pygame
import sys
import os
import re

def resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a resource, works for PyInstaller.

    Args:
        relative_path (str): The relative path to the resource.

    Returns:
        str: The absolute path to the resource.
    """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def func_message(level: str) -> str:
    """
    Generate a formatted message with the current function name.
    
    Args:
        level (str): The log level (e.g. 'WARN', 'ERROR').
    """
    frame = inspect.currentframe().f_back # get caller's name
    func_name = frame.f_code.co_name
    return f'[{level}] func {func_name} says: '

def add_placeholders(num: int, key: str) -> list[str]:
    """
    Return a list with paths to placeholder image/s or sound/s. Note that the returned paths are \n
    already resolved with resource_path(), so there is no need to use the function again.
    
    Args:
        num (int): The number of placeholders.
        key (str): The placeholder type. Can be "IMAGE" or "SOUND".
    """
    key = key.upper()
    
    MISSING_RESOURCES = {
    "IMAGE": 'image/error/missing_image.png',
    "SOUND": 'sound/error/missing_sound.mp3'
    }
    
    if key not in MISSING_RESOURCES.keys():
        raise ValueError(func_message('ERROR') + f"Invalid key '{key}'! Must be 'IMAGE' or 'SOUND'.")
    if num < 0:
        raise ValueError(func_message('ERROR' + "Invalid number of placeholders."))
    
    resolved_path = resource_path(MISSING_RESOURCES[key])
    
    if not os.path.exists(resolved_path):
        raise ValueError(func_message('ERROR') + f"Path '{resolved_path}' not found!")
    
    return [resolved_path for _ in range(num)]

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

def check_screen_bounds(screen: pygame.Surface, player) -> None:
    """
    Check if the player is outside the screen bounds and adjust position if necessary.

    Args:
        screen (pygame.Surface): The game screen.
        player: The player object with position attributes.
    """
    if player.position.x >= screen.get_width():
        player.position.x = screen.get_width() - 1

    if player.position.y >= screen.get_height(): 
         player.position.y = screen.get_height() - 1

    if player.position.x <= 0:
        player.position.x = 1

    if player.position.y <= 0:
        player.position.y = 1

def check_player_collision(player_1, player_2, dt: float) -> None:
    """
    Check if player_1 collides with player_2 and adjust positions if necessary.

    Args:
        player_1: The first player object with position and collision tolerance attributes.
        player_2: The second player object with position and collision tolerance attributes.
        dt (float): Delta time for frame-independent calculation.
    """
    if isclose(player_1.position.x, player_2.position.x, abs_tol=player_1.collision_tol) and \
    isclose(player_1.position.y, player_2.position.y, abs_tol=player_1.collision_tol):
        dx = 120 if player_1.position.x > player_2.position.x else -120
        dy = 120 if player_1.position.y > player_2.position.y else -120
        player_1.position.x += dx * dt
        player_2.position.x -= dx * dt
        player_1.position.y += dy * dt
        player_2.position.y -= dy * dt
            
def player_control(player, dt: float, arrows: bool, wasd: bool):
    """
    Control the player movement and dash based on keyboard input.

    Args:
        player: The player object with position, size, and speed attributes.
        dt (float): Delta time, used for frame-independent drawing.
        arrows (bool): Arrows control mode.
        wasd (bool): WASD control mode.
    """
    MOVEMENT_RATE = player_movement_rate(player, dt)
    direction = pygame.Vector2(0, 0)
    keys = pygame.key.get_pressed()

    # Dictionary with Key: Movement pairs
    movement_keys = {
        pygame.K_w: (0, -1), pygame.K_s: (0, 1),
        pygame.K_a: (-1, 0), pygame.K_d: (1, 0),
        pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1),
        pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)
    }

    # Player movement
    for key, (dx, dy) in movement_keys.items():
        if (arrows and key in {pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT}) or \
           (wasd and key in {pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d}):
            if keys[key]:
                direction.x += dx
                direction.y += dy

    # Separate dash for WASD and arrows
    if wasd and keys[pygame.K_LSHIFT]:
        player.dash()
    if arrows and keys[pygame.K_RSHIFT]:
        player.dash()

    # Apply current player movement rate
    if direction.length() > 0:
        player.position += direction.normalize() * MOVEMENT_RATE
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

def player_movement_rate(player, dt:float) -> float:
    """
    Get player movement rate number from formula.
    
    Args:
        player (Player): The Player object.
        dt (float): Delta time for frame-independent calculation.
    """
    SCALE_FACTOR = 100
    EXPONENT = 0.25
    return ((SCALE_FACTOR / (player.size ** EXPONENT)) * player.speed) * dt

def player_size_reduct(player, dt:float) -> float:
    """
    Get player size reduction number from formula.
    
    Args:
        player (Player): The Player object.
        dt (float): Delta time for frame-independent calculation.
    """
    FACTOR = 30e-3
    EXPONENT = 1.4
    return ((FACTOR * (player.size ** EXPONENT))) * dt

def _check_obj_exists(list_objs:list, obj_idx:int) -> bool:
    """
    Helper for debug functions. Checks if the given obj_idx exists in the list_objs.
    
    Args:
        list_obj (list): The objects list.
        obj_idx (int): The given object index number.
    """
    return obj_idx >= 0 and obj_idx <= len(list_objs) - 1

def player_debug(players:list, player_n:int, screen:pygame.Surface, enable: bool) -> None:
    """
    Debug function for the Player class. Prints player attributes and draws debug circles on the screen.

    Args:
        players (list): The list of Player objects.
        player_n (int): The specific Player from the list.
        screen (pygame.Surface): The game screen.
        enable (bool): Flag to enable or disable debugging.
    """
    if enable:
        
        if not _check_obj_exists(players, player_n):
            raise ValueError(f"player_n {player_n} does not exist in players!")
        player = players[player_n]
        
        debug_string = (
            f"[PLAYER № {player_n} DEBUG] " 
            f"X: {player.position.x:.2f} "
            f"Y: {player.position.y:.2f} | "
            f"eat_tol: {player.eat_tol:.2f} | "
            f"hit_tol: {player.hit_tol:.2f} | "
            f"size: {player.size:.2f} | "
            f"speed: {player.speed:.2f} | "
            f"last_speed {player.last_speed:.2f} | "
            f"dash_on: {player.dash_on} | "
            f"dash_available: {player.dash_available}"
        )
        print(debug_string)
        
        # Player dots
        pygame.draw.circle(screen, "green", player.hit_pos, player.hit_tol) # Player hit range dot
        pygame.draw.circle(screen, "red", player.eat_pos, player.eat_tol) # Player eat range dot
        pygame.draw.circle(screen, "blue", player.position, 8) # Player position dot

def prey_debug(preys:list, prey_n:int, screen:pygame.Surface, enable: bool) -> None:
    """
    Debug function for the Prey class. Prints prey attributes and draws a debug dot on the screen.

    Args:
        preys (list): The list of Prey objects.
        prey_n (int): The specific Prey from the list.
        screen (pygame.Surface): The game screen.
        enable (bool): Flag to enable or disable debugging.
    """
    if enable:
        
        if not _check_obj_exists(preys, prey_n):
            raise ValueError(f"prey_n {prey_n} does not exist in preys!")
        prey = preys[prey_n]
        
        debug_string = (f"[PREY № {prey_n} DEBUG] "
                        f"X: {prey.position.x:.2f} "
                        f"Y: {prey.position.y:.2f} | " 
                        f"aura: {prey.aura} | "
                        f"eatable: {prey.eatable} | " 
                        f"counter: {prey.counter:.2f}"
        )
        print(debug_string)

        # Prey position dot
        pygame.draw.circle(screen, "blue", prey.position, 5)
        
def dagger_debug(daggers:list, dagger_n:int, screen:pygame.Surface, enable:bool) -> None:
    """
    Debug function for the Dagger class. Prints prey attributes and draws a debug dot on the screen.
    
    Args:
        daggers (list): The list of Dagger objects.
        dagger_n (int): The specific Dagger from the list.
        screen (pygame.Surface): The game screen.
        enable (bool): Flag to enable or disable debugging.
    """
    if enable:
        
        if not _check_obj_exists(daggers, dagger_n):
            raise ValueError(f"dagger_n {dagger_n} does not exist in daggers!")
        dagger = daggers[dagger_n]
        
        debug_string = (
            f"[DAGGER № {dagger_n} DEBUG] "
            f"X: {dagger.position.x:.2f} | "
            f"Y: {dagger.position.y:.2f} | "
            f"timer: {dagger.timer:.2f} | "
            f"spawn: {dagger.spawn_despawn[0]:.2f} | "
            f"despawn {dagger.spawn_despawn[1]:.2f} | "
            f"angle: {dagger.angle} | "
            f"speed_multiplier: {dagger.speed_multiplier:.2f} | "
            f"flame: {dagger.flame} | "
            f"played_sound: {dagger.played_sound}"
        )
        print(debug_string)
        
        # Dagger position dot
        pygame.draw.circle(screen, "red", dagger.position, 10)
        
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
            
def load_image(path: str) -> pygame.Surface:
    """
    Safely try to load an image with pygame.
    
    Args:
        path (str): The path to the image.
    """

    try:
        return pygame.image.load(resource_path(path)).convert_alpha()
    
    except FileNotFoundError:
        print(func_message("ERROR") + f"Image at '{path}' not found! Loading a placeholder.")
        return pygame.image.load(resource_path(add_placeholders(1, 'IMAGE')[0])).convert_alpha()
    
def load_sound(path: str) -> pygame.mixer.Sound:
    """
    Safely try to load a sound with pygame.
    
    Args:
        path (str): The path to the sound.
    """
    try:
        return pygame.mixer.Sound(resource_path(path))
    
    except FileNotFoundError:
        print(func_message("ERROR") + f"Sound at '{path}' not found! Loading a placeholder.")
        return pygame.mixer.Sound(resource_path(add_placeholders(1, 'SOUND')[0]))
    
def load_music(path: str) -> None:
    """
    Safely try to load a music with pygame.
    
    Args:
        path (str): The path to the music.
    """
    try:
        pygame.mixer.music.load(resource_path(path))
        
    except FileNotFoundError:
        print(func_message("ERROR") + f"Music at '{path}' not found! Loading a placeholder.")
        pygame.mixer.music.load((add_placeholders(1, 'SOUND')[0]))
            
def load_images(paths: tuple[str], count: int = None) -> tuple[pygame.Surface]:
    """
    Load pygame images from a list of paths. Optionally ensures a specific count of images.
    
    Args:
        paths (list[str]): The image file paths list.
        count (int): Optional expected image count. If actual count is lower, appends placeholder/s.
    """
    images = []
    actual_count = len(paths)
    
    # Load actual images
    images.extend(load_image(resource_path(path)) for path in paths)
    
    # Add placeholders if needed
    if count:
        
        if count > actual_count:
            print(func_message("WARN") + f"Image files count lower than expected! Adding {count - actual_count} placeholder/s.")
            # images.extend(load_image(path) for path in add_placeholders(count - actual_count, 'IMAGE')) # non recursive variant
            images.extend(load_images(add_placeholders(count - actual_count, 'IMAGE')))
            
        elif count < actual_count:
            print(func_message("WARN") + f"Image files count higher than expected: {actual_count} / {count}!")
    
    return tuple(images)
def load_sounds(paths: tuple[str], count: int = None) -> tuple[pygame.mixer.Sound]:
    """
    Load pygame sounds from a list of paths. Optionally ensures a specific count of sounds.
    
    Args:
        paths (list[str]): The sound file paths list.
        count (int): Optional expected sounds count. If actual count is lower, appends placeholder/s.
    """
    sounds = []
    actual_count = len(paths)
    
    # Load actual sounds
    sounds.extend(load_sound(resource_path(path)) for path in paths)
    
    # Add placeholders if needed
    if count:
        
        if count > actual_count:
            print(func_message("WARN") + f"Sound files count lower than expected! Adding {count - actual_count} placeholder/s.")
            # sounds.extend(load_sound(path) for path in add_placeholders(count - actual_count, 'SOUND')) # non recursive variant
            sounds.extend(load_sounds(add_placeholders(count - actual_count, 'SOUND')))
            
        elif count < actual_count:
            print(func_message("WARN") + f"Sound files count higher than expected: {actual_count} / {count}!")
    
    return tuple(sounds)

def traverse_folder(path: str) -> tuple:
    """
    Traverse through the given path to a folder. Returns a tuple in natural order with paths to all files. \n
    NOTE: Will return an empty tuple if no files are found!
    
    Args:
        path (str): The given folder's path.
    """
    def natural_sort_key(s: str) -> list:
        """Helper function to sort strings naturally (e.g., file_2 before file_10)."""
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]
    
    file_paths = []
    resolved_path = resource_path(path)
    
    if not os.path.exists(resolved_path):
        print(func_message("ERROR") + f"Path '{path}' does not exist!")
        return tuple()
    
    for root, dirs, files in os.walk(resolved_path):
        
        if len(dirs) > 0:
            print(func_message("WARN") + f"Path '{root}' has {len(dirs)} embedded folder/s!")
            
        if len(files) == 0:
            print(func_message("WARN") + f"Path '{root}' has no files!")
            
        for file in files:
            file_paths.append(os.path.join(root, file))
            
    return tuple(sorted(file_paths, key=natural_sort_key))
        
def load_playlist(paths: tuple[str], count: int = None) -> tuple[tuple[str, str]]:
    """
    Loads in a all files from the given paths argument and creates a tuple with tuples (name, file path). \n
    Optionally ensures a specific count of sounds.
        
    Args:
        paths (tuple[str]): The file paths.
        count (int): Optional expected sounds count. If actual count is lower, appends placeholder/s.
    """
    actual_count = len(paths)
    if actual_count == 0:
        print(func_message("ERROR") + f"The given paths argument is empty!")
    
    # Load playlist
    playlist = []
    for file_path in paths:
        pair = os.path.splitext(os.path.basename(file_path))[0], file_path
        playlist.append(pair)
        
    # Add placeholders if needed
    if count:
        if count > actual_count:
            print(func_message("WARN") + f"Sound files count lower than expected! Adding {count - actual_count} placeholder/s.")
            
            for _ in range(count - actual_count):
                placeholder_path = add_placeholders(1, 'SOUND')[0]  # Get the first placeholder path
                placeholder_name = os.path.splitext(os.path.basename(placeholder_path))[0]
                playlist.append((placeholder_name, placeholder_path))  # Append as a tuple (name, path)
        
        elif count < actual_count:
            print(func_message("WARN") + f"Sound files count higher than expected: {actual_count} / {count}!")
        
    return tuple(playlist)
    
