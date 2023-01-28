from world import WORLD
from robot import ROBOT

import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy
import constants as c
import time as time

class SIMULATION:
    def __init__(self, directOrGUI):
        # p.DIRECT gives "blind mode", p.GUI shows the animation
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT) 
        else:
            self.physicsClient = p.connect(p.GUI) 

        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        # add gravity
        p.setGravity(0, 0, -9.8)

        self.world = WORLD()
        self.robot = ROBOT()

    def run(self):
        for i in range(c.num_iterations):
            # "steps" (moves forward) the physics inside the world for a small amount of time
            p.stepSimulation()

            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i, self.robot)

            # sleep() suspends execution for the given number of seconds
            time.sleep(c.time_step)

            #print(i)

    def __del__(self):
        p.disconnect()
    
    def Get_Fitness(self):
        self.robot.Get_Fitness()

        
        
        

        