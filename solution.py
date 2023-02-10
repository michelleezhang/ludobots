import os
import numpy
import pyrosim.pyrosim as pyrosim
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = numpy.array([
                numpy.array([numpy.random.rand() for i in range(c.numMotorNeurons)]) for j in range(c.numSensorNeurons)
        ])
        self.weights = (self.weights * 2) - 1
    
    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system('python3 simulate.py ' + directOrGUI + ' ' + str(self.myID) + ' 2&>1 &')

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists('fitness' + str(self.myID) + '.txt'):
            time.sleep(0.01)
        
        fitnessFile = open('fitness' + str(self.myID) + '.txt', 'r')
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system('rm fitness' + str(self.myID) + '.txt')
        
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[0, 0.2, 0.25], size=[15, 2.6, 0.5])
        pyrosim.End()

    def Create_Body(self):
        blockheight = 0.5
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1 + blockheight], size=[1, 1, 0.5])

        pyrosim.Send_Joint(name = "Torso_Shell1" , parent= "Torso" , child = "Shell1" , type = "revolute", position = [0, 0, 1.3], jointAxis = "0 0 1")
        pyrosim.Send_Cube(name="Shell1", pos=[0, 0, 0 + blockheight], size=[0.8, 0.6, 0.3])

        pyrosim.Send_Joint( name = "Shell1_Shell2" , parent= "Shell1" , child = "Shell2" , type = "revolute", position = [0, 0, 0.01], jointAxis = "0 0 1")
        pyrosim.Send_Cube(name="Shell2", pos=[0, 0, 0.25 + blockheight], size=[0.5, 0.4, 0.15])


        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0.4, -0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.3, blockheight], size=[0.2, 0.6, 0.2])

        pyrosim.Send_Joint( name = "Torso_BackLeg2" , parent= "Torso" , child = "BackLeg2" , type = "revolute", position = [-0.4, -0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg2", pos=[0, -0.3, blockheight], size=[0.2, 0.6, 0.2])






        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0.4, 0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.3, blockheight], size=[0.2, 0.6, 0.2])

        pyrosim.Send_Joint( name = "Torso_FrontLeg2" , parent= "Torso" , child = "FrontLeg2" , type = "revolute", position = [-0.4, 0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg2", pos=[0, 0.3, blockheight], size=[0.2, 0.6, 0.2])



        pyrosim.Send_Joint( name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [-0.5, 0.4, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.3, 0, blockheight], size=[0.6, 0.2, 0.2])

        pyrosim.Send_Joint( name = "Torso_LeftLeg2" , parent= "Torso" , child = "LeftLeg2" , type = "revolute", position = [-0.5, -0.4, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLeg2", pos=[-0.3, 0, blockheight], size=[0.6, 0.2, 0.2])

        pyrosim.Send_Joint( name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [0.5, 0.4, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.3, 0, blockheight], size=[0.6, 0.2, 0.2])

        pyrosim.Send_Joint( name = "Torso_RightLeg2" , parent= "Torso" , child = "RightLeg2" , type = "revolute", position = [0.5, -0.4, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLeg2", pos=[0.3, 0, blockheight], size=[0.6, 0.2, 0.2])






        pyrosim.Send_Joint( name = "FrontLeg_FrontLowerLeg" , parent= "FrontLeg" , child = "FrontLowerLeg" , type = "revolute", position = [0, 0.6, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.5 + blockheight], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint( name = "FrontLeg2_FrontLowerLeg2" , parent= "FrontLeg2" , child = "FrontLowerLeg2" , type = "revolute", position = [0, 0.6, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg2", pos=[0, 0, -0.5 + blockheight], size=[0.2, 0.2, 1])


        pyrosim.Send_Joint( name = "BackLeg_BackLowerLeg" , parent= "BackLeg" , child = "BackLowerLeg" , type = "revolute", position = [0, -0.6, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.5 + blockheight], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint( name = "BackLeg2_BackLowerLeg2" , parent= "BackLeg2" , child = "BackLowerLeg2" , type = "revolute", position = [0, -0.6, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg2", pos=[0, 0, -0.5 + blockheight], size=[0.2, 0.2, 1])


        # pyrosim.Send_Joint( name = "LeftLeg_LeftLowerLeg" , parent= "LeftLeg" , child = "LeftLowerLeg" , type = "revolute", position = [-0.6, 0, 0], jointAxis = "0 1 0")
        # pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5 + blockheight], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint( name = "LeftLeg2_LeftLowerLeg2" , parent= "LeftLeg2" , child = "LeftLowerLeg2" , type = "revolute", position = [-0.6, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg2", pos=[0, 0, -0.5 + blockheight], size=[0.2, 0.2, 1])


        pyrosim.Send_Joint( name = "RightLeg_RightLowerLeg" , parent= "RightLeg" , child = "RightLowerLeg" , type = "revolute", position = [0.6, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.5 + blockheight], size=[0.2, 0.2, 1])

        # pyrosim.Send_Joint( name = "RightLeg2_RightLowerLeg2" , parent= "RightLeg2" , child = "RightLowerLeg2" , type = "revolute", position = [0.6, 0, 0], jointAxis = "0 1 0")
        # pyrosim.Send_Cube(name="RightLowerLeg2", pos=[0, 0, -0.5 + blockheight], size=[0.2, 0.2, 1])


        pyrosim.End()


    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        linkNames = ['FrontLowerLeg', 
                      'FrontLowerLeg2', #'FrontLowerLeg3', 
                     'BackLowerLeg', 
                      'BackLowerLeg2', #'BackLowerLeg3', 
                     #'LeftLowerLeg', 
                      'LeftLowerLeg2', #'LeftLowerLeg3'
                     'RightLowerLeg',
                     #'RightLowerLeg2'
                    ] 

        jointNames = ['Torso_Shell1', 'Shell1_Shell2', 
                      'Torso_BackLeg', 
                       'Torso_BackLeg2', #'Torso_BackLeg3',
                      'Torso_FrontLeg', 
                       'Torso_FrontLeg2', #'Torso_FrontLeg3',
                      'Torso_LeftLeg',  
                       'Torso_LeftLeg2', #'Torso_LeftLeg3',
                      'Torso_RightLeg', 
                       'Torso_RightLeg2', #'Torso_RightLeg3',
                      'FrontLeg_FrontLowerLeg', 
                       'FrontLeg2_FrontLowerLeg2', #'FrontLeg3_FrontLowerLeg3', 
                      'BackLeg_BackLowerLeg', 
                       'BackLeg2_BackLowerLeg2', #'BackLeg3_BackLowerLeg3', 
                      #'LeftLeg_LeftLowerLeg', 
                       'LeftLeg2_LeftLowerLeg2', #'LeftLeg3_LeftLowerLeg3',
                      'RightLeg_RightLowerLeg',  
                      # 'RightLeg2_RightLowerLeg2',  #'RightLeg3_RightLowerLeg3'
                    ] 

        sensorcount = 0
        while sensorcount < len(linkNames):
            pyrosim.Send_Sensor_Neuron(name = sensorcount, linkName = linkNames[sensorcount])
            sensorcount += 1
        
        i =  0
        motorcount = sensorcount + 1
        while i < len(jointNames):
            pyrosim.Send_Motor_Neuron(name = motorcount, jointName = jointNames[i])
            motorcount += 1
            i += 1

        # generate a synapse
        for currentRow in range(c.numSensorNeurons):        
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + c.numSensorNeurons, weight = self.weights[currentRow][currentColumn])

        pyrosim.End()
    
    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)
        randomColumn = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randomRow, randomColumn] = random.random()  * 2 - 1

    def Set_ID(self, id):
        self.myID = id