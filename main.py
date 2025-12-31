# ~-~-~ Circle Nom main entry point ~-~-~
if __name__ == "__main__":
        
    # Firstly import Pygame and init everything required
    import pygame
    pygame.font.init()
    pygame.mixer.init()
    pygame.display.init()
    
    # Secondly import and create/load the config file, set the screen resolution
    from circle_nom.helpers.config_reader import ConfigReader
    ConfigReader.create_configs()
    screen = pygame.display.set_mode(size=ConfigReader.get_screen())
    
    # Lastly import the profiler and the Menu
    from circle_nom.helpers.profile import profile
    from circle_nom.ui.menu import Menu    
    
    # Call the Menu with the profiler - can be Enabled/Disabled in the config file
    profile(func=Menu(screen=screen).launch_main_menu)