import matplotlib.pyplot as plt
import numpy as np

# Parameters
FACTOR = 100
EXPONENT = 1.4

# Range of player sizes
SIZES = np.linspace(30, 120, 10) 

# Calculate speed increase for each size
speed_increases = [((FACTOR / (size ** EXPONENT)) * size) for size in SIZES]
new_speeds = [increase for increase in speed_increases]

# Plotting the bar chart
plt.figure(figsize=(8, 6))
plt.bar([str(size) for size in SIZES], new_speeds, color='skyblue', label=f'exponent={EXPONENT}')

# Customization
plt.title("Player Speed After Dash for Different Sizes")
plt.xlabel("Player Size")
plt.ylabel("Player Speed")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
