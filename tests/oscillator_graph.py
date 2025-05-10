import sys 
from pathlib import Path 
sys.path.append(str(Path(__file__).resolve().parent.parent))

from circle_nom.systems.oscillator import Oscillator 
import matplotlib.pyplot as plt 
from random import randint
import pygame

# Config
TOTAL_FRAMES = 1000
FPS_RANGE = 30, 1000
wave = Oscillator(a_min=-5, a_max=5, period=1.8, pattern="sine")

DT_LOG = [] 
WAVE_VALUES = []
clock = pygame.Clock()
for _ in range(TOTAL_FRAMES):

    # Random FPS cap to simulate inconsistent dt
    dt = clock.tick(randint(*FPS_RANGE)) / 1000
    
    # Append results to data lists
    DT_LOG.append(clock.get_fps())
    WAVE_VALUES.append(wave.update(dt))

# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(10, 6))

# Primary Y-axis (left) - Amplitude
ax1.plot(WAVE_VALUES, label='Oscillator Output', color='blue')
ax1.set_ylabel("Wave Amplitude")
ax1.set_xlabel("Total Frames")

# Secondary Y-axis (right) - Delta Time
ax2 = ax1.twinx()  # Creates separate y-axis but shares x-axis
ax2.plot(DT_LOG, label='Game Loop FPS', color=(1, 0, 0, 0.75), linestyle='dotted')
ax2.set_ylabel("FPS")

# Other customisations
fig.suptitle("Time-based Oscillator")
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")
ax1.grid(True)

# Show graph
plt.show()