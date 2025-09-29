from circle_nom.systems.logging import get_logger
import math

class Oscillator:
    
    # Logger reference
    _LOGGER = get_logger(name=__name__)
    
    # Oscillator wave types
    _WAVE_TYPES = "sine", "triangle", "square", "sawtooth"
    
    def __init__(self, a_min: int|float, a_max: int|float, period: int|float, pattern: str = "sine"):
        """
        Time-based oscillator for generating peridoic waves independently.
        
        Args:
            a_min (int|float): The wave's minimum amplitude (lowest possible value).
            a_max (int|float): The wave's maximum amplitude (highest possible value).
            period (int|float): The speed in which the wave will complete one full cycle.
            pattern (str): The given wave pattern. Can be either "sine", "triangle", "square" or "sawtooth".
        """
        self._a_min = a_min
        self._a_max = a_max
        self._period = period
        
        self._pattern = pattern
        if pattern not in self._WAVE_TYPES:
            self._LOGGER.error(f"Oscillator received invalid wave pattern: {pattern}.")
        
        self._frequency = 1 / period
        self._time = 0
        
        self._LOGGER.info(f"Oscillator with pattern {self._pattern} initialized successfully.")
        
    def _get_wave_value(self, t) -> float:
        """Internal method for generating waveform patterns. Use update() to get wave values."""
        
        if self._pattern == "sine":
            return math.sin(t * 2 * math.pi)
        
        elif self._pattern == "triangle":
            return 2 * abs(((t % 1) * 2) - 1) - 1
        
        elif self._pattern == "square":
            return 1 if (t % 1) < 0.5 else -1
        
        elif self._pattern == "sawtooth":
            return 2 * (t % 1) - 1
        
        else:
            return 0 # Default fallback
        
    def update(self, dt: int|float) -> float:
        """
        Updates the oscillator based on the delta time from the gameloop. \n
        
        Args:
            dt (int|float): Delta time from the gameloop.
            
        Returns:
            float: The new float value of the wave.
        """
        self._time += dt
        normalized_value = self._get_wave_value(self._time * self._frequency)
        return self._a_min + (normalized_value + 1) /  2 * (self._a_max - self._a_min)