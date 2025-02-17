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

def rot_center(image, angle, xy):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (xy)).center)

    return rotated_image, new_rect

def get_song_name(index:int, theme_songs:list) -> str:
    """
    Finds the song name using the given index.

    Args:
        index (int): The current index in theme_songs.
        theme_songs (list): Theme songs list. Used for error checking.

    Returns:
        str: Name of the song.
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
        raise ValueError(f"Lenght list_names: {len(list_names)} != Lenght theme_songs: {len(theme_songs)}")
    return list_names[index % len(list_names)]

def check_bounds(screen:pygame.Surface, player):
        """
        Function for checking if player is outside of playable area / screen bounds.
        """
        if player.position.x >= screen.get_width():
            player.position.x = screen.get_width() - 1

        if player.position.y >= screen.get_height(): 
            player.position.y = screen.get_height() - 1

        if player.position.x <= 0:
            player.position.x = 1

        if player.position.y <= 0:
            player.position.y = 1


def player_debug(player, screen:pygame.Surface, enable:bool):
    """
    Debug function for class Player. Prints on console X/Y, size, speed, eat / hit tolerance and their ranges on screen.
    """
    if enable:
        print(f"player X: {player.position.x:.2f} Y: {player.position.y:.2f}",end=" || ") 
        print(f"player eat_tol: {player.eat_tol:.2f}",end=" || ")
        print(f"player hit_tol: {player.hit_tol:.2f}",end=" || ")
        print(f"player size: {player.size:.2f}", end=" || ")
        print(f"player speed: {player.speed:.2f}")

        # Player dots
        pygame.draw.circle(screen, "green", player.hit_pos, player.hit_tol) # Player hit range dot
        pygame.draw.circle(screen, "red", player.eat_pos, player.eat_tol) # Player eat range dot

def prey_debug(prey, screen:pygame.Surface, enable:bool):
    """
    Debug function for class Prey. Prints on console X / Y with a dot on screen, prey counter and it's aura bool.
    """
    if enable:
        print(f"prey X: {prey.coords[0]} Y: {prey.coords[1]}",end=" | ")
        print(f"prey aura: {prey.aura}", end=" | ")
        print(f"prey counter: {prey.counter}")

        # Prey position dot
        pygame.draw.circle(screen, "blue", prey.coords, 5)

def player_control(player, dt:float, WASD:bool, ARROWS:bool):

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

    if WASD == False and ARROWS == False:
        raise ValueError("Enable either WASD or ARROWS controls in player_control function!")