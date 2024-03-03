import numpy as np
import matplotlib.pyplot as plt
import json
from agent import Agent


# Load obstacle and agent data
with open('obs.json') as f:
    obs_data = json.load(f)

with open('agent.json') as f:
    agent_data = json.load(f)

obs_pos = (int(obs_data['position']['x']), int(obs_data['position']['y']))
obs_radius = int(obs_data['length'])

# Define grid for potential field visualization
x = np.linspace(0, 800, 50)
y = np.linspace(0, 600, 50)
X, Y = np.meshgrid(x, y)  # Create meshgrid for grid structure

# Calculate force magnitudes and directions for each grid point
F_total = np.zeros((len(y), len(x)))  # Array to store force magnitudes (scalars)

for i in range(len(x)):
    for j in range(len(y)):
        position = np.array([x[i], y[j]])
        agent = Agent(
            position=position,
            color=agent_data['color'],
            radius=agent_data['length'],
            max_speed=0.5,
            obstacles_p=[obs_pos]
        )
        F_total[i,j] = agent.TPF()[0]

# Create 2D colormap plot of the potential field with arrows indicating direction
fig, ax = plt.subplots(figsize=(8, 6))

# Plot the magnitude first
magnitude_plot = ax.imshow(
    F_total, cmap='viridis', vmin=-5, vmax=5, extent=(x.min(), x.max(), y.min(), y.max())
)
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_title('Potential Field Visualization (Magnitude)')
ax.set_xlim([X.min(), X.max()])
ax.set_ylim([Y.min(), Y.max()])

# ax.scatter(obs_pos[0], obs_pos[1], color='red', label='Obstacle')
ax.legend()

# Use the magnitude plot as the mappable for the colorbar
plt.colorbar(magnitude_plot)
plt.show()

