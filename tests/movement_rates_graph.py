import sys 
from pathlib import Path 
sys.path.append(str(Path(__file__).resolve().parent.parent))

from circle_nom.helpers.player_utils import get_movement_rate
from tests.models.fake_player import FakePlayer
import matplotlib.pyplot as plt
import numpy as np

# Parameters
player = FakePlayer()
PLAYER_SPEED = 60
DT = 0.016

# Range of player sizes
SIZES = np.linspace(30, 120, 100)  # 100 points from size 30 to 120

# Calculate movement rate for each size
movement_nums = []
for i in range(len(SIZES) - 1):
    
    # Update player size
    player.size = SIZES[i]
    
    # Get new number from function
    rate = get_movement_rate(player, DT)
    
    # Append results to data list
    movement_nums.append(rate)
    
# Plotting the graph
plt.figure(figsize=(8, 6))
plt.plot(movement_nums, label='Player Movement Speed', color='blue')

# Customization
plt.title("Player Movement Speed vs Player Size")
plt.xlabel("Player Size")
plt.ylabel("Player Speed")
plt.grid(True)
plt.legend()
plt.show()
