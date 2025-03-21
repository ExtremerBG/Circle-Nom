from helpers.profile import profile
from models.menu import Menu

 # Set True to enable performance profiling
profile(False, Menu().launch)