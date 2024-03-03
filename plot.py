# # import numpy as np
# # import matplotlib.pyplot as plt

# # from agent import Agent



# # n_steps = 20000

# # agent = Agent(position=[0,0], goal=np.array([700,500]), color="blue")

# # obstacle_p = [200,230]
# # att_fs = []
# # rep_fs = []

# # for _ in range(n_steps):

# #     att_f = np.linalg.norm(agent.Attractive_force())
# #     rep_f = np.linalg.norm(agent.Repulsive_force(obstacle_p))
# #     print(rep_f)


# #     att_fs.append(att_f)
# #     rep_fs.append(rep_f)

# #     agent.move()

# # # Create time array
# # time = np.arange(n_steps)

# # # Plot attractive and repulsive forces over time
# # plt.plot(time, att_fs, label='Attractive Force')
# # plt.plot(time, rep_fs, label='Repulsive Force')
# # plt.xlabel('Time Step')
# # plt.ylabel('Force Magnitude')
# # plt.title('Attractive and Repulsive Forces over Time')
# # plt.legend()
# # plt.grid(True)
# # plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
# from agent import Agent
# import json

# def parse_color(color_str):
#     color_dict = {
#         "red": (255, 0, 0),
#         "green": (0, 255, 0),
#         "blue": (0, 0, 255),
#         "yellow": (255, 255, 0),
#         "purple": (128, 0, 128),
#         "orange": (255, 165, 0),
#         "pink": (255, 192, 203),
#         "black": (0, 0, 0),
#         "white": (255, 255, 255)
#     }
#     return color_dict.get(color_str, (0, 0, 0))


# def visualize_potential_field():
#     # Load agent and obstacle data
#     with open('agent.json') as f:
#         agent_data = json.load(f)

#     with open('obs.json') as f:
#         obs_data = json.load(f)




# def visualize_potential_field():
#     # Load agent and obstacle data
#     with open('agent.json') as f:
#         agent_data = json.load(f)

#     with open('obs.json') as f:
#         obs_data = json.load(f)

#     # Create agent object
#     agent = Agent(position=(agent_data['position']['x'], agent_data['position']['y']),
#                   color=agent_data['color'],
#                   radius=agent_data['length'],
#                   max_speed=0.5)

#     # Extract obstacle position and radius and convert to integers
#     obs_pos = (int(obs_data['position']['x']), int(obs_data['position']['y']))
#     obs_radius = int(obs_data['length'])

#     # Extract goal position
#     goal_pos = (agent.goal[0], agent.goal[1])


#     # Normalize color values to the range [0, 1]
#     obs_color = tuple(c / 255 for c in parse_color(obs_data['color']))
#     goal_color = 'green'  # You can choose the color for the goal position

#     # Define grid for potential field visualization
#     x = np.linspace(0, 800, 50)
#     y = np.linspace(0, 600, 50)
#     X, Y = np.meshgrid(x, y)

#     # Calculate potential field at each point in the grid
#     F_total = np.zeros_like(X)
#     for i in range(len(x)):
#         for j in range(len(y)):
#             position = np.array([x[i], y[j]])
#             F_total[j, i] = np.linalg.norm(agent.Repulsive_force(position) + agent.Attractive_force())

#     # Plot potential field with obstacles
#     plt.figure(figsize=(8, 6))
#     levels = np.linspace(0, np.max(F_total), 50)  # Adjust levels for better visibility
#     plt.contourf(X, Y, F_total, levels=levels, cmap='viridis')
#     plt.colorbar(label='Potential Field Magnitude')
#     plt.scatter(*agent.p, color=parse_color(agent.color), label='Agent')
#     circle = plt.Circle(obs_pos, obs_radius, color=obs_color, fill=True, alpha=0.5)
#     plt.gca().add_patch(circle)
#     plt.scatter(*goal_pos, color=goal_color, label='Goal')  # Plotting the goal position
#     plt.xlabel('X Position')
#     plt.ylabel('Y Position')
#     plt.title('Static Visualization of Potential Field')
#     plt.legend()
#     plt.grid(True)
#     plt.show()

# if __name__ == "__main__":
#     visualize_potential_field()
