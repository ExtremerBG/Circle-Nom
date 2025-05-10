import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from circle_nom.helpers.player_utils import player_dash_speed_increase
from tests.models.fake_player import FakePlayer
import matplotlib.pyplot as plt
import numpy as np

# Range of player sizes
SIZES = np.linspace(30, 120, 10)

# Calculate speed increase for each size using the actual formula
speed_increases = [player_dash_speed_increase(FakePlayer(size)) for size in SIZES]

# Plotting the bar chart
plt.figure(figsize=(8, 6))
plt.bar([str(round(size, 1)) for size in SIZES], speed_increases, color='skyblue', label='speed increases')

# Customization
plt.title("Player Dash Speed Increase for Different Sizes")
plt.xlabel("Player Size")
plt.ylabel("Dash Speed Increase")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.show()