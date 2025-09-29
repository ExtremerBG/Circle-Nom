from circle_nom.helpers.config_reader import ConfigReader
from circle_nom.systems.logging import get_logger
from datetime import datetime
import cProfile
import pstats
import os

# Logger reference
_LOGGER = get_logger(name=__name__)

def profile(func, *args, **kwargs) -> None:
    """
    Profiles a given function and prints the profiling stats.

    Args:
        func (Callable): The function to be profiled.
        *args: Positional arguments for the function.
        **kwargs: Keyword arguments for the function.
    """
    # If Profiler is enabled in config
    if ConfigReader.get_profile():
        
        # Create profile file path
        profile_file = f"profiles/{datetime.now().strftime("%Y-%m-%d")}/output.txt"
        os.makedirs(os.path.dirname(profile_file), exist_ok=True)
    
        # Declare and start profile
        profiler = cProfile.Profile()
        profiler.enable()
        
        # Log profile start
        _LOGGER.info("Profiler started.")
        
        # Exec func
        func(*args, **kwargs)
        
        # Stop profile
        profiler.disable()
        
        # Dump to file
        with open(profile_file, 'w') as file:
            stats = pstats.Stats(profiler, stream=file)
            stats.sort_stats('time').print_stats()
            
        # Log profile finish
        _LOGGER.info(f"Profiler finished, output file is at '{os.path.abspath(profile_file)}'.")
        
    # If not exec only the given func
    else:
        func(*args, **kwargs)