from typing import Callable
from random import uniform
from math import isclose
import gif_pygame
import pygame
import sys
import os

pygame.mixer.init()

def resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a resource, works for PyInstaller.

    Args:
        relative_path (str): The relative path to the resource.

    Returns:
        str: The absolute path to the resource.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def rand_screen_pos() -> pygame.Vector2:
    """
    Generate a random position on the screen with a bias towards certain areas.

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

def get_song_name(index: int, theme_songs: list) -> str:
    """
    Get the song name from the list of theme songs using the given index.

    Args:
        index (int): The current index in theme_songs.
        theme_songs (list): List of theme songs.

    Returns:
        str: The name of the song.
    """
    list_names = [
        "Cowboy Bebop - Tank", #1
        "Smash Ultimate - Chemical Plant Zone", #2
        "Hideki Naganuma - Sneakman", #3
        "Persona 5 - Last Surprise ", #4
        "Persona 5 - Wake Up, Get up, Get Out There", #5
        "Samba de Amigo - Samba de Janeiro", #6
        "Sonic Mania - Theme of the Hard-Boiled Heavies", #7
        "Mario Kart DS - Waluigi Pinball & Wario Stadium", #8
        "Mortal Kombat - Techno Syndrome", #9
        "Undertale - Hopes and Dreams", #10
        "Persona 4 - Specialist", #11
        "Mario Paint - Creative Exercise", #12
        "Mt.dede - Kirby Superstar Theme", #13
        "Yakuza - Friday Night", #14
        "Skeleton Boomerang - Disco Necropolis" #15
    ]
    if len(list_names) != len(theme_songs):
        raise ValueError(f"Length list_names: {len(list_names)} != Length theme_songs: {len(theme_songs)}")
    return list_names[index % len(list_names)]

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

def check_player_collision(player_1, player_2) -> None:
    """
    Check if player_1 collides with player_2 and adjust positions if necessary.

    Args:
        player_1: The first player object with position and collision tolerance attributes.
        player_2: The second player object with position and collision tolerance attributes.
    """
    # Check if player_1 is close enough to player_2
    if isclose(player_1.position.x, player_2.position.x, abs_tol=player_1.collision_tol) \
        and isclose(player_1.position.y, player_2.position.y, abs_tol=player_1.collision_tol):
        
        # If player_1 is to the right of player_2, move them apart horizontally
        if player_1.position.x > player_2.position.x:
            player_1.position.x += 1
            player_2.position.x -= 1
        else:
            player_1.position.x -= 1
            player_2.position.x += 1

        # If player_1 is below player_2, move them apart vertically
        if player_1.position.y > player_2.position.y:
            player_1.position.y += 1
            player_2.position.y -= 1
        else:
            player_1.position.y -= 1
            player_2.position.y += 1

    # Check if player_2 is close enough to player_1
    if isclose(player_2.position.x, player_1.position.x, abs_tol=player_2.collision_tol) \
        and isclose(player_2.position.y, player_1.position.y, abs_tol=player_2.collision_tol):

        # If player_2 is to the right of player_1, move them apart horizontally
        if player_2.position.x > player_1.position.x:
            player_2.position.x += 1
            player_1.position.x -= 1
        else:
            player_2.position.x -= 1
            player_1.position.x += 1

        # If player_2 is below player_1, move them apart vertically
        if player_2.position.y > player_1.position.y:
            player_2.position.y += 1
            player_1.position.y -= 1
        else:
            player_2.position.y -= 1
            player_1.position.y += 1
            
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
    coords = 1215, 695
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
        # Select prey from list
        prey = preys[prey_n]
        debug_string = (f"[PREY № {prey_n} DEBUG] "
                        f"X: {prey.coords.x:.2f} "
                        f"Y: {prey.coords.y:.2f} | " 
                        f"aura: {prey.aura} | "
                        f"eatable: {prey.eatable} | " 
                        f"counter: {prey.counter:.2f}"
        )
        print(debug_string)

        # Prey position dot
        pygame.draw.circle(screen, "blue", prey.coords, 5)
        
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
        # Select dagger from list
        dagger = daggers[dagger_n]
        debug_string = (
            f"[DAGGER № {dagger_n} DEBUG] "
            f"X: {dagger.coords.x:.2f} | "
            f"Y: {dagger.coords.y:.2f} | "
            f"timer: {dagger.timer:.2f} | "
            f"spawn: {dagger.spawn_despawn[0]:.2f} | "
            f"despawn {dagger.spawn_despawn[1]:.2f} | "
            f"direction: {dagger.get_dir} | "
            f"speed_multiplier: {dagger.speed_multiplier:.2f} | "
            f"flame: {dagger.flame} | "
            f"played_sound: {dagger.played_sound}"
        )
        print(debug_string)
        
        # Dagger position dot
        pygame.draw.circle(screen, "red", dagger.coords, 10)
        
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

def draw_rects(screen:pygame.Surface, rects:tuple[pygame.Rect], enable:bool) -> None:
    """
    Function for drawing semi transparent rects onto the screen.
    
    Args:
        screen (pygame.Surface): The game screen.
        rects tuple[pygame.Rect]: The rectangles to draw.
        enable (bool): Whether to enable the drawing.
    """
    if enable:
        for rect in rects:
            transparent_surface = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
            transparent_surface.fill((0, 255, 0, 64))
            screen.blit(transparent_surface, (rect[0], rect[1]))
            
def safe_load_image(path: str) -> pygame.Surface | gif_pygame.GIFPygame:
    """
    Safely try to load an image with pygame or gif_pygame.
    """
    MISSING_IMAGE_PATH = 'image/error/missing_image.png'
    try:
        if path.endswith(('.gif', '.apng')):
            return gif_pygame.load(resource_path(path))
        else:
            return pygame.image.load(resource_path(path))
    except FileNotFoundError:
        print(f"[ERROR]: image at '{path}' not found!")
        if path.endswith(('.gif', '.apng')):
            return gif_pygame.load(resource_path(MISSING_IMAGE_PATH))
        else:
            return pygame.image.load(resource_path(MISSING_IMAGE_PATH))
    
def safe_load_sound(path: str) -> pygame.mixer.Sound:
    """
    Safely try to load a sound with pygame.
    """
    MISSING_SOUND_PATH = 'sound/error/missing_sound.mp3'
    try:
        return pygame.mixer.Sound(resource_path(path))
    except FileNotFoundError:
        print(f"[ERROR]: sound at '{path}' not found!")
        return pygame.mixer.Sound(resource_path(MISSING_SOUND_PATH))
    
def safe_load_music(path: str) -> pygame.mixer.music:
    """
    Safely try to load a music with pygame.
    """
    MISSING_SOUND_PATH = 'sound/error/missing_sound.mp3'
    try:
        return pygame.mixer.music.load(resource_path(path))
    except FileNotFoundError as e:
        print(f"[ERROR]: music at '{path}' not found!")
        return pygame.mixer.music.load((resource_path(MISSING_SOUND_PATH)))
            
def load_images(paths: list[str]) -> tuple[pygame.Surface|gif_pygame.GIFPygame]:
    """
    Load pygame images from list of paths. Returns tuple with loaded images.
    
    Args:
        paths (list[str]): The file paths list.
    """
    return tuple(safe_load_image(resource_path(path)) for path in paths)

def load_sounds(paths: list[str]) -> tuple[pygame.mixer.Sound]:
    """
    Load pygame sounds from list of paths. Returns tuple with loaded sounds.
    
    Args:
        paths (list[str]): The file paths list.
    """
    return tuple(safe_load_sound(resource_path(path)) for path in paths)
