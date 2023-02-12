import os
import numpy
import pyrosim.pyrosim as pyrosim
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID

        self.linkNames = []
        self.jointNames = []

        #self.weights = numpy.array([
        #         numpy.array([numpy.random.rand() for i in range(c.numMotorNeurons)]) for j in range(c.numSensorNeurons)
        # ])
        # self.weights = (self.weights * 2) - 1
    
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
        pyrosim.Send_Cube(name="Box", pos=[-5, 0, 0.25], size=[1, 1, 0.5])
        pyrosim.End()

    def Create_Body(self):
        self.linkNames = []
        self.jointNames = []

        pyrosim.Start_URDF("body.urdf")

        # first link and first joint are absolute
        # after that, relative to prev joint 

        # generate all z positions randomly in a list
        num_links = random.randint(3, 9)
        linksize_z = numpy.array([random.uniform(0.5, 1.5) for j in range(num_links + 1)])

        # create root cube
        prev_linksize_x = random.uniform(0.5, 1.5)
        prev_linksize_y = random.uniform(0.5, 1.5)

        pyrosim.Send_Cube(name = "Link0", pos = [0, 0, linksize_z[0] / 2], size = [prev_linksize_x, prev_linksize_y, linksize_z[0]], sensor_boolean=False)

        for i in range(1, num_links):  
            linksize_x = random.uniform(0.5, 1.5)
            linksize_y = random.uniform(0.5, 1.5)

            parent_name = "Link" +  str(i - 1)
            child_name = "Link" +  str(i)

            if i == 1:
                jointposn_y = prev_linksize_y / 2
                jointposn_z = numpy.max(linksize_z) / 2
            else:
                jointposn_y = prev_linksize_y
                jointposn_z = 0
            
            prev_linksize_y = linksize_y

            # sends the previous joint, and then the next cube
            # e.g. joint beweeen 1 and 2, then cube 2
            pyrosim.Send_Joint(name = parent_name + "_" + child_name, parent = parent_name, child = child_name, type = "revolute", position = [0, jointposn_y, jointposn_z], jointAxis = "1 0 0")
            
            sensor_boolean = bool(random.getrandbits(1))

            if sensor_boolean:
                self.linkNames.append(child_name)
                self.jointNames.append(parent_name + "_" + child_name)
                print('Link : ', self.linkNames, ' an jonts ', self.jointNames)

            pyrosim.Send_Cube(name = child_name, pos = [0, linksize_y / 2, 0], size = [linksize_x, linksize_y, linksize_z[i]], sensor_boolean=sensor_boolean)
        
            # random sensor placement along the chain

        pyrosim.End()


    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        sensorcount = 0 
        while sensorcount < len(self.linkNames):
            pyrosim.Send_Sensor_Neuron(name = sensorcount, linkName = self.linkNames[sensorcount])
            sensorcount += 1
        
        i =  0 
        motorcount = sensorcount + 1
        while i < len(self.jointNames):
            pyrosim.Send_Motor_Neuron(name = motorcount, jointName = self.jointNames[i])
            motorcount += 1
            i += 1

        # generate a synapse
        for currentRow in range(len(self.linkNames)):        
            for currentColumn in range(len(self.jointNames)):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + len(self.linkNames), weight = 1.5)



        # linkNames = ['Link1', 'Link2'
        #             ] 

        # jointNames = ['Link0_Link1', 'Link1_Link2'
        #             ] 

        # sensorcount = 0
        # while sensorcount < len(linkNames):
        #     pyrosim.Send_Sensor_Neuron(name = sensorcount, linkName = linkNames[sensorcount])
        #     sensorcount += 1
        
        # i =  0
        # motorcount = sensorcount + 1
        # while i < len(jointNames):
        #     pyrosim.Send_Motor_Neuron(name = motorcount, jointName = jointNames[i])
        #     motorcount += 1
        #     i += 1

        # # generate a synapse
        # for currentRow in range(c.numSensorNeurons):        
        #     for currentColumn in range(c.numMotorNeurons):
        #         pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + c.numSensorNeurons, weight = self.weights[currentRow][currentColumn])

        pyrosim.End()
    
    def Mutate(self):
        pass
        # randomRow = random.randint(0, c.numSensorNeurons - 1)
        # randomColumn = random.randint(0, c.numMotorNeurons - 1)
        #self.weights[randomRow, randomColumn] = random.random()  * 2 - 1

    def Set_ID(self, id):
        self.myID = id