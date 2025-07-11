from datetime import datetime
import cProfile
import pstats
import os

def profile(enable:bool, func, *args, **kwargs) -> None:
    """
    Profiles a given function and prints the profiling stats.

    Args:
        enable (bool): Whether the profile is enabled or not.
        func (Callable): The function to be profiled.
        *args: Positional arguments for the function.
        **kwargs: Keyword arguments for the function.
    """
    if enable:
        # Create profile file path
        profile_file = f"profiles/{datetime.now().strftime("%Y-%m-%d")}/result.txt"
        os.makedirs(os.path.dirname(profile_file), exist_ok=True)
    
        # Declare and start profile
        profiler = cProfile.Profile()
        profiler.enable()
        
        # Exec func
        func(*args, **kwargs)
        
        # Stop profile
        profiler.disable()
        
        # Dump to file
        with open(profile_file, 'w') as file:
            stats = pstats.Stats(profiler, stream=file)
            stats.sort_stats('time').print_stats()
    else:
        # Exec func only
        func(*args, **kwargs)
    

