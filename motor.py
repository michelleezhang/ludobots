import numpy as numpy
import constants as c
import pybullet as p
import pyrosim.pyrosim as pyrosim

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName

    def Set_Value(self, desiredAngle, robot, id):
        # # simulate a motor that supplies force to one of the robot's joints.
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = id,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = desiredAngle,
            maxForce = c.max_force)