import car
from numpy import random
import numpy as np
import copy
import math

class MPPI:
    #K is number of samples, N is number of timesteps, U is control sequence
    def __init__(self, dt, K, N):
        self.dt = dt
        self.car = car.Car(x=0, y=0, vx=0, vy=0)
        self.costs = np.zeros(K)
        self.K = K
        self.N = N
        self.u = np.zeros((N, 2))
        self.allLocations = []
        self.locations = []
        self.totalCost = 0
        self.noise = []
        self.lowestCost = 5

        
    def cost(self):
        cost = 0
        #cost = cost + 99*(abs(self.car.u[0])+abs(self.car.u[0]))
        if self.car.x[0] < 100 and self.car.x[0] > -100 and self.car.x[1] < 100 and self.car.x[1] > -100:
            cost = cost + 9999
        return (abs(self.car.x[0]) + abs(self.car.x[1]-200) + cost)*.0001
    
    def getNoise(self):
        return random.normal(loc = 0, scale = 2*self.lowestCost, size=(self.K,self.N,2))

    def rollout(self, x, noise):
        self.totalCost = 0
        self.car.x = copy.deepcopy(x)

        self.locations = []
        for i in range(len(self.noise)):
            self.noise[i][0] *= np.exp(-0.05 * i)
            self.noise[i][1] *= np.exp(-0.05 * i)
        for i in range(self.N - 1):
            self.car.u = self.u[i] + noise[i]
            self.car.update(self.dt)
            self.totalCost += self.cost()
            self.locations.append((int(self.car.x[0] + self.car.width/2), int(self.car.x[1] + self.car.height/2)))
    
    def getUupdate(self, x):
        self.car.x = copy.deepcopy(x)
        index = np.argmin(self.costs)
        self.lowestCost = self.costs[index]
        for i in range(len(self.noise[index])):
            self.noise[index][i][0] *= np.exp(-0.05 * i)
            self.noise[index][i][1] *= np.exp(-0.05 * i)
        self.u = self.u + self.noise[index]
        for i in range(self.N - 1):
            self.car.u = self.u[i]
            self.car.update(self.dt)
            self.locations.append((int(self.car.x[0] + self.car.width/2), int(self.car.x[1] + self.car.height/2)))
        self.allLocations.append(self.locations)
        return self.u[0]
            
      
    def allPaths(self, x):
        #self.u = np.zeros((self.N, 2))
        self.allLocations = []
        self.noise = self.getNoise()
        for j in range(self.K):
            self.rollout(x, self.noise[j])
            self.allLocations.append(self.locations)
            self.costs[j] = self.totalCost
        #self.costs = self.costs/np.max(self.costs)
        
        action = self.getUupdate(x)

        self.u[0:self.N-2] = self.u[1:self.N-1]
        self.u[self.N-1] = 0


        return self.allLocations, self.costs, action
            
            
        
            
        