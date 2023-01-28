import os
import numpy
import pyrosim.pyrosim as pyrosim
import random
# import pybullet as p

class SOLUTION:
    def __init__(self):
        self.weights = numpy.array(
            [[numpy.random.rand(), numpy.random.rand()],
            [numpy.random.rand(), numpy.random.rand()],
            [numpy.random.rand(), numpy.random.rand()]]
        )
        self.weights = (self.weights * 2) - 1
    
    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system('python3 simulate.py ' + directOrGUI)
        fitnessFile = open('fitness.txt', 'r')
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-2, 2, 0.5], size=[1, 1, 1])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        length, width, height = 1, 1, 1
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[length, width, height])

        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0.5, 0, 1])
        pyrosim.Send_Cube(name="BackLeg", pos=[0.5, 0, -0.5], size=[length, width, height])

        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [-0.5, 0, 1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[-0.5, 0, -0.5], size=[length, width, height])

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

        # generate a synapse
        pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 3 , weight = -1.0 )
        pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 3 , weight = -1.0 )

        pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 4 , weight = -1.0 )
        pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 4 , weight = -1.0 )

        for currentRow in range(3):        
            for currentColumn in range(2):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + 3, weight = self.weights[currentRow][currentColumn])

        pyrosim.End()
    
    def Mutate(self):
        randomRow = random.randint(0, 2)
        randomColumn = random.randint(0, 1)
        self.weights[randomRow][randomColumn] = random.random() * 2 - 1
