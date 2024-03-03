import numpy as np
import matplotlib.pyplot as plt
import json
from mpl_toolkits.mplot3d import Axes3D
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
z = np.zeros((len(y), len(x)))  # Initialize potential field as a 3D array

X, Y = np.meshgrid(x, y)  # Create meshgrid for grid structure

# Calculate force magnitudes and directions for each grid point
for i in range(len(x)):
    for j in range(len(y)):
        position = np.array([x[i], y[j]])  # Include z-coordinate (0)
        agent = Agent(
            position=position,
            color=agent_data['color'],
            radius=agent_data['length'],
            max_speed=0.5,
            obstacles_p=[obs_pos]
        )
        force, direction = agent.TPF()  # Get force magnitude and direction
        z[i, j] = force  # Store force magnitude in the appropriate cell

# Create 3D plot of the potential field
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Reshape X and Y into 1D arrays
X_1d = X.flatten()
Y_1d = Y.flatten()

print("X_1d: ", X.shape)
# Plot the potential field surface
ax.plot_trisurf(X_1d, Y_1d, z, cmap='viridis', vmin=-5, vmax=5)

# Plot the obstacle as a sphere
ax.plot_trisurf([obs_pos[0]], [obs_pos[1]], [0],  # Single point for sphere
                color='red', alpha=0.5)

ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_zlabel('Potential Field Value')
ax.set_title('Potential Field Visualization (3D)')
ax.set_xlim([X.min(), X.max()])
ax.set_ylim([Y.min(), Y.max()])
ax.set_zlim(-5, 5)  # Set z-axis limits

plt.show()
