import sys 
from pathlib import Path 
sys.path.append(str(Path(__file__).resolve().parent.parent))

from models.oscillator import Oscillator 
import matplotlib.pyplot as plt 
from random import uniform

# Config
TOTAL_FRAMES = 300
DT_RANGE = 0.033, 0.002
wave = Oscillator(a_min=-5, a_max=5, period=1.5, pattern="sawtooth")

DT_LOG = [] 
WAVE_VALUES = []
for _ in range(TOTAL_FRAMES):

    # Random delta time to simulate inconsistent Frame Times
    # DT_RANGE must be 0.033, 0.002 for ~30 to ~500 FPS delta.
    dt = uniform(*DT_RANGE)
    
    # Append results to data lists
    DT_LOG.append(dt)
    WAVE_VALUES.append(wave.update(dt))

# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(10, 6))

# Primary Y-axis (left) - Amplitude
ax1.plot(WAVE_VALUES, label='Oscillator Output', color='blue')
ax1.set_ylabel("Wave Amplitude")
ax1.set_xlabel("Frames")

# Secondary Y-axis (right) - Delta Time
ax2 = ax1.twinx()  # Creates separate y-axis but shares x-axis
ax2.plot(DT_LOG, label='Random Delta Time', color=(1, 0, 0, 0.75), linestyle='dotted')
ax2.set_ylabel("Delta Time")

# Other customisations
fig.suptitle("Time-based Oscillator")
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")
ax1.grid(True)

# Show graph
plt.show()