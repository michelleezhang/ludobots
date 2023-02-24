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




        def create_branches(direction, num_links, linksize_x, linksize_y, linksize_z):
                if direction == "+x":
                    link_name_string = "XLink"
                    joint_posn = [linksize_x / 2, linksize_y / 2, 0]
                    joint_axis = "1 0 0"   
                elif direction == "-x":
                    link_name_string = "MinXLink"
                    joint_posn = [-0.5 * linksize_x, linksize_y / 2, 0]
                    joint_axis = "1 0 0"
                elif direction == "+z":
                    link_name_string = "ZLink"
                    joint_posn = [0, linksize_y / 2, linksize_z / 2]
                    joint_axis = "0 0 1"
                    
                for j in range(num_links):
                    if j == 0: # first branch joint
                        parentx_name = child_name

                        y_bound = linksize_y # for + and -x
                        x_bound = linksize_x

                    else:
                        if direction == "+x":
                            joint_posn = [prev_x, 0, 0]
                        elif direction == "-x":
                            joint_posn = [-1 * prev_x, 0, 0]
                        elif direction == "+z":
                            joint_posn = [0, 0, prev_z]

                        parentx_name = child_name + link_name_string + str(j - 1)

                        y_bound = prev_y
                        x_bound = prev_x

                    childx_name = child_name + link_name_string + str(j)

                    pyrosim.Send_Joint(name = parentx_name + "_" + childx_name, 
                                    parent = parentx_name, child = childx_name, 
                                    type = "revolute", 
                                    position = [joint_posn[0], joint_posn[1], joint_posn[2]], 
                                    jointAxis = joint_axis)

                    sensor_boolean = bool(random.getrandbits(1))

                    if sensor_boolean:
                        self.linkNames.append(childx_name)
                        self.jointNames.append(parentx_name + "_" + childx_name)

                    linksize_x = random.uniform(0.5, 1)
                    linksize_y = random.uniform(0.5, 1)
                    linksize_z = random.uniform(0.5, 1)

                    prev_x = linksize_x
                    prev_y = linksize_y
                    prev_z = linksize_z

                    if direction == "+x":
                        link_posn = [linksize_x / 2, 0, 0]
                        linksize_y = min(linksize_y, y_bound)
                    elif direction == "-x":
                        link_posn = [-0.5 * linksize_x, 0, 0]
                        linksize_y = min(linksize_y, y_bound)
                    elif direction == "+z":
                        link_posn = [0, 0, linksize_z / 2]
                        linksize_x = min(linksize_x, x_bound)
                        linksize_y = min(linksize_y, y_bound)


                    pyrosim.Send_Cube(name = childx_name, 
                                  pos = [link_posn[0], link_posn[1], link_posn[2]], 
                                  size = [linksize_x, linksize_y, linksize_z], # if you don't want to bound, just do x_linksize_y for the y size
                                  sensor_boolean=sensor_boolean)


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

            pyrosim.Send_Cube(name = child_name, pos = [0, linksize_y / 2, 0], size = [linksize_x, linksize_y, linksize_z[i]], sensor_boolean=sensor_boolean)
 

            num_x_links = random.randint(0, 3)
            num_minx_links = random.randint(0, 3)
            num_z_links = random.randint(0, 2)
            
            create_branches("+x", num_x_links, linksize_x, linksize_y, linksize_z[i])
            create_branches("-x", num_minx_links, linksize_x, linksize_y, linksize_z[i])
            create_branches("+z", num_z_links, linksize_x, linksize_y, linksize_z[i])
                
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