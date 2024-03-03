import numpy as np
from random import random

def to_np_float_array(x):
    return np.array(x, dtype=float)

def parse_color(color_str):
    if color_str == "red":
        return (255, 0, 0)
    elif color_str == "green":
        return (0, 255, 0)
    elif color_str == "blue":
        return (0, 0, 255)
    elif color_str == "yellow":
        return (255, 255, 0)
    elif color_str == "purple":
        return (128, 0, 128)
    elif color_str == "orange":
        return (255, 165, 0)
    elif color_str == "pink":
        return (255, 192, 203)
    elif color_str == "black":
        return (0, 0, 0)
    elif color_str == "white":
        return (255, 255, 255)
    else:
        return (0, 0, 0)


class agent_template:
    def __init__(self, position:[np.ndarray, list, tuple], radius: float= 0.5, velocity: [np.ndarray, list, tuple]= np.zeros(2)):
        self.p = to_np_float_array(position)
        self.r = radius
        self.v = to_np_float_array(velocity)

class Agent(agent_template): 
    """ represents micro entity/agent in swarm"""
    def __init__(self, position, color, radius=10, goal=np.array([700,500]), max_speed=0.05, obstacles_p=None):
        super().__init__(position, radius)

        self.vmax = max_speed
        self.goal = goal

        # Potential field constants
        self.C = 0.1
        self.Q = 800
        self.eta = 30000

        if obstacles_p is None:
            self.obstacles_p = []
        else:
            self.obstacles_p = obstacles_p
        self.v = self.desired_velocity  # to be updated before movement started so should be fine

        self.color = parse_color(color)


# class Agent(agent_template): 
#     """ represents micro entity/agent in swarm"""
#     def __init__(self, position, radius = 10, goal: [np.ndarray, list, tuple]= np.array([2,2]), max_speed = 5):
#         super().__init__(position, radius)

#         self.vmax = max_speed
#         self.goal = goal
#         self.v = self.desired_velocity # to be updated before movement started so should be fine

#         self.color = parse_color(color)

#         # Potential field constants
#         self.C = 1.0
#         self.Q = 1.0
#         self.eta = 1.0

#         self.obstacles_p = []


    @property
    def desired_velocity(self):
        if not self.obstacles_p:
            _, desired_direction = self.attractive_force()
        else:
            _, desired_direction = self.TPF()

        # Check if the magnitude of the desired velocity exceeds vmax
        desired_velocity_magnitude = np.linalg.norm(desired_direction)

        if desired_velocity_magnitude > self.vmax:
            # Scale the velocity vector to ensure it falls within the vmax bounds
            desired_direction = desired_direction / desired_velocity_magnitude * self.vmax

        return desired_direction
    
    def move(self):
        self.p += self.desired_velocity

    def attractive_force(self):
        direction = (self.goal - self.p) / np.linalg.norm(self.goal - self.p)
        magnitude = self.C * np.sqrt(np.linalg.norm(self.p - self.goal))
        return magnitude, direction  # Return both magnitude and direction
    
    def repulsive_force(self, obstacle_p):
        direction = (self.p - obstacle_p) / np.linalg.norm(self.p - obstacle_p)
        distance = np.linalg.norm(obstacle_p - self.p)
        if distance > self.Q:
            magnitude = 0
        else:
            magnitude = self.eta * (1/self.Q - 1/distance) * (1/(distance **2))
        return magnitude, direction  # Return both magnitude and direction

    
    def TPF(self):
        """returns the total potential field in that instance"""
        total_magnitude = 0
        total_direction = np.zeros_like(self.goal - self.p)

        # Combine attractive force
        mag, dir = self.attractive_force()
        total_magnitude += mag
        total_direction += mag * dir

        # Combine repulsive forces from obstacles
        for obstacle_p in self.obstacles_p:
            mag, dir = self.repulsive_force(obstacle_p)
            total_magnitude -= mag
            total_direction -= mag * dir

        return total_magnitude, total_direction