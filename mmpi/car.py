import math
from numpy import random

class Car:
    def __init__(self, x=0, y=0, vx=0, vy=0):
        self.x = [x , y, vx, vy] #x, y, vx, vy
        self.u = [0, 0] #ax, ay
        self.previous_positions = []
        self.width = 30
        self.height = 50
        self.thrust = 200

    def update(self, dt):
        self.x[2] += (self.u[0]*self.thrust - self.x[2]) * dt
        self.x[3] += (self.u[1]*self.thrust - self.x[3]) * dt
        self.x[0] += self.x[2] * dt
        self.x[1] += self.x[3] * dt
        
