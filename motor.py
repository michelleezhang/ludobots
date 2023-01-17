import numpy as numpy
import constants as c
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()
    
    def Prepare_To_Act(self):
        #self.values = numpy.zeros(c.num_iterations)
        self.amplitude = c.amplitude
        self.frequency = c.frequency
        self.offset = c.offset

        # one motor oscillates at half the frequency of the other
        if self.jointName == "Torso_BackLeg":
            self.frequency = self.frequency * 0.5
    
        x = numpy.linspace(0, 2 * numpy.pi, c.num_iterations)
        self.motorValues = self.amplitude * numpy.sin(self.frequency * x + self.offset)

    def Set_Value(self, t, robot, id):
        # # simulate a motor that supplies force to one of the robot's joints.
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = id,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = self.motorValues[t], 
            maxForce = c.max_force)
    
    def Save_Values(self):
        numpy.save('data/MotorValues.npy', self.motorValues)