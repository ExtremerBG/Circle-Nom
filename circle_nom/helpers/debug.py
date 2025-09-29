from circle_nom.helpers.config_reader import ConfigReader
from circle_nom.systems.logging import get_logger
from circle_nom.models.player import Player
from circle_nom.models.dagger import Dagger
from circle_nom.models.prey import Prey
from typing import Any
import pygame

logger = get_logger(name=__name__)
ENABLE_PLAYER, ENABLE_PREY, ENABLE_DAGGER = ConfigReader().get_debug()

def _check_obj_exists(tuple_objs: tuple[Any, ...], obj_idx:int) -> bool:
    """
    Helper for debug functions. Checks if the given obj_idx exists in the tuple_objs.
    
    Args:
        tuple_objs (tuple): The objects tuple.
        obj_idx (int): The given object index number.
    """
    return obj_idx >= 0 and obj_idx <= len(tuple_objs) - 1

def player(players: tuple[Player, ...], player_n: int, screen: pygame.Surface) -> None:
    """
    Debug function for the Player class. Prints player attributes and draws debug circles on the screen.

    Args:
        players (tuple): The tuple of Player objects.
        player_n (int): The specific Player from the tuple.
        screen (pygame.Surface): The game screen.
    """
    if ENABLE_PLAYER:
        
        if not _check_obj_exists(players, player_n):
            raise ValueError(f"player_n {player_n} does not exist in players!")
        player = players[player_n]
        
        debug_string = (
            f"PLAYER № {player_n} | "
            f"X: {player.position.x:.2f} "
            f"Y: {player.position.y:.2f} | "
            f"eat_tol: {player.eat_tol:.2f} | "
            f"hit_tol: {player.hit_tol:.2f} | "
            f"size: {player.size:.2f} | "
            f"speed: {player.speed:.2f} | "
            f"speed_before_dash: {player.speed_before_dash:.2f} | "
            f"dash_available: {player.dash_available} | "
            f"last_dash_timestamp: {player._last_dash_timestamp:.2f} | "
            f"can_eat: {player.can_eat}"
        )
        print(debug_string)
        # logger.debug(msg=debug_string)
        
        # Player dots
        pygame.draw.circle(screen, "green", player.hit_pos, player.hit_tol) # Player hit range dot
        pygame.draw.circle(screen, "red", player.eat_pos, player.eat_tol)   # Player eat range dot
        pygame.draw.circle(screen, "blue", player.position, 8)              # Player position dot

def prey(preys: tuple[Prey], prey_n: int, screen: pygame.Surface) -> None:
    """
    Debug function for the Prey class. Prints prey attributes and draws a debug dot on the screen.

    Args:
        preys (tuple): The tuple of Prey objects.
        prey_n (int): The specific Prey from the tuple.
        screen (pygame.Surface): The game screen.
    """
    if ENABLE_PREY:
        
        if not _check_obj_exists(preys, prey_n):
            raise ValueError(f"prey_n {prey_n} does not exist in preys!")
        prey = preys[prey_n]
        
        debug_string = (
            f"PREY № {prey_n} | "
            f"X: {prey.position.x:.2f} "
            f"Y: {prey.position.y:.2f} | "
            f"state: {prey._state} | " 
            f"last_state_change: {prey.last_state_change:.2f} | "
            f"eatable: {prey.eatable} | "
            f"aura: {prey.aura}"
        )
        print(debug_string)
        # logger.debug(msg=debug_string)

        # Prey position dot
        pygame.draw.circle(screen, "blue", prey.position, 5)
        
def dagger(daggers: tuple[Dagger], dagger_n: int, screen: pygame.Surface) -> None:
    """
    Debug function for the Dagger class. Prints prey attributes and draws a debug dot on the screen.
    
    Args:
        daggers (tuple): The tuple of Dagger objects.
        dagger_n (int): The specific Dagger from the tuple.
        screen (pygame.Surface): The game screen.
        enable (bool): Flag to enable or disable debugging.
    """
    if ENABLE_DAGGER:
        
        if not _check_obj_exists(daggers, dagger_n):
            raise ValueError(f"dagger_n {dagger_n} does not exist in daggers!")
        dagger = daggers[dagger_n]
        
        debug_string = (
            f"DAGGER № {dagger_n} | "
            f"X: {dagger.position.x:.2f} "
            f"Y: {dagger.position.y:.2f} | "
            f"spawn: {dagger.spawn_timestamp:.2f} | "
            f"despawn {dagger.despawn_timestamp:.2f} | "
            f"angle: {dagger.angle} | "
            f"speed_multiplier: {dagger.speed_multiplier:.2f} | "
            f"flame: {dagger.flame} | "
            f"played_sound: {dagger.played_sound}"
        )
        print(debug_string)
        # logger.debug(msg=debug_string)
        
        # Dagger position dot
        pygame.draw.circle(screen, "red", dagger.position, 10)