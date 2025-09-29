# ~-~-~ Circle Nom main entry point ~-~-~
if __name__ == "__main__":
    
    # First import Pygame and init everything required
    import pygame
    pygame.font.init()
    pygame.mixer.init()
    pygame.display.init()
    
    # Set the Pygame display size - resolution can be configured in the config file
    from circle_nom.helpers.config_reader import ConfigReader
    screen = pygame.display.set_mode(size=ConfigReader.get_screen())
    
    # Call this method if you want the config to be created (if found missing) 
    # in the project's root folder and/or in C:/USERNAME/Documents/CircleNom/.
    ConfigReader.create_configs()
    
    # Lastly import the Profiler and the Game Menus
    from circle_nom.helpers.profile import profile
    from circle_nom.ui.menu import Menu
    
    # Call the Menus with the profiler - can be Enabled/Disabled in the config file
    profile(func=Menu(screen=screen).launch_main_menu)
