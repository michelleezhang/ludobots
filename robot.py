import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim

from sensor import SENSOR
from motor import MOTOR

class ROBOT:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)

        self.Prepare_To_Sense()
        self.Prepare_To_Act() #???
    
    def Prepare_To_Sense(self):
        self.sensors = {}

        # linkNamesToIndices is a dictionary in pyrosim that gives name of every link in body.urdf
        for linkName in pyrosim.linkNamesToIndices:

            # creates a SENSOR instance, stored as an entry in the self.sensors dictionary by name
            self.sensors[linkName] = SENSOR(linkName)
            #print(linkName)
    
    def Sense(self, t):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(t)
        
    def Prepare_To_Act(self):
        self.motors = {} # ??

        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
    
    def Act(self, t, robot):
        for motor in self.motors:
            self.motors[motor].Set_Value(t, robot, self.robotId)

