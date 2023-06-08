import math

class Entity:
    def __init__(self,world):
        self.world = world

        self.position = [0,80,0]
        self.rotation = [-math.tau / 4,0]

        self.velocity = [0,0,0]

        self.width = 0.6
        self.height = 1.8
    
    def update(self,delta_time):
        self.position = [x + v * delta_time for x,v in zip(self.position,self.velocity)]
        self.velocity = [0,0,0]