import numpy as numpy
import constants as c
import pyrosim.pyrosim as pyrosim

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = numpy.zeros(c.num_iterations)
    
    def Get_Value(self, t):
        # storing sensor values
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
    
    def Save_Values(self):
        numpy.save('data/SensorValues.npy', self.values)


