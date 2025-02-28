from random import randint
from math import isclose
import pygame
import sys
import os

def resource_path(relative_path):
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

def rand_screen_pos():
    """
    Generate a random position on the screen with a bias towards certain areas.

    Returns:
        tuple: A tuple containing the x and y coordinates of the random position.
    """
    bias_edge = randint(0, 100)

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

def rot_center(image: pygame.Surface, angle: int | float, xy):
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

def check_screen_bounds(screen: pygame.Surface, player):
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

def check_player_collision(player_1, player_2):
    """
    Check if player_1 collides with player_2 and adjust positions if necessary.

    Args:
        player_1: The first player object with position and collision tolerance attributes.
        player_2: The second player object with position and collision tolerance attributes.
    """
    # Check if player_1 is close enough to player_2
    if isclose(player_1.position.x, player_2.position.x, abs_tol=player_1.collision_tol) and isclose(player_1.position.y, player_2.position.y, abs_tol=player_1.collision_tol):
        
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
    if isclose(player_2.position.x, player_1.position.x, abs_tol=player_2.collision_tol) and isclose(player_2.position.y, player_1.position.y, abs_tol=player_2.collision_tol):

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

def player_debug(player, screen: pygame.Surface, enable: bool):
    """
    Debug function for the Player class. Prints player attributes and draws debug circles on the screen.

    Args:
        player: The player object with position, size, speed, eat_tol, and hit_tol attributes.
        screen (pygame.Surface): The game screen.
        enable (bool): Flag to enable or disable debugging.
    """
    if enable:
        print(f"player X: {player.position.x:.2f} Y: {player.position.y:.2f}", end=" || ") 
        print(f"player eat_tol: {player.eat_tol:.2f}", end=" || ")
        print(f"player hit_tol: {player.hit_tol:.2f}", end=" || ")
        print(f"player size: {player.size:.2f}", end=" || ")
        print(f"player speed: {player.speed:.2f}")

        # Player dots
        pygame.draw.circle(screen, "green", player.hit_pos, player.hit_tol) # Player hit range dot
        pygame.draw.circle(screen, "red", player.eat_pos, player.eat_tol) # Player eat range dot

def prey_debug(prey, screen: pygame.Surface, enable: bool):
    """
    Debug function for the Prey class. Prints prey attributes and draws a debug dot on the screen.

    Args:
        prey: The prey object with coords, aura, and counter attributes.
        screen (pygame.Surface): The game screen.
        enable (bool): Flag to enable or disable debugging.
    """
    if enable:
        print(f"prey X: {prey.coords[0]} Y: {prey.coords[1]}", end=" | ")
        print(f"prey aura: {prey.aura}", end=" | ")
        print(f"prey counter: {prey.counter}")

        # Prey position dot
        pygame.draw.circle(screen, "blue", prey.coords, 5)

def player_control(player, dt: float, WASD: bool, ARROWS: bool):
    """
    Control the player movement based on keyboard input.

    Args:
        player: The player object with position, size, and speed attributes.
        dt (float): Delta time from the game clock.
        WASD (bool): Flag to enable WASD controls.
        ARROWS (bool): Flag to enable arrow key controls.

    Raises:
        ValueError: If both WASD and ARROWS are disabled.
    """
    keys = pygame.key.get_pressed()
    if WASD:
        if keys[pygame.K_w]:
            player.position.y -= ((3300 / player.size) * player.speed) * dt

        if keys[pygame.K_s]:
            player.position.y += ((3300 / player.size) * player.speed) * dt

        if keys[pygame.K_a]:
            player.position.x -= ((3300 / player.size) * player.speed) * dt

        if keys[pygame.K_d]:
            player.position.x += ((3300 / player.size) * player.speed) * dt

    if ARROWS:
        if keys[pygame.K_UP]:
            player.position.y -= ((3300 / player.size) * player.speed) * dt

        if keys[pygame.K_DOWN]:
            player.position.y += ((3300 / player.size) * player.speed) * dt

        if keys[pygame.K_LEFT]:
            player.position.x -= ((3300 / player.size) * player.speed) * dt

        if keys[pygame.K_RIGHT]:
            player.position.x += ((3300 / player.size) * player.speed) * dt

    if not WASD and not ARROWS:
        raise ValueError("Enable either WASD or ARROWS controls in player_control function!")