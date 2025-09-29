from genericpath import exists
from pathlib import Path
import configparser
import traceback
import os

class ConfigReader:
    """ 
    This config reader supports reading a config.ini file located in either the project's root or in C:/USERNAME/Documents/CircleNom/. \n
    Loading order is the root config first, then documents and lastly the defaults are loaded if neither is found. \n
    Call create_configs method to create a new config with default values, if the file cannot be found in either location. \n
    Other features are extensive error checking and debug message printing, meaning if any of the config file has invalid or missing data, \n
    it will automatically fallback to its default settings and notify the user. All of its methods are classmethods, there is no __init__, \n
    meaning you only need to import this class to use it properly. Check the _DEFAULT_CONFIG const for more info on what the config contains.
    """
    
    # ConfigParser object
    _config_parser = configparser.ConfigParser()
    _loaded = False
    
    # Default fallback config
    _DEFAULT_CONFIG = {
        # Screen dimentions - note that only the background image scales.
        "SCREEN": {
            "screen_width": 1280,
            "screen_height": 720
        },
        
        # Prey difficulty values - Prey spawn timers in seconds
        "PREY_DIFFICULTY": {
            "easy_diff": 2.4,
            "medium_diff": 1.8,
            "hard_diff": 1.2,
            "impossible_diff": 0.6
        },
        
        # Dagger difficulty values - Daggers spawn rate in seconds
        "DAGGER_DIFFICULTY": {
            "easy_diff": 1.0,
            "medium_diff": 0.7,
            "hard_diff": 0.4,
            "impossible_diff": 0.1
        },
        
        # Easter egg mode - percent chance to occur
        "EASTER": {
            "easter_chance": 10
        },
        
        # Logging options - Enable/Disable booleans
        "LOGGING": {
            "console_logging": True,
            "file_logging": False
        },
        
        # Debug options - Enable/Disable booleans
        "DEBUG": {
            "player_debug": False,
            "prey_debug": False,
            "dagger_debug": False
        },
        
        # Performance profiler options - Enable/Disable booleans
        "PROFILE": {
            "perf_profile": False
        }
    }
    
    # Create a dictionary with the name of the config file and its path
    _CONFIG_NAME_AND_PATH = {
        "Root": Path(__file__).resolve().parents[2] / "config.ini",
        "Documents": (Path(os.environ["USERPROFILE"]) / "Documents" / "CircleNom" / "config.ini")
    }
    # Ensure the documents path has the folders required
    _CONFIG_NAME_AND_PATH["Documents"].parent.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def create_configs(cls) -> None:
        """
        Automatically create new config files in the project's root folder and in C:/USERNAME/Documents/CircleNom/ \n
        if any of the locations are missing the file. Does not override an already existing config file.
        """
        count = 0
        print("Checking if config files are missing...")
        for NAME, PATH in cls._CONFIG_NAME_AND_PATH.items():
            if not exists(PATH):
                print(f"{NAME} config not found. Trying to create one with default values.")
                try:
                    for section, options in cls._DEFAULT_CONFIG.items():
                        cls._config_parser[section] = {k: str(v) for k, v in options.items()}
                        
                    with open(PATH, 'w') as docs_config:
                        cls._config_parser.write(docs_config)
                    print(f"{NAME} config created successfully at '{PATH}'.")
                except:
                    print(f"An error occured while trying to create the {NAME} config.")
                    print(traceback.format_exc)
            else:
                print(f"{NAME} config found at '{PATH}'.")
                count += 1
        if count == len(cls._CONFIG_NAME_AND_PATH.values()):
            print("All config files accounted for.")
     
    @classmethod
    def _load_config(cls) -> None:
        if not cls._loaded:
            
            # Try to load config file in order project root -> documents folder
            for NAME, PATH in cls._CONFIG_NAME_AND_PATH.items():
                if PATH.exists():
                    try:
                        cls._config_parser.read(PATH)
                        cls._loaded = True
                        print(f"{NAME} config loaded at '{PATH}'.")
                        return
                    except Exception:
                        print(f"An error occured while trying to load the {NAME} config at '{PATH}'.")
                        traceback.print_exc()
                else:
                    print(f"Could not find the {NAME} config at '{PATH}'.")
                    
            print(f"Both Root and Documents config files could not be loaded. Using default values.")
            cls._config_parser.read_dict(cls._DEFAULT_CONFIG)
                
    @classmethod
    def _safe_section(cls, section: str) -> configparser.SectionProxy:
        """Safely get section with ConfigParser. If not found, inject default values."""
        cls._load_config()
        if section not in cls._config_parser:
            print(f"{section} section not found in config file. Injecting default values.")
            cls._config_parser[section] = {k: str(v) for k, v in cls._DEFAULT_CONFIG[section].items()}
        return cls._config_parser[section]
    
    @classmethod
    def _safe_getint(cls, section: configparser.SectionProxy,  key: str, fallback: int) -> int:
        """Safely get int value with the key from the given section."""
        try:
            return section.getint(key, fallback=fallback)
        except (ValueError, TypeError):
            return fallback
    
    @classmethod
    def _safe_getfloat(cls, section: configparser.SectionProxy,  key: str, fallback: float) -> float:
        """Safely get float value with the key from the given section."""
        try:
            return section.getfloat(key, fallback=fallback)
        except (ValueError, TypeError):
            return fallback

    @classmethod
    def _safe_getbool(cls, section: configparser.SectionProxy,  key: str, fallback: bool) -> bool:
        """Safely get boolean value with the key from the given section."""
        try:
            return section.getboolean(key, fallback=fallback)
        except (ValueError, TypeError):
            return fallback
        
    @classmethod
    def get_screen(cls) -> tuple[int, int]:
        """Get a tuple consisting of the screen width and height pixel values."""
        section = cls._safe_section("SCREEN")
        return (
            cls._safe_getint(section=section, key="screen_width", fallback=int(cls._DEFAULT_CONFIG["SCREEN"]["screen_width"])),
            cls._safe_getint(section=section, key="screen_height", fallback=int(cls._DEFAULT_CONFIG["SCREEN"]["screen_height"]))
        )
    
    @classmethod
    def get_prey_difficulty(cls) -> tuple[float, float, float, float]:
        """
        Get the Prey dificulty values (in seconds) which affect the Prey spawning cooldowns. \n
        Value order corresponds to Easy, Medium, Hard & Impossible difficulties.
        """
        section = cls._safe_section("PREY_DIFFICULTY")
        return (
            cls._safe_getfloat(section=section, key="easy_diff", fallback=float(cls._DEFAULT_CONFIG["PREY_DIFFICULTY"]["easy_diff"])),
            cls._safe_getfloat(section=section, key="medium_diff", fallback=float(cls._DEFAULT_CONFIG["PREY_DIFFICULTY"]["medium_diff"])),
            cls._safe_getfloat(section=section, key="hard_diff", fallback=float(cls._DEFAULT_CONFIG["PREY_DIFFICULTY"]["hard_diff"])),
            cls._safe_getfloat(section=section, key="impossible_diff", fallback=float(cls._DEFAULT_CONFIG["PREY_DIFFICULTY"]["impossible_diff"]))
        )
        
    @classmethod
    def get_dagger_difficulty(cls) -> tuple[float, float, float, float]:
        """
        Get the Dagger difficulty values (in seconds) which affect the Dagger spawnrate and deviance cooldowns. \n
        Value order corresponds to Easy, Medium, Hard & Impossible difficulties.
        """
        section = cls._safe_section("DAGGER_DIFFICULTY")
        return (
            cls._safe_getfloat(section=section, key="easy_diff", fallback=float(cls._DEFAULT_CONFIG["DAGGER_DIFFICULTY"]["easy_diff"])),
            cls._safe_getfloat(section=section, key="medium_diff", fallback=float(cls._DEFAULT_CONFIG["DAGGER_DIFFICULTY"]["medium_diff"])),
            cls._safe_getfloat(section=section, key="hard_diff", fallback=float(cls._DEFAULT_CONFIG["DAGGER_DIFFICULTY"]["hard_diff"])),
            cls._safe_getfloat(section=section, key="impossible_diff", fallback=float(cls._DEFAULT_CONFIG["DAGGER_DIFFICULTY"]["impossible_diff"]))
        )
        
    @classmethod
    def get_easter_chance(cls) -> float:
        """
        Get the percent chance of easter egg mode happening.
        """
        section = cls._safe_section("EASTER")
        return cls._safe_getfloat(section=section, key="easter_chance", fallback=float(cls._DEFAULT_CONFIG["EASTER"]["easter_chance"]))
            
    @classmethod
    def get_logging(cls) -> tuple[bool, bool]:
        """Get the logging setting values. First boolean toggles console logging, second toggles file logging."""
        section = cls._safe_section("LOGGING")
        return (
            cls._safe_getbool(section=section, key="console_logging", fallback=bool(cls._DEFAULT_CONFIG["LOGGING"]["console_logging"])),
            cls._safe_getbool(section=section, key="file_logging", fallback=bool(cls._DEFAULT_CONFIG["LOGGING"]["file_logging"]))
        )
        
    @classmethod
    def get_debug(cls) -> tuple[bool, bool, bool]:
        """Get the debug setting values. 3 booleans corresponding to toggling Player, Prey and Dagger debug options."""
        section = cls._safe_section("DEBUG")
        return (
            cls._safe_getbool(section=section, key="player_debug", fallback=bool(cls._DEFAULT_CONFIG["DEBUG"]["player_debug"])),
            cls._safe_getbool(section=section, key="prey_debug", fallback=bool(cls._DEFAULT_CONFIG["DEBUG"]["prey_debug"])),
            cls._safe_getbool(section=section, key="dagger_debug", fallback=bool(cls._DEFAULT_CONFIG["DEBUG"]["dagger_debug"]))
        )
        
    @classmethod
    def get_profile(cls) -> bool:
        """Get the performace profile toggle setting value."""
        section = cls._safe_section("PROFILE")
        return cls._safe_getbool(section=section, key="perf_profile", fallback=bool(cls._DEFAULT_CONFIG["PROFILE"]["perf_profile"]))