import math # faster for calculations as it is pre-compiled
import numpy as np



class Swarm():
    def __init__():
        self.gamma = 5
        self.center = []

    #@property 
    def bivariate_normal(self, x, y):
        return math.e**-((x-self.center[0])**2 + self.gamma*( y - self.center[1])**2)

    def dx(self, x, y):
        return self.bivariate_normal(x, y) * 2 * (x - self.centre[0])
    
    def dy(self, x, y):
        return self.bivariate_normal(x, y) * 2 * self.gamma * (y - self.centre[1])

    def xrot(self, x, y, theta):
        return (x - self.center[0])* math.cos(theta) - (y- self.center[1]) * math.sin(theta)
    
    def yrot(self, x, y, theta):
        return (x - self.center[0])* math.sin(theta) + (y- self.center[1]) * math.cos(theta)
    
    def R_star():
        return (x - center)**2 + self.gamma * ()**2