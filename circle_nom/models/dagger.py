from cycler import V
from circle_nom.systems.logging import get_logger
from random import randint, uniform, choice
from circle_nom.systems.timer import Timer
import pygame

class Dagger():
    
    # Internal consts
    _MARGIN = 100
    _BASE_SPEED = 700
    
    # Logger
    _LOGGER = get_logger(name=__name__)
    
    # Dagger spawn rate
    _SPAWN_RATE = 1
    
    def __init__(self, 
                 screen: pygame.Surface, game_timer: Timer,
                 dagger_images: list[pygame.Surface], 
                 dagger_sounds: list[pygame.Sound],
                 flame_sequence: list[pygame.Surface]) -> None:
        """
        Initialize a Dagger object with direction and other attributes.

        Args:
            screen (pygame.Surface): The game screen object reference.
            game_timer (Timer): The game timer. Used for different cooldowns.
            dagger_images (list[pygame.Surface]): List of dagger images.
            dagger_sounds (list[pygame.Sounds]): List of dagger sounds.
            flame_sequence (list[pygame.Surface]): Flame sequence animation.
        """
        # Objects from engine
        self._screen = screen
        self._game_timer = game_timer
        
        # Assets
        self._dagger_images = dagger_images
        self._dagger_sounds = dagger_sounds
        self._flame_sequence = flame_sequence
        
        # Set dagger attributes
        self.reset_dagger()
    
    @property
    def position(self) -> pygame.Vector2:
        """
        Returns the position coordinates of the dagger.

        Returns:
            Vector2: Vector2 type with the dagger's coordinates.
        """
        return self._position
    
    @property
    def flame(self) -> bool:
        """
        Return whether the dagger has a flame effect, based on the speed_multiplier.

        Returns:
            bool: True if the dagger has a flame effect, False otherwise.
        """
        return self._flame
    
    @property
    def played_sound(self) -> bool:
        """
        Return the played_sound flag. True if Dagger has played a sound, false otherwise.
        
        Returns:
            bool: The played_sound flag.
        """
        return self._played_sound
    
    @property
    def speed_multiplier(self) -> float:
        """
        Return the dagger's speed multiplier value.
        
        Returns:
            float: The speed_multiplier value.
        """
        return self._speed_multiplier
    
    @property
    def spawn_timestamp(self) -> float:
        """ 
        Return the spawn timestamp of the Dagger.
        
        Returns:
            float: spawn_timestamp attribute.
        """
        return self._spawn_timestamp
    
    @property
    def despawn_timestamp(self) -> float:
        """
        Returnm the despawn timestamp of the Dagger.
        
        Returns:
            float: despawn_timestamp attribute.
        """
        return self._despawn_timestamp
    
    @property
    def angle(self) -> int:
        """
        Return the dagger's angle.
        
        Returns:
            int: angle in degrees.
        """
        return self._angle
    
    @classmethod
    def set_spawnrate(cls, new_spawnrate: int | float) -> None:
        """
        Set the spawnrate of the Dagger. It's calculated with the formula: \n
        current time + random number from spawnrate to spawnrate * 2.
        
        Args:
            new_spawnrate (int|float): The new Dagger spawnrate.
        """
        if isinstance(new_spawnrate, (int, float)):
            cls._SPAWN_RATE = new_spawnrate
            cls._LOGGER.info(f"Dagger spawnrate value ({new_spawnrate:.2f}) applied.")
        else:
            raise ValueError("Classmethod 'set_spawnrate' accepts int/float only!")
        
    def _get_blit_pos(self, coords:pygame.Vector2, image: pygame.Surface) -> pygame.Vector2:
        """
        Internal helper for getting the center position for blit.
        """
        return coords - pygame.Vector2(image.width / 2, image.height / 2)
        
    def reset_dagger(self) -> None:
        """
        Resets the dagger's position, direction, and image.
        """
        self._position = pygame.Vector2(float('inf'), float('inf'))
        self._created = True

        # Decide dagger direction
        direction = randint(0, 3)

        # Up - Vertical
        if direction == 0:
            self._angle = 0
            self._position.x = uniform(self._MARGIN, self._screen.width - self._MARGIN)
            self._position.y = self._screen.height + self._MARGIN
            
        # Down - Vertical
        elif direction == 1:
            self._angle = 180
            self._position.x = uniform(self._MARGIN, self._screen.width - self._MARGIN)
            self._position.y = - self._MARGIN
            
        # Left - Horizontal
        elif direction == 2:
            self._angle = 90
            self._position.x = self._screen.width + self._MARGIN
            self._position.y = uniform(self._MARGIN, self._screen.height - self._MARGIN)
            
        # Right - Horizontal
        elif direction == 3:
            self._angle = 270
            self._position.x = - self._MARGIN
            self._position.y = uniform(self._MARGIN, self._screen.height - self._MARGIN)

        # Speed multiplier and flame based on it
        self._speed_multiplier = uniform(1, 1.8)
        self._flame = self._speed_multiplier >= 1.6
        
        # Spawn timestamp
        self._spawn_timestamp = self._game_timer.get_time() + uniform(self._SPAWN_RATE, self._SPAWN_RATE * 2)
        
        # Despawn timestamp - calculate based on the spawn time and decided dagger speed
        # Different numerator based on the dagger movement direction and screen size
        NUMERATOR = self._screen.width / 540 if direction in (2, 3) else self._screen.height / 450
        self._despawn_timestamp = self._spawn_timestamp + NUMERATOR / self._speed_multiplier
        
        # Choose dagger image from list and rotate
        self._image:pygame.Surface = pygame.transform.rotate(choice(self._dagger_images), self._angle)

        # Played sound flag
        self._played_sound = False
        
        # Log the dagger init
        log_str = (
            f"Dagger with spawn/despawn timestamps {self._spawn_timestamp:.2f}/{self._despawn_timestamp:.2f}s, "
            f"X {self._position.x:.2f} Y {self._position.y:.2f}, "
            f"speed multiplier {self._speed_multiplier:.2f} and angle {self._angle} initialized."
        )
        self._LOGGER.info(log_str)
        
    def grace_spawn(self, value: int|float) -> None:
        """
        Set grace spawn time (in seconds) for the next dagger.

        Args:
            value (int | float): The value to add to the spawn time.
        """
        if isinstance(value, (int, float)):
            self._spawn_timestamp += value
            self._despawn_timestamp += value
            self._LOGGER.info(f"Dagger grace spawn/despawn value ({value:.2f}) applied.")
        else:
            raise ValueError("Method 'grace_spawn' accepts int/float only!")
    
    def draw(self, dt: float) -> None:
        """
        Draw the dagger on the screen.
        
        Args:
            dt (float): Delta time, used for frame independent drawing.
        """
        
        # Reset dagger and cancel next frame calculations if its despawn time
        if self._game_timer.get_time() >= self._despawn_timestamp:
            self.reset_dagger()
            return
        
        # Calculate next frame position and draw if dagger is spawnewd
        if self._game_timer.get_time() >= self._spawn_timestamp:
            
            # Calculate delta movement
            delta_movement: dict[float, float] = { # type: ignore
                0:   (0, -self._BASE_SPEED * self._speed_multiplier * dt), # angle 0: up (x, y-)
                180: (0, +self._BASE_SPEED * self._speed_multiplier * dt), # angle 180: down (x, y+)
                90:  (-self._BASE_SPEED * self._speed_multiplier * dt, 0), # angle 90: left (x-, y)
                270: (+self._BASE_SPEED * self._speed_multiplier * dt, 0)  # angle 270: right (x+, y)
            }
            
            # Update position based on angle
            self._position.xy += delta_movement.get(self._angle) # type: ignore
            
            # Draw flame if its on
            if self._flame:
                
                # Select from flame_sequence and rotate
                flame_image = pygame.transform.rotate(self._flame_sequence[int(self._game_timer.get_time() / 0.12 % len(self._flame_sequence))], self._angle)
                self._screen.blit(flame_image, self._get_blit_pos(self._position, flame_image))
            
            # Draw dagger
            self._screen.blit(self._image, self._get_blit_pos(self._position, self._image))
        return
        
    def play_sound(self) -> None:
        """
        Play a random dagger sound if it hasn't been played yet.
        """
        if self._played_sound == False:
            choice(self._dagger_sounds).play()
            self._played_sound = True
            self._LOGGER.info(f"Started playing Dagger sound at X {self._position.x:.2f} Y {self._position.y:.2f}.")