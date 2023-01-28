import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim

from sensor import SENSOR
from motor import MOTOR

from pyrosim.neuralNetwork import NEURAL_NETWORK

class ROBOT:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)

        self.Prepare_To_Sense()
        self.Prepare_To_Act() #???

        # creates a neural network (self.nn), and adds any neurons and synapses to it from brain.nndf.
        self.nn = NEURAL_NETWORK("brain.nndf")
    
    def Prepare_To_Sense(self):
        self.sensors = {}

        # linkNamesToIndices is a dictionary in pyrosim that gives name of every link in body.urdf
        for linkName in pyrosim.linkNamesToIndices:

            # creates a SENSOR instance, stored as an entry in the self.sensors dictionary by name
            self.sensors[linkName] = SENSOR(linkName)
    
    def Sense(self, t):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(t)
        
    def Prepare_To_Act(self):
        self.motors = {} # ??

        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
    
    def Act(self, t, robot):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)

                motor = self.motors[jointName]
                motor.Set_Value(desiredAngle, robot, self.robotId)
        
    def Think(self):
        self.nn.Update()
        #self.nn.Print()

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotId, 0)
            # first arg is the unique ID of a body in the simulation (return value of loadURDF).
            # second arg is the link we want -- 0  means the first link

        positionOfLinkZero = stateOfLinkZero[0]

        xCoordinateOfLinkZero = positionOfLinkZero[0]

        # write xcoord to fitness.txt
        f = open('fitness.txt', 'w')
        f.write(str(xCoordinateOfLinkZero))
        f.close()

