import numpy as np
import matplotlib.pyplot as plt
from swarmfield import Swarm_field

# Define parameters
gamma = 0.5
center = [0, 0]
# Rt_ratio = 0.1


# Define grid for potential field visualization
x = np.linspace(-300, 300, 100)
y = np.linspace(-300, 300, 100)
X, Y = np.meshgrid(x, y)  # Create meshgrid for grid structure


# Calculate force magnitudes for each grid point
F_total = np.zeros_like(X)  # Array to store force magnitudes (scalars)
swarm_field = Swarm_field(pos=[1, 1], gamma=gamma, center=center,Rto_ratio = 20, Rti_ratio = 100, Rta_ratio = 10)


for i in range(len(x)):
    for j in range(len(y)):
        swarm_field.pos = [x[i], y[j]]
        F_total[j, i] = np.linalg.norm(swarm_field.velocity())


# Create 2D colormap plot of the potential field
fig, ax = plt.subplots(figsize=(8, 6))

# Plot the magnitude
magnitude_plot = ax.imshow(
    F_total, cmap='viridis', extent=(x.min(), x.max(), y.min(), y.max()), origin='lower',
    interpolation='nearest', vmin=0, vmax=500
)
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_title('Potential Field Visualization (Magnitude)')
ax.set_xlim([X.min(), X.max()])
ax.set_ylim([Y.min(), Y.max()])

# Add colorbar
plt.colorbar(magnitude_plot, ax=ax, orientation='vertical', label='Magnitude')

plt.show()