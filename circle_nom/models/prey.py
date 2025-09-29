from circle_nom.helpers.other_utils import rot_center, rand_screen_pos
from circle_nom.systems.logging import get_logger
from circle_nom.systems.timer import Timer
from random import randint, uniform
import pygame

class Prey():
    
    # Prey animations config
    ANIM_DUR = 0.42             # Spawn/Despawn animation duration
    ANIM_ROT_SPEED = 640        # Spawn/Despawn animation rotation speed
    AURA_ROT_SPEED = 45         # Prey aura rotation speed
    AURA_MAX_SCALE = 180        # Maximum prey aura scale
    
    # Prey balancing
    SPAWNED_DUR = 2             # Time prey stays spawned before despawning
    NOSPAWN_DUR = 0.5           # Time prey is not spawning after despawn
    MAX_SIZE = 70               # Maximum prey size
    
    # Internal prey states
    _NOSPAWN = "NOSPAWN"        # Prey is currently not able to spawn
    _SPAWNING = "SPAWNING"      # Prey is currently in a spawning animation
    _SPAWNED = "SPAWNED"        # Prey is fully spawned and able to be eaten
    _DESPAWNING = "DESPAWNING"  # Prey is currently in a despawning animation
    
    # Logger reference
    _LOGGER = get_logger(name=__name__)

    def __init__(self, screen: pygame.Surface, game_timer: Timer,
                 list_images:list[pygame.Surface], aura_image:pygame.Surface) -> None:
        """
        Initializes the Prey object with images, aura image, and screen.

        Args:
            screen (pygame.Surface): The game screen. Used in the different draw methods.
            game_timer (Timer): The game timer. Used for different cooldowns.
            list_images (list[pygame.Surface]): List of prey images.
            aura_image (pygame.Surface): The aura image.
        """
        # Objects from the engine
        self._screen = screen
        self._game_timer = game_timer
        
        # Assets
        self._list_images = list_images
        self._aura_image = aura_image
        
        # Internal attributes
        self._aura_angle = 0
        self.reset_prey()

    @property
    def aura(self) -> bool:
        """
        Returns whether the prey has an aura effect.

        Returns:
            bool: True if the prey has an aura effect, False otherwise.
        """
        return self._aura_flag

    @property
    def position(self) -> pygame.Vector2:
        """
        Returns the position coordinates of the prey. If none returns Vector2('inf', 'inf').

        Returns:
            Vector2: The x and y coordinates.
        """
        return self._position if self._position else pygame.Vector2(float('inf'), float('inf'))

    @property
    def eatable(self) -> bool:
        """
        Returns the prey's eatable bool. True if prey is not in animation, false otherwise.
        
        Returns:
            bool: The eatable bool.
        """
        return self._eatable
    
    @property
    def last_state_change(self):
        """
        Get the internal timestamp of the prey's last state change.
        
        Returns:
            float: The last_state_change timestamp value.
        """
        return self._last_state_change
    
    @property
    def state(self) -> str:
        """
        Get the current prey state.
        
        Returns:
            str: The prey state.
        """
        return self._state
    
    @state.setter
    def state(self, new_state: str) -> None:
        """
        Set the prey's state. Updates the last_state_change timestamp value if the new state is different from the old one.
        
        Args:
            new_state (str): The new state value. Can be one of: ["NOSPAWN", "SPAWNING", "SPAWNED", "DESPAWNED"].
        """
        # if new_state not in {Prey._NOSPAWN, Prey._SPAWNING, Prey._SPAWNED, Prey._DESPAWNING}:
        #     raise ValueError("State setter received invalid value.")
        
        if new_state != self._state:
            self._state = new_state
            self._last_state_change = self._game_timer.get_time()
            
    @classmethod
    def set_spawned_duration(cls, new_duration: int | float) -> None:
        """
        Set the duration the prey stays spawned in seconds.
        Args:
            new_duration (int | float): The new spawn duration.
        """
        cls.SPAWNED_DUR = new_duration
        
    @classmethod
    def set_no_spawn_duration(cls, new_duration: int | float) -> None:
        """
        Set the duration before a new pray can be spawned after despawning.
        Args:
            new_duration (int | float): The new nospawn duration.
        """
        cls.NOSPAWN_DUR = new_duration
        
    def _animate(self, progress: float, reverse: bool, dt: float) -> None:
        """
        Handles the animation of the prey (scaling and rotation) for spawn and despawn.
        Args:
            progress (float): 0.0 to 1.0 progress through the animation.
            reverse (bool): Whether the animation is in reverse (despawn).
            dt (float): Delta time for frame-rate independent rotation.
        """
        # Calculate scale and rotation direction
        scale_vect = progress
        rotation_vect = 1
        if reverse:
            scale_vect = 1 - scale_vect
            rotation_vect = -1
            
        # Scale prey from 0 to 70 pixels
        self._scale = (Prey.MAX_SIZE + self._size_deviance)* scale_vect
        
        # Calculate prey angle
        self._prey_angle = (self._prey_angle % 360) - Prey.ANIM_ROT_SPEED * rotation_vect * dt
        
        # Animate prey aura if present
        if self._aura_flag:
            
            # Calculate aura scale based on the prey scale vect
            aura_scale = Prey.AURA_MAX_SCALE * scale_vect
            aura = pygame.transform.smoothscale(self._aura_image, (aura_scale, aura_scale))
            
            # Calculate aura rotation angle
            self._aura_angle = (self._aura_angle % 360) - Prey.AURA_ROT_SPEED * dt
            
            # Rotate aura based on the calculated angle and draw
            rotated_aura = rot_center(aura, self._aura_angle, self._position)
            self._screen.blit(rotated_aura[0], rotated_aura[1])
            
        # Lastly draw the rotated prey
        prey = pygame.transform.smoothscale(self._image, (self._scale, self._scale))
        rotated_prey = rot_center(prey, self._prey_angle, self._position)
        self._screen.blit(rotated_prey[0], rotated_prey[1])

    def _draw_normal(self, dt: float) -> None:
        """
        Draws the prey and its aura (if present) in the normal (alive) state.
        Args:
            dt (float): Delta time for frame-rate independent rotation.
        """
        # Rotate and draw aura if present
        if self._aura_flag:
            self._aura_angle = (self._aura_angle % 360) - Prey.AURA_ROT_SPEED * dt
            rotated_aura = rot_center(self._aura_image, self._aura_angle, self._position)
            self._screen.blit(rotated_aura[0], rotated_aura[1])
            
        # Draw prey
        prey = pygame.transform.smoothscale(self._image, (Prey.MAX_SIZE + self._size_deviance, Prey.MAX_SIZE + self._size_deviance))
        rotated_prey = rot_center(prey, self._prey_angle, self._position)
        self._screen.blit(rotated_prey[0], rotated_prey[1])

    def draw(self, dt: float) -> None:
        """
        Draws the prey on the screen, handling state transitions and animation using delta time (dt).
        
        Args:
            dt (float): Delta time in seconds since the last frame. Ensures frame-rate independent animation.
        """
        # Get current time and elapsed time in the current Prey state
        now = self._game_timer.get_time()
        elapsed = now - self._last_state_change
        
        # No spawn state
        if self.state == Prey._NOSPAWN:
            
            # If elapsed time has not reached the end of nospawn duration do nothing
            if elapsed < Prey.NOSPAWN_DUR: return
            
            # If it has, transition prey to spawning
            else: 
                self.state = Prey._SPAWNING
                
                # Log the change
                log_str = (
                    f"Prey at time {self._game_timer.get_time():.2f}s, "
                    f"X {self._position.x:.2f} Y {self._position.y:.2f} "
                    f"changed state to {self._state}."
                )
                self._LOGGER.info(log_str)

        # Spawning state
        elif self._state == Prey._SPAWNING:
            
            # If elapsed time has not reached the end of the spawn anim dur -
            # animate spawn (scale up and rotate clockwise)
            if elapsed < Prey.ANIM_DUR:
                progress = elapsed / Prey.ANIM_DUR
                self._animate(progress, reverse=False, dt=dt)
                
            # If it has, transition prey to spawned state
            else:
                self.state = Prey._SPAWNED
                
                # Set the prey to be eatable and fix it to it's max size
                self._eatable = True
                self._scale = Prey.MAX_SIZE + self._size_deviance
                
                # Call draw normal method here to avoid flicker - 
                # otherwise a draw method will be skipped in this call
                self._draw_normal(dt=dt)
                
                # Log the change
                log_str = (
                    f"Prey at time {self._game_timer.get_time():.2f}s, "
                    f"X {self._position.x:.2f} Y {self._position.y:.2f} "
                    f"changed state to {self._state}."
                )
                self._LOGGER.info(log_str)
        
        # Spawned state
        elif self.state == Prey._SPAWNED:
            
            # If elapsed time is smaller than the alive duration draw prey
            if elapsed <= Prey.SPAWNED_DUR:
                self._draw_normal(dt=dt)
            
            # If its not, set new prey state to despawning
            else:
                self.state = Prey._DESPAWNING
                self._eatable = False
                
                # Call draw normal method here to avoid flicker - 
                # otherwise a draw method will be skipped in this call
                self._draw_normal(dt=dt)
                
                # Log the change
                log_str = (
                    f"Prey at time {self._game_timer.get_time():.2f}s, "
                    f"X {self._position.x:.2f} Y {self._position.y:.2f} "
                    f"changed state to {self._state}."
                )
                self._LOGGER.info(log_str)
                
        # Despawning state
        elif self.state == Prey._DESPAWNING:
            
            # If elapsed time has not reached the end of despawn anim dur -
            # animate despawn (scale down and rotate counterclockwise)
            if elapsed < Prey.ANIM_DUR:
                progress = elapsed / Prey.ANIM_DUR
                self._animate(progress, reverse=True, dt=dt)
            
            # If it has, reset the prey for next cycle
            else: self.reset_prey()
            
    def reset_prey(self) -> None:
        # Choose a new prey image and aura it if it's the first file (a sandwich)
        self._image_index = randint(0, len(self._list_images) - 1)
        self._image = self._list_images[self._image_index]
        self._aura_flag = (self._image_index == 0)
        
        # Get a new random angle, screen position and size deviance
        self._prey_angle = uniform(0, 360)
        self._position = rand_screen_pos(self._screen)
        self._size_deviance = uniform(-10, 10)
        
        # Initial NOSPAWN Prey attributes
        self._state = Prey._NOSPAWN
        self._last_state_change = self._game_timer.get_time()
        self._eatable = False
        self._scale = 0
        
        # Log the Prey init
        log_str = (
            f"Prey at time {self._game_timer.get_time():.2f}s, "
            f"X {self._position.x:.2f} Y {self._position.y:.2f}, "
            f"with state {self.state} initialized."
        )
        self._LOGGER.info(log_str) 
