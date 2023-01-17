import numpy as numpy
import constants as c
import pyrosim.pyrosim as pyrosim

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName

        self.values = numpy.zeros(c.num_iterations)
        # print(self.values)
    
    def Get_Value(self, t):
        # storing sensor values
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

        if t == c.num_iterations - 1:
            print(self.values)
    
    def Save_Values(self):
        numpy.save('data/SensorValues.npy', self.values)


