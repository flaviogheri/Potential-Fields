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
    def __init__(self, position, color, radius=10, goal=np.array([700,500]), max_speed=0.05):
        super().__init__(position, radius)

        self.vmax = max_speed
        self.goal = goal

        # Potential field constants
        self.C = 0.1
        self.Q = 500
        self.eta = 30000

        self.obstacles_p = []
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
            desired_velocity = self.Attractive_force()
        else: 
            desired_velocity = self.TPF()
    
        # Check if the magnitude of the desired velocity exceeds vmax
        desired_velocity_magnitude = np.linalg.norm(desired_velocity)
        
        if desired_velocity_magnitude > self.vmax:
            # Scale the velocity vector to ensure it falls within the vmax bounds
            desired_velocity = desired_velocity / desired_velocity_magnitude * self.vmax

        return desired_velocity
    
    def move(self):
        self.p += self.desired_velocity

    
    

    def Attractive_force(self):
        direction = (self.goal - self.p) / np.linalg.norm(self.goal - self.p)
        magnitude = self.C * np.sqrt(np.linalg.norm(self.p - self.goal))
        force_vector = magnitude * direction
        return force_vector
        # delta_Uatt = self.C * np.sqrt(np.linalg.norm( self.p[0]- self.goal[0]) + np.linalg.norm(self.p[1] - self.goal[1]))

        # return delta_Uatt
    
    def Repulsive_force(self, obstacle_p):
        direction = (self.p - obstacle_p) / np.linalg.norm(self.p - obstacle_p)
        distance = np.linalg.norm(obstacle_p - self.p)
        if distance>self.Q:
            delta_Urep = 0
        else:        
            delta_Urep = self.eta * (1/self.Q - 1/distance)* (1/(distance **2))
        force_vector = delta_Urep * direction
        return force_vector
    
    def TPF(self):
        """returns the total potential field in that instance"""
        F_att = self.Attractive_force()
        F_total = F_att
        for obstacle_p in self.obstacles_p: 
            F_total += self.Repulsive_force(obstacle_p)
            print("att", F_att, "rep", self.Repulsive_force(obstacle_p), "F_total", F_total)
        return F_total





    # def Attraction_force():
    #     """ currently using basic formulation, in future think of changing for more complex. (So that attractive force gorues more slowly)
        
    #     potential idea--> use quadratic potential near goal (<d*) and conic further away"""

    #     Uatt = C * np.sqrt(np.linalg.norm(self.p[0]-self.goal[0]) + np.linalg.norm(self.p[1] - self.goal[1]))
    #     return Uatt
    
    # def Repuslive_force(obstacle_p):
    #     """ distances of obstacles are measured in theta (radians) and euclidian distance"""

    #     distance = np.linalg.norm(obstacle_p - self.p)
    #     if distance > Q:
    #         Urep = 0
    #     else: 
    #         Urep= 1 / (distance)
    #     return Urep



    # @property
    # def desired_velocity(self):
    #     distance = self.goal - self.p
    #     norm = np.linalg.norm(distance)
    #     if norm < self.r :
    #         return np.zeros(2)
    #     direction = distance / norm
    #     return self.vmax * direction

