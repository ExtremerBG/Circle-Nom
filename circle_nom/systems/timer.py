from circle_nom.systems.logging import get_logger
import threading
import time

logger = get_logger(name=__name__)

class Timer:
    
    def __init__(self, name: str | None = None, debug: bool = False) -> None:
        """
        A thread-safe Timer that runs in a background thread. \n
        Allows starting, stopping, resetting, and retrieving elapsed time. \n
        Starts a background thread that continuously updates the elapsed time.
        
        Args:
            name (str): Optional arg to set a custom thread name.
            debug (bool): Optional arg to enable debug mode.
        """
        self._debug = debug                       # Boolean for debugging prints
        self._start_time = None                   # Timestamp when the timer was started
        self._elapsed = 0                         # Total elapsed time in seconds
        self._formatted_last_elapsed = -1         # Cache used in formatted time to avoid recompute
        self._formatted_last_output = "0 seconds" # Cache used in formatted time to avoid recompute
        self._running = False                     # Flag indicating if the timer is running
        self._lock = threading.Lock()             # Lock to ensure thread-safe access
        self._thread = threading.Thread(target=self._run, daemon=True)
        if name: self._thread.name = name
        self._thread.start()
        if self._debug: logger.info(msg=f"Thread '{self._thread.name}' started. Timer object id {id(self)} created.")

    def _run(self) -> None:
        """
        Background thread method that updates the elapsed time while running.
        """
        while True:
            if self._running:
                with self._lock:
                    self._elapsed = time.time() - self._start_time
            time.sleep(0.016)  # Update every 16ms or ~60fps - less hinders performance, more breaks animations based on time

    def start(self) -> None:
        """
        Starts or resumes the timer.
        If already running, does nothing.
        """
        with self._lock:
            if not self._running:
                self._start_time = time.time() - self._elapsed
                self._running = True
        if self._debug: logger.info(msg=f"Thread '{self._thread.name}' has started its timer.")

    def stop(self) -> None:
        """
        Stops or pauses the timer.
        If already stopped, does nothing.
        """
        with self._lock:
            if self._running:
                self._elapsed = time.time() - self._start_time
                self._running = False
        if self._debug: logger.info(msg=f"Thread '{self._thread.name}' has stopped its timer.")

    def reset(self) -> None:
        """
        Resets the timer to zero.
        If running, continues from zero.
        If stopped, clears the start time.
        """
        with self._lock:
            self._start_time = time.time()
            self._elapsed = 0
            self._formatted_last_elapsed = -1
            self._formatted_last_output = "0 seconds"
            if not self._running:
                self._start_time = None
        if self._debug: logger.info(msg=f"Thread '{self._thread.name}' has reset its timer.")

    def get_time(self) -> float:
        """
        Returns the current elapsed time in seconds as a float.
        Can be safely called from any thread.
        
        Returns:
            float: The current elapsed time in seconds.
        """
        with self._lock:
            return self._elapsed
        
    def get_formatted_time(self) -> str:
        """
        Returns the elapsed time as a string in a fancier string format.
        
        Returns:
            str: The formatted time, e.g."2 hr, 24 min and 48 sec".
        """
        with self._lock:
            
            # Check if formatted time is not cached already
            # if one ore more seconds have passed create new string and recache
            if self._elapsed - self._formatted_last_elapsed >= 1:
                self._formatted_last_elapsed = self._elapsed
                
                # Calculate hours, minutes and seconds
                total_seconds = int(self._elapsed)
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                
                # Assemble the formatted output string
                formatted = ""
                if hours: formatted += f"{hours} hr, "
                if minutes: formatted += f"{minutes} min and "
                formatted += f"{seconds} sec"
                
                self._formatted_last_output = formatted
                return formatted
            
            # If it is, return cache to avoid calcs above
            return self._formatted_last_output