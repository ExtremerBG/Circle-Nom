from .functions import resource_path
import cProfile
import pstats

def profile(enable:bool, func, *args, **kwargs):
    """
    Profiles a given function and prints the profiling stats.

    Args:
        enable (bool): Whether the profile is enabled or not.
        func (Callable): The function to be profiled.
        *args: Positional arguments for the function.
        **kwargs: Keyword arguments for the function.
    """
    if enable:
        # Declare file path
        file_path = resource_path("helpers/profile_result.txt")
        
        # Declare and start profile
        profiler = cProfile.Profile()
        profiler.enable()
        
        # Exec func
        func(*args, **kwargs)
        
        # Stop profile
        profiler.disable()
        
        # Dump to file
        with open(file_path, 'x') as file:
            stats = pstats.Stats(profiler, stream=file)
            stats.sort_stats('time').print_stats()
    else:
        # Exec func only
        func(*args, **kwargs)
    

