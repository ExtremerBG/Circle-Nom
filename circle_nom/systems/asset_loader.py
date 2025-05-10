from .logging import console_message
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
        console_message("ERROR", f"Path '{path}' does not exist!")
        return tuple()
    
    for root, dirs, files in os.walk(resolved_path):
        
        if len(dirs) > 0:
            console_message("WARN", f"Path '{root}' has {len(dirs)} embedded folder/s!")
            
        if len(files) == 0:
            console_message("WARN", f"Path '{root}' has no files!")
            
        for file in files:
            file_paths.append(os.path.join(root, file))
            
    return tuple(sorted(file_paths, key=natural_sort_key))

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
    "IMAGE": 'assets/images/error/missing_image.png',
    "SOUND": 'assets/sounds/error/missing_sound.mp3'
    }
    
    if key not in MISSING_RESOURCES.keys():
        raise ValueError(console_message('ERROR', f"Invalid key '{key}'! Must be 'IMAGE' or 'SOUND'."))
    if num < 0:
        raise ValueError(console_message('ERROR' , "Invalid number of placeholders."))
    
    resolved_path = resource_path(MISSING_RESOURCES[key])
    
    if not os.path.exists(resolved_path):
        raise ValueError(console_message('ERROR' , f"Path '{resolved_path}' not found!"))
    
    return [resolved_path for _ in range(num)]

def load_image(path: str) -> pygame.Surface:
    """
    Safely try to load an image with pygame.
    
    Args:
        path (str): The path to the image.
    """

    try:
        return pygame.image.load(resource_path(path)).convert_alpha()
    
    except FileNotFoundError:
        console_message("ERROR" , f"Image at '{path}' not found! Loading a placeholder.")
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
        console_message("ERROR" , f"Sound at '{path}' not found! Loading a placeholder.")
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
        console_message("ERROR" , f"Music at '{path}' not found! Loading a placeholder.")
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
            console_message("WARN",  f"Image files count lower than expected! Adding {count - actual_count} placeholder/s.")
            # images.extend(load_image(path) for path in add_placeholders(count - actual_count, 'IMAGE')) # non recursive variant
            images.extend(load_images(add_placeholders(count - actual_count, 'IMAGE')))
            
        elif count < actual_count:
            console_message("WARN", f"Image files count higher than expected: {actual_count} / {count}!")
    
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
            console_message("WARN" + f"Sound files count lower than expected! Adding {count - actual_count} placeholder/s.")
            # sounds.extend(load_sound(path) for path in add_placeholders(count - actual_count, 'SOUND')) # non recursive variant
            sounds.extend(load_sounds(add_placeholders(count - actual_count, 'SOUND')))
            
        elif count < actual_count:
            console_message("WARN", f"Sound files count higher than expected: {actual_count} / {count}!")
    
    return tuple(sounds)

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
        console_message("ERROR", f"The given paths argument is empty!")
    
    # Load playlist
    playlist = []
    for file_path in paths:
        pair = os.path.splitext(os.path.basename(file_path))[0], file_path
        playlist.append(pair)
        
    # Add placeholders if needed
    if count:
        if count > actual_count:
            console_message("WARN", f"Sound files count lower than expected! Adding {count - actual_count} placeholder/s.")
            
            for _ in range(count - actual_count):
                placeholder_path = add_placeholders(1, 'SOUND')[0]  # Get the first placeholder path
                placeholder_name = os.path.splitext(os.path.basename(placeholder_path))[0]
                playlist.append((placeholder_name, placeholder_path))  # Append as a tuple (name, path)
        
        elif count < actual_count:
            console_message("WARN", f"Sound files count higher than expected: {actual_count} / {count}!")
        
    return tuple(playlist)