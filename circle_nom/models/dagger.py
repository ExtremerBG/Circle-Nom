from random import randint, uniform, choice
import pygame

class Dagger():
    
    def __init__(self, dagger_images: list[pygame.Surface], dagger_sounds: list[pygame.Sound], flame_sequence: list[pygame.Surface],  screen: pygame.Surface):
        """
        Initialize a Dagger object with direction and other attributes.

        Args:
            list_daggers (list[pygame.Surface]): List of dagger images.
            screen (pygame.Surface): The game screen.
        """
        self._screen = screen

        self._dagger_images = dagger_images
        self._flame_sequence = flame_sequence
        self._dagger_sounds = dagger_sounds
        self._angle = None
        self._played_sound = None
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
    def timer(self) -> float:
        """ 
        Return the timer of the dagger.
        
        Returns:
            float: Dagger timer.
        """
        return self._timer
    
    @property
    def spawn_despawn(self) -> tuple:
        """ 
        Return the spawn and despawn numbers.
        
        Returns:
            tuple: spawn, despawn.
        """
        return self._spawn, self._despawn
    
    @property
    def angle(self) -> int:
        """
        Return the dagger's angle.
        
        Returns:
            int: angle in degrees.
        """
        return self._angle
        
    def _get_blit_pos(self, coords:pygame.Vector2, image: pygame.Surface):
        """
        Internal helper for getting the center position for blit.
        """
        return coords - pygame.Vector2(image.get_width() / 2, image.get_height() / 2)
        
    def reset_dagger(self):
        """
        Resets the dagger's position, direction, and image.
        """
        self._position = pygame.Vector2(float('inf'), float('inf'))
        self._created = True

        # Dagger direction
        direction = randint(0, 3)

        # Up
        if direction == 0:
            self._angle = 0
            self._position.x = uniform(100, 1180)
            self._position.y = self._screen.get_height() + 100 # margin
            
        # Down
        elif direction == 1:
            self._angle = 180
            self._position.x = uniform(100, 1180)
            self._position.y = -100 # margin
            
        # Left
        elif direction == 2:
            self._angle = 90
            self._position.x = self._screen.get_width() + 100 # margin
            self._position.y = uniform(100, 620)
            
        # Right
        elif direction == 3:
            self._angle = 270
            self._position.x = -100 # margin
            self._position.y = uniform(100, 620)

        # Speed multiplier and flame based on it
        self._speed_multiplier = uniform(1, 2)
        self._flame = self._speed_multiplier >= 1.6
        
        # Choose dagger image from list and rotate
        self._image:pygame.Surface = pygame.transform.rotate(choice(self._dagger_images), self._angle)
        
        # Spawn time
        self._spawn = randint(20, 40)

        # Despawn time
        self._despawn = (240 + self._spawn) / self._speed_multiplier

        # Timer for spawn/despawn
        self._timer = 0

        # Played sound flag
        self._played_sound = False  
        
    def grace_spawn(self, value: int|float):
        """
        Set grace spawn time for the next dagger.

        Args:
            value (int | float): The value to add to the spawn time.
        """
        if isinstance(value, (int, float)):
            self._spawn += value
            self._despawn = (240 + self._spawn) / self._speed_multiplier # update despawn
        else:
            raise ValueError("Method grace_spawn accepts int/float only!")
    
    def draw(self, dt:float):
        """
        Draw the dagger on the screen.
        
        Args:
            dt (float): Delta time, used for frame independent drawing.
        """
        # Increment position
        if self._timer > self._spawn:
            
            # Calculate delta movement
            delta_movement: dict[float, float] = {
                0: (0, -600 * self._speed_multiplier * dt), # angle 0: up (x, y-)
                180: (0, +600 * self._speed_multiplier * dt), # angle 180: down (x, y+)
                90: (-600 * self._speed_multiplier * dt, 0), # angle 90: left (x-, y)
                270: (+600 * self._speed_multiplier * dt, 0) # angle 270: right (x+, y)
            }
            
            # Update position based on angle
            self._position.xy += delta_movement.get(self._angle)

        # Reset dagger and cancel next frame draw
        if self._timer > self._despawn:
            self.reset_dagger()
            return

        # Draw
        if self._timer > self._spawn:
            
            # Draw flame
            if self._flame:
                # Select from flame_sequence and rotate
                flame_image = pygame.transform.rotate(self._flame_sequence[int(self._timer / 6 % len(self._flame_sequence))], self._angle)
                self._screen.blit(flame_image, self._get_blit_pos(self._position, flame_image))
            
            # Draw dagger
            self._screen.blit(self._image, self._get_blit_pos(self._position, self._image))

        # Increment timer
        self._timer += 60 * dt

    def play_sound(self):
        """
        Play a random dagger sound if it hasn't been played yet.
        """
        if self._played_sound == False:
            choice(self._dagger_sounds).play()
            self._played_sound = True