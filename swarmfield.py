import math # faster for calculations as it is pre-compiled
import numpy as np



class Swarm_field:
    def __init__(self, pos, gamma, center = [0,0], Rt_ratio=0.1):

        self.pos = [1,1]
        self.center = center

        self.gamma = gamma
        self.gamma_rot = 5
        self.alpha_in = 5 # should be within
        self.alpha_out = 5 # should be within
        self.alpha_perp = 5 # should be within
        self.Rto_ratio = Rt_ratio
        self.Rti_ratio = Rt_ratio

        self.rad
        self.calculate_R_star
        self.calculate_delta_R_in
        self.calculate_delta_R_out

    @property 
    def rad(self):
        self.r = math.sqrt((self.pos[0] - self.center[0])**2 + ((self.gamma**2) * (self.pos[1] - self.center[1])**2))

    @property
    def calculate_R_star(self):
        self.R_star = math.sqrt((self.pos[0] - self.center[0])**2 + self.gamma * (self.pos[1] - self.center[1])**2)
    @property
    def calculate_delta_R_in(self):
        """ inside boundary of the R neighboorhood"""
        self.delta_R_in = self.Rti_ratio * self.R_star

    @property
    def calculate_delta_R_out(self):
        """ outside boundary of the R neighboorhood"""
        self.delta_R_out = self.Rto_ratio * self.R_star


    #@property 
    def bivariate_normal(self):
        return math.e**-((self.pos[0]-self.center[0])**2 + self.gamma*(self.pos[1] - self.center[1])**2)

    def dx(self):
        return self.bivariate_normal() * 2 * (self.pos[0] - self.center[0])
    
    def dy(self):
        return self.bivariate_normal() * 2 * self.gamma * (self.pos[1] - self.center[1])

    # def xrot(self, x, y, theta):
    #     return (x - self.center[0])* math.cos(theta) - (y- self.center[1]) * math.sin(theta)
    
    # def yrot(self, x, y, theta):
    #     return (x - self.center[0])* math.sin(theta) + (y- self.center[1]) * math.cos(theta)
    
    def Sin(self):
        """ Limiting function (sigmoid)-> gradient vector field directed towards outside.
        (Called as such as it is only used within the center of the field)"""
        return 1 - (1/(1 + math.e ** (self.alpha_in*(self.r-(self.R_star+self.delta_R_in)))))

    def Sout(self):
        """ gradient vector fielsd directed towards center"""
        return 1 - (1/(1+ math.e ** (-self.alpha_out*(self.r - (self.R_star+self.delta_R_out)))))
    
    def N(self):
        return (math.e ** (-self.alpha_perp * (self.r - self.R_star)**20))

    def SGN(self):
        return (1 - 2 * (1/(1+ math.e ** (-self.alpha_perp* self.gamma_rot))))

    def velocity(self):
        """" function that returns the velocity of swarm field depending on the agents position
        inputs: x, y
        """
        vx = self.Sin() - self.Sout()*self.dx() + self.SGN() * self.N() * self.dx()
        vy = self.Sin() - self.Sout()*self.dy() + self.SGN() * self.N() * self.dy()
        return (vx, vy)

        # print((self.Sin() - self.Sout())*(self.dx(), self.dy()) + self.SGN() * self.N() * (self.dx(), self.dy()))
        # return None
    