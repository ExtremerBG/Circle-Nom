import matplotlib.pyplot as plt
import numpy as np

# Parameters
FACTOR = 100
EXPONENT = 0.25
PLAYER_SPEED = 60
DT = 0.016

# Range of player sizes
SIZES = np.linspace(30, 120, 100)  # 100 points from size 30 to 120

# Calculate movement rate for each size
movement_rates = ((FACTOR / (SIZES ** EXPONENT)) * PLAYER_SPEED) * DT

# Plotting the graph
plt.figure(figsize=(8, 6))
plt.plot(SIZES, movement_rates, label=f'exponent={EXPONENT}', color='blue')

# Customization
plt.title("Player Movement Speed vs Player Size")
plt.xlabel("Size")
plt.ylabel("Speed")
plt.grid(True)
plt.legend()
plt.show()
