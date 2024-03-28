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
    def __init__(self, center_position, position, color, alpha_avoid, Rta_ratio, radius=10, goal=np.array([700,500]), max_speed=0.5, dt=0.1, obstacles_p=None):
        super().__init__(position, radius)

        self.vmax = max_speed
        self.dt = 1
        # self.goal = goal

        # # Potential field constants
        # self.C = 0.15 # scaling factor for attractive force
        # self.Q = 800 # scaling factor for repulsive force
        # self.eta = 30000 # steepness of potential field (gain for attractive force)4
        self.center_position = center_position

        if obstacles_p is None:
            self.obstacles_p = []
        else:
            self.obstacles_p = obstacles_p
        self.v = self.desired_velocity  # to be updated before movement started so should be fine

        self.color = parse_color(color)

        # self.r_avoid = self.calc_r_avoid

        # self.r_vision = self.r_avoid * 2

        # self.alpha_avoid 


   
#    def find_obs(self):
#         for 
        
    @property 
    def calc_r_avoid(self):
        self.distances = [abs(self.p - obstacle_p) for obstacle_p in self.obstacles_p]

    # def d_avoid(self):
    #     self.calc_r_avoid
    #     return [(-100 if (distance < self.swarm_field.Rta_ratio) else 1/ (1+ math.exp(-self.sigmoid_steepness * (distance - self.swarm_field.Rta_ratio)))) for distance in self.distances]

    def d_avoid(self):
        self.calc_r_avoid
        d_avoid = []

        """The following is wrong (please plot sigmoid in geogebra to see): 
        reason being is that the force increases with distance rather than reducing, above a new sigmoid shape has been made.
        """
        ######## TEMPORARY MAX RANGE PLEASE EDIT THIS LATER ##############

        ### (function in general is wrong but desperately need something that does what need it to without having to calibrate it myself too much)
        # what max range does is sets a max range at which we take the d_avoid, and also scales the force so that it varies from 0 - max_range
        max_range = self.swarm_field.Rta_ratio * 2


        for distance in self.distances:
            angle = np.arctan2(distance[1], distance[0])
            polar_distance = abs(np.linalg.norm(distance))



            if polar_distance < self.swarm_field.Rta_ratio:
                
                d_avoid.append((100, angle + np.pi))
        
        # d_avoid now is going to be a vector describing magnitude and direction of the force to avoid obstacles
        return d_avoid

            # if polar_distance < self.swarm_field.Rta_ratio :
            #     d_avoid.append([-1000, angle])
            #     print("polar_distance: ", polar_distance, "RTA: ", self.swarm_field.Rta_ratio, self.p)
            # else: 
            #     # instead of paper we will use ln(x/R-c/R) instead (as way easier), and create bound for if too distant can ignore
            #     if polar_distance - self.swarm_field.Rta_ratio > max_range:
            #         d_avoid.append([0,angle])
            #     else: 
            #         # finally use the ln(x/R-c/R) + c equation
            #         # print("actually within log range:", math.log(polar_distance/max_range - self.swarm_field.Rta_ratio/max_range))
            #         # d_avoid.append([20, angle])
            #         d_avoid.append([0,angle])
            #         # d_avoid.append([(math.log(polar_distance/max_range - self.swarm_field.Rta_ratio/max_range)),angle])

        # return d_avoid
        # for distance in self.distances:
        #     angle = np.arctan2(distance[1], distance[0])
        #     polar_distance = np.linalg.norm(distance)
        #     if  polar_distance < self.swarm_field.Rta_ratio:
        #         d_avoid.append([-100, angle])# this returns magnitude and angle (polar coordinates)
        #     else: 
        #         d_avoid.append([1 - (1 / (np.exp(-self.swarm_field.alpha_avoid * (polar_distance - self.swarm_field.Rta_ratio)))),angle])
        # return d_avoid

        
    @property 
    def swarm_field(self):
        return Swarm_field(pos=self.p, center=self.center_position)
    
    @property
    def desired_velocity(self):
        if np.array(self.obstacles_p).size == 0:
            v = self.swarm_field.velocity() 
        else: 
            nearest_obstacle = min(self.obstacles_p, key=lambda o: np.linalg.norm(o - self.p))
            print(nearest_obstacle)
            direction_to_obstacle = nearest_obstacle - self.p
            if np.linalg.norm(direction_to_obstacle) < self.swarm_field.Rta_ratio:
                v_avoid_obstacle = np.array(-1000 / np.linalg.norm(direction_to_obstacle))
            else:
                v_avoid_obstacle = np.array([0,0])
            # v_avoid_obstacle = -1000 / np.linalg.norm(direction_to_obstacle)
            
            v = np.array(self.swarm_field.velocity()- v_avoid_obstacle)
            # v = np.array(self.swarm_field.velocity() + self.sum_d_avoid())
            print(v)
            return v
    # @property
    # def desired_velocity(self):
    #     if np.array(self.obstacles_p).size == 0:
    #         v = self.swarm_field.velocity() 
    #     else:
    #         # print("vmax: " , self.vmax)
    #         # if np.all(self.sum_d_avoid()) > 0.0:
    #             # print('swarm field: ', self.swarm_field.velocity(), 'sum_d_avoid post conversion: ',self.sum_d_avoid())
    #             # print('position : ', self.p)
    #         v = np.array(self.swarm_field.velocity()) + self.sum_d_avoid()
    #     # Check if the magnitude of the desired velocity exceeds vmax
    #     desired_velocity_magnitude = np.linalg.norm(v) + 1000
        

    #     # v = v / desired_velocity_magnitude * self.vmax
    #     # if desired_velocity_magnitude > self.vmax:
    #     #     # Scale the velocity vector to ensure it falls within the vmax bounds
    #     #     v = v / desired_velocity_magnitude * self.vmax
    #     # print("derireved vel", v)
    #     return v
    
    def sum_d_avoid(self):

        # Initialize variables for sum of x-components and y-components
        sum_x = 0
        sum_y = 0
        d_avoid_list = self.d_avoid()
        # Sum up the x-components and y-components from all obstacles
        for magnitude, angle in d_avoid_list:
            # Convert angle to radians
            angle_rad = math.radians(angle)
            
            # Calculate x and y components
            x_component = magnitude * math.cos(angle_rad)
            y_component = magnitude * math.sin(angle_rad)

            # if magnitude <0 :
            #     print("magnitude: ", magnitude, "angle: ", angle, "angle_rad: ", angle_rad, "cos: ", math.cos(angle_rad), "x_component: ", x_component)

            # if math.cos(angle_rad) < 0 or math.sin(angle_rad) < 0:
            #     print("angle: ", angle, "angle_rad: ", angle_rad, "cos: ", math.cos(angle_rad), "x_component: ", x_component)

            # Adjust signs based on angle
            # if self.p[0] < 0:
            #     x_component = x_component

            # if self.p[1] < 0:
            #     y_component = -y_component

            # Add x and y components to the sum
            sum_x += x_component
            sum_y += y_component
            
        return np.array([sum_x, sum_y])

    
    # def sum_d_avoid(self):
    #     # returns the sum of all the gradients from all the obstacles around the robot

    #     # Calculate d_avoid for each obstacle
    #     d_avoid_list = self.d_avoid()
    #     print("d_avoid_list: ", d_avoid_list)
    #     # Initialize the sum of gradients
    #     sum_dx_avoid = 0
    #     sum_dy_avoid = 0
        
    #     # print("d_avoid_list: ", d_avoid_list)
    #     # Sum up the gradients from all obstacles
    #     for dx_avoid, dy_avoid in d_avoid_list:
    #         sum_dx_avoid += dx_avoid
    #         sum_dy_avoid += dy_avoid
    #     print("sum dx",sum_dx_avoid, sum_dy_avoid)
    #     # Return the sum of gradients
    #     # print("sum_dx_avoid, sum_dy_avoid :", sum_dx_avoid, sum_dy_avoid)
    #     return sum_dx_avoid, sum_dy_avoid


    def move(self):
        # Scale desired velocity by dt for frame-rate independent movement
        # print("swarm center: ", self.center_position)
        scaled_velocity = (self.desired_velocity[0] * self.dt, self.desired_velocity[1] * self.dt)
        self.p += scaled_velocity


    # @property
    # in future might be worth transforming this into a property instead !!


    # @property 
    # def calc_r_avoid(self):
    #     self.r_avoid = [math.sqrt((self.p[0] - obstacle_p[0])**2 + (self.p[1]-obstacle_p[1])**2) for obstacle_p in self.obstacles_p]
    #     return self.r_avoid
    
    # def S_avoid(self):


    #     ################## ISSUE HERE ############################	
    #     """ s avoid is getting smaller when agents getting bigger, not the adverse effect..., 
        
        
    #     indeed when the function is plotted it is seen that the function gets bigger with a larger r not the opposite effect...
        
    #     attempted sol: make it -alpha_avoid"""

    #     # return [1 if (r - self.swarm_field.Rta_ratio) < 0 else: deltaSavoid for ]

        

    #     # print("sqrt param: ", [abs(r - self.swarm_field.Rta_ratio) for r in self.r_avoid])
    #     # print("S_avoid: ", [(1 - 1/(1 + math.e**(-self.swarm_field.alpha_avoid*(math.sqrt(r - self.swarm_field.Rta_ratio)))) ) for r in self.r_avoid])
    #     if all([(r - self.swarm_field.Rta_ratio) > 0 for r in self.r_avoid]):
    #         return [(1 - 1/(1 + math.e**(-self.swarm_field.alpha_avoid*(math.sqrt(r - self.swarm_field.Rta_ratio))))) for r in self.r_avoid]
    #     else:
    #         return [1 for r in self.r_avoid]
    #     # return [1 if (r - self.swarm_field.Rta_ratio) < 0 else 
    #     #     (1 - 1/(1 + math.e**(-self.swarm_field.alpha_avoid*(math.sqrt(r - self.swarm_field.Rta_ratio))))) for r in self.r_avoid]


    # def d_avoid_params(self):


    #     """ find parameters required to calculate d_avoid"""

    #     C =
    #     a = self.center_position[0]
    #     b = self.center_position[1]
    #     Q = 
    #     r_avoid =


    
    # def d_avoid(self):
        # retuns the d_avoid for each obstacle in the surroundings
        # self.calc_r_avoid  # Calculate r_avoid before using it
        # print("d_avoid: ", [(self.S_avoid()[i] * (self.p[0] - self.obstacles_p[i][0]), self.S_avoid()[i] * (self.p[1] - self.obstacles_p[i][1])) for i in range(len(self.obstacles_p))]
        # print("d_avoid: ", [(self.S_avoid()[i] , self.S_avoid()[i]) for i in range(len(self.obstacles_p))])
        
        # return [(self.S_avoid()[i] , self.S_avoid()[i]) for i in range(len(self.obstacles_p))]
        # return [(self.S_avoid()[i] * (self.p[0] - self.obstacles_p[i][0]), self.S_avoid()[i] * (self.p[1] - self.obstacles_p[i][1])) for i in range(len(self.obstacles_p))]
    
        # return [(self.S_avoid()[i] * (self.p[0] - self.obstacles_p[i][0]), 
        #             self.S_avoid()[i] * (self.p[1] - self.obstacles_p[i][1])) 
        #         for i in range(len(self.obstacles_p))]

        # return [1 if ]