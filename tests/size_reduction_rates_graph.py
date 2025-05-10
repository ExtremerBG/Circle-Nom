import sys 
from pathlib import Path 
sys.path.append(str(Path(__file__).resolve().parent.parent))

from circle_nom.helpers.player_utils import player_size_reduct
from tests.models.fake_player import FakePlayer
import matplotlib.pyplot as plt
import numpy as np
        
# Parameters
player = FakePlayer()
SIZES = np.linspace(0, 160, 100)
DT = 0.016

# Calculate size reduction for each size
reduction_rates = []
for i in range(len(SIZES) - 1):
    
    # Update player size
    player.size = SIZES[i]
    
    # Get new rate from function
    rate = player_size_reduct(player, DT)
    
    # Append results to data list
    reduction_rates.append(rate)
    
# Plotting the graph
plt.figure(figsize=(8, 6))
plt.plot(reduction_rates, label=f'Reduction Rate', color='blue')

# Customization
plt.title("Player Size Reduction vs Player Size")
plt.xlabel("Player Size")
plt.ylabel("Size Reduction")
plt.grid(True)
plt.legend()

# Show graph
plt.show()
