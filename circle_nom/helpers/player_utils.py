from math import isclose
import pygame

def player_movement_rate(player, dt:float) -> float:
    """
    Get player movement rate number from formula.
    
    Args:
        player (Player): The Player object.
        dt (float): Delta time for frame-independent calculation.
        
    Returns:
        float: Number used to influence the speed of the given player.
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
        
    Returns:
        float: Number used to reduce the size of the given player.
    """
    FACTOR = 30e-3
    EXPONENT = 1.4
    return ((FACTOR * (player.size ** EXPONENT))) * dt

def player_dash_speed_increase(player) -> float:
    """
    Get the player speed increase number from formula.
    
    Args:
        player (Player): The Player object.
        
    Returns:
        float: Number used to add to the speed of the given player.
    """
    FACTOR = 100
    EXPONENT = 1.4
    return ((FACTOR / (player.size ** EXPONENT)) * player.size)

def player_check_bounds(screen: pygame.Surface, player) -> None:
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
        
def player_check_collision(player_1, player_2, dt: float) -> None:
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
        
def player_control(player, dt: float, arrows: bool, wasd: bool) -> None:
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