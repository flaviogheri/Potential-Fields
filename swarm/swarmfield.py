import math # faster for calculations as it is pre-compiled
import numpy as np



class Swarm_field:
    def __init__(self, pos, gamma = 1, epsilon = 0.001, center = [0,0], Rto_ratio = 20, Rti_ratio = 30, Rta_ratio = 50):

        self.pos = [1,1]
        self.center = center

        self.gamma = gamma
        self.gamma_rot = 5
        # self.alpha_in = 5 # should be within
        # self.alpha_out = 5 # should be within
        # self.alpha_perp = 5 # should be within
        self.epsilon = epsilon
        self.Rto_ratio = Rto_ratio
        self.Rti_ratio = Rti_ratio
        self.Rta_ratio = Rta_ratio # ratio at which agents should avoid each other

        self.rad
        self.calculate_R_star
        self.calculate_delta_R_in
        self.calculate_delta_R_out

        # calculating liminting functions (alphas) using epsilon variable (S_in(R*) = epsilon)

        self.alpha_in = (1/self.Rti_ratio) * math.log(((1-self.epsilon)/self.epsilon))
        self.alpha_out = (1/self.Rto_ratio) * math.log(((1-self.epsilon)/self.epsilon))
        self.alpha_perp = (1/(((self.Rto_ratio-self.Rti_ratio)/2)**2)) * math.log(1-self.epsilon)
        self.alpha_avoid = (1/self.Rta_ratio) * math.log(((1-self.epsilon)/self.epsilon))


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
        # print("power: ", (-self.alpha_out*(self.r - (self.R_star+self.delta_R_out))))
        # IMPORT (TEMP ISSUE RESOLVE) found issue with powers (sigmoid), if outside the field by large margin, the powers used are extremly large, cancelling out
        # wont happen as previewed (see notes--> in theory this equation should simplify to Sout = 1-1/1+infty = 1)
        if  -self.alpha_out*(self.r - (self.R_star+self.delta_R_out)) > 20:
            return 1
        else: 
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
    