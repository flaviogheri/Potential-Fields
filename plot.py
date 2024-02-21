import numpy as np
import matplotlib.pyplot as plt

from agent import Agent



n_steps = 20000

agent = Agent(position=[0,0], goal=np.array([700,500]), color="blue")

obstacle_p = [200,230]
att_fs = []
rep_fs = []

for _ in range(n_steps):

    att_f = np.linalg.norm(agent.Attractive_force())
    rep_f = np.linalg.norm(agent.Repulsive_force(obstacle_p))
    print(rep_f)


    att_fs.append(att_f)
    rep_fs.append(rep_f)

    agent.move()

# Create time array
time = np.arange(n_steps)

# Plot attractive and repulsive forces over time
plt.plot(time, att_fs, label='Attractive Force')
plt.plot(time, rep_fs, label='Repulsive Force')
plt.xlabel('Time Step')
plt.ylabel('Force Magnitude')
plt.title('Attractive and Repulsive Forces over Time')
plt.legend()
plt.grid(True)
plt.show()