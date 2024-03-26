import numpy as np
import matplotlib.pyplot as plt
from agentinswarm import swarm_agent


gamma = 0.5
center = [0, 0]

x = np.linspace(-300, 300, 100)
y = np.linspace(-300, 300, 100)
X, Y = np.meshgrid(x, y) 

obstacles = np.array([[100,100], [-100,-100], [300,300], [400,400], [500,500], [600,600], [700,700], [800,800], [900,900]])

agent = swarm_agent(center_position=center, obstacles_p=obstacles, position=[1, 1], color="red", alpha_avoid=5, Rta_ratio=10, radius=10, max_speed=20)


F_total = np.zeros_like(X)

for i in range(len(x)):
    for j in range(len(y)):
        # agent.p = np.array([x[i], y[j]])
        agent.p = np.array([x[i], y[j]]).astype(int)
        # print("F_total: ", np.linalg.norm(agent.desired_velocity))
        F_total[j, i] = np.linalg.norm(agent.desired_velocity)


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

# Add colorbar to the plot
cbar = fig.colorbar(magnitude_plot)
cbar.set_label('Magnitude')

# Display the plot
plt.show()