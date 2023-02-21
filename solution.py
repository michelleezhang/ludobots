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
        num_links = random.randint(3, 6)
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

            # tbh you can do +-x and then z

            pyrosim.Send_Cube(name = child_name, pos = [0, linksize_y / 2, 0], size = [linksize_x, linksize_y, linksize_z[i]], sensor_boolean=sensor_boolean)


            num_x_links = random.randint(0, 3)

            for j in range(num_x_links):
                if j == 0: # first branch joint
                    parentx_name = child_name

                    x_joint_xposn = linksize_x / 2
                    x_joint_yposn = linksize_y / 2
                    y_bound = linksize_y
                else:
                    parentx_name = child_name + "XLink" + str(j - 1)

                    x_joint_xposn = x_prev_x # size of last branch cube
                    x_joint_yposn = 0
                    y_bound = x_prev_y

                childx_name = child_name + "XLink" + str(j)

                pyrosim.Send_Joint(name = parentx_name + "_" + childx_name, 
                                parent = parentx_name, child = childx_name, 
                                type = "revolute", 
                                position = [x_joint_xposn, x_joint_yposn, 0], 
                                jointAxis = "1 0 0")

                sensor_boolean = bool(random.getrandbits(1))

                if sensor_boolean:
                    self.linkNames.append(childx_name)
                    self.jointNames.append(parentx_name + "_" + childx_name)

                x_linksize_x = random.uniform(0.5, 1)
                x_linksize_y = random.uniform(0.5, 1)
                x_linksize_z = random.uniform(0.5, 1)
                x_prev_x = x_linksize_x
                x_prev_y = x_linksize_y

                pyrosim.Send_Cube(name = childx_name, 
                                  pos = [x_linksize_x / 2, 0, 0], 
                                  size = [x_linksize_x, min(x_linksize_y, y_bound), x_linksize_z], # if you don't want to bound, just do x_linksize_y for the y size
                                  sensor_boolean=sensor_boolean) 
            


            num_minx_links = random.randint(0, 2)

            for m in range(num_minx_links):
                if m == 0: # first branch joint
                    parentminx_name = child_name

                    minx_joint_xposn = -0.5 * linksize_x
                    minx_joint_yposn = linksize_y / 2
                    minx_y_bound = linksize_y
                else:
                    parentminx_name = child_name + "MinXLink" + str(m - 1)

                    minx_joint_xposn = -1 * minx_prev_x # size of last branch cube
                    minx_joint_yposn = 0
                    minx_y_bound = minx_prev_y

                childminx_name = child_name + "MinXLink" + str(m)

                pyrosim.Send_Joint(name = parentminx_name + "_" + childminx_name, 
                                parent = parentminx_name, child = childminx_name, 
                                type = "revolute", 
                                position = [minx_joint_xposn, minx_joint_yposn, 0], 
                                jointAxis = "1 0 0")

                sensor_boolean = bool(random.getrandbits(1))

                if sensor_boolean:
                    self.linkNames.append(childminx_name)
                    self.jointNames.append(parentminx_name + "_" + childminx_name)

                minx_linksize_x = random.uniform(0.5, 1)
                minx_linksize_y = random.uniform(0.5, 1)
                minx_linksize_z = random.uniform(0.5, 1)
                minx_prev_x = minx_linksize_x
                minx_prev_y = minx_linksize_y

                pyrosim.Send_Cube(name = childminx_name, 
                                  pos = [-0.5 * minx_linksize_x, 0, 0], 
                                  size = [minx_linksize_x, min(minx_linksize_y, minx_y_bound), minx_linksize_z], # if you don't want to bound, just do x_linksize_y for the y size
                                  sensor_boolean=sensor_boolean) 


            num_z_links = random.randint(0, 3)

            for k in range(num_z_links):
                if k == 0: # first branch joint
                    parentz_name = child_name
                    z_joint_zposn = linksize_z / 2 
                    z_joint_xposn = linksize_x / 2 
                    z_y_bound = linksize_y
                    z_x_bound = linksize_x

                else:
                    parentz_name = child_name + "ZLink" + str(k - 1)
                    z_joint_zposn = z_prev_z
                    z_joint_xposn = 0
                    z_y_bound = z_prev_y
                    z_x_bound = z_prev_x
                
                childz_name = child_name + "ZLink" + str(k)

                pyrosim.Send_Joint(name = parentz_name + "_" + childz_name, 
                                parent = parentz_name, child = childz_name, 
                                type = "revolute", 
                                position = [z_joint_xposn, 0, z_joint_zposn], 
                                jointAxis = "0 0 1")

                sensor_boolean = bool(random.getrandbits(1))

                if sensor_boolean:
                    self.linkNames.append(childz_name)
                    self.jointNames.append(parentz_name + "_" + childz_name)

                z_linksize_x = random.uniform(0.5, 1)
                z_linksize_y = random.uniform(0.5, 1)
                z_linksize_z = random.uniform(0.5, 1)
                z_prev_x = z_linksize_x
                z_prev_y = z_linksize_y
                z_prev_z = z_linksize_z

                pyrosim.Send_Cube(name = childz_name, 
                                  pos = [0, 0, z_linksize_z / 2], #/ 2], 
                                  size = [min(z_x_bound, z_linksize_x), min(z_y_bound, z_linksize_y), z_linksize_z], # if you don't want to bound, just do x_linksize_y for the y size
                                  sensor_boolean = sensor_boolean)
                


            

                
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
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + len(self.linkNames), weight = 1.0)

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