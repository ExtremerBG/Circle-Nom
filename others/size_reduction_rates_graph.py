import matplotlib.pyplot as plt
import numpy as np

# Parameters
FACTOR = 30e-3
EXPONENT = 1.4
DT = 0.016

# Range of player sizes
SIZES = np.linspace(0, 160, 100)  # 100 points from size 0 to 160

# Calculate size reduction for each size
size_reduction = (FACTOR * (SIZES ** EXPONENT)) * DT

# Plotting the graph
plt.figure(figsize=(8, 6))
plt.plot(SIZES, size_reduction, label=f'exponent={EXPONENT}', color='blue')

# Customization
plt.title("Player Size Reduction vs Player Size")
plt.xlabel("Size")
plt.ylabel("Size Reduction")
plt.grid(True)
plt.legend()
plt.show()
