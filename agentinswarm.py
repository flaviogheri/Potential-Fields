import numpy as np
import math
from random import random

from swarmfield import Swarm_field

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

class swarm_agent(agent_template): 
    """ represents micro entity/agent in swarm"""
    def __init__(self, center_position, position, color, alpha_avoid, Rta_ratio, radius=10, goal=np.array([700,500]), max_speed=0.05, dt=0.1, obstacles_p=None):
        super().__init__(position, radius)

        self.vmax = max_speed
        self.dt = 1
        self.goal = goal

        # Potential field constants
        self.C = 0.15 # scaling factor for attractive force
        self.Q = 800 # scaling factor for repulsive force
        self.eta = 30000 # steepness of potential field (gain for attractive force)

        if obstacles_p is None:
            self.obstacles_p = []
        else:
            self.obstacles_p = obstacles_p
        self.v = self.desired_velocity  # to be updated before movement started so should be fine

        self.color = parse_color(color)

        self.swarm_field = Swarm_field(pos=center_position)
        self.r_avoid = self.calc_r_avoid()
        

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
    

    # @property
    # in future might be worth transforming this into a property instead !!
    @property 
    def calc_r_avoid(self):
        self.r_avoid = [math.sqrt((self.p[0] - obstacle_p[0])**2 + (self.p[1]-obstacle_p[1])**2) for obstacle_p in self.obstacles_p]
        return self.r_avoid
    
    def S_avoid(self, alpha_avoid, Rta_ratio):
        return (1 - 1/(1+ math.e**(alpha_avoid*(math.sqrt(self.r_avoid - Rta_ratio)))))
    
    def move(self):
        # Scale desired velocity by dt for frame-rate independent movement
        scaled_velocity = self.desired_velocity * self.dt
        self.p += self.desired_velocity



    


    # def attractive_force(self):

    #     return magnitude, direction  # Return both magnitude and direction
    
    # def repulsive_force(self, obstacle_p):

    #     if distance > self.Q:

    #     else:

    #     return magnitude, direction  # Return both magnitude and direction

    
    # def TPF(self):
    #     """returns the total potential field in that instance"""
    #     total_magnitude = 0
    #     total_direction = np.zeros_like(self.goal - self.p)

    #     # Combine attractive force
    #     mag, dir = self.attractive_force()
    #     total_magnitude += mag
    #     total_direction += mag * dir

    #     # Combine repulsive forces from obstacles
    #     for obstacle_p in self.obstacles_p:
    #         mag, dir = self.repulsive_force(obstacle_p)
    #         total_magnitude -= mag
    #         total_direction -= mag * dir

    #     return total_magnitude, total_direction
    

