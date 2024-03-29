import os
import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID

        # create seed
        self.seed = c.seed
        random.seed(self.seed)

        self.linkNames = []
        self.jointNames = []

        self.minsize = 0.5
        self.maxsize = 1.1
        self.num_branchlinks = [random.randint(3, 6), random.randint(0, 2), random.randint(0, 2), random.randint(0, 2)]
        # y, x, -x, z

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

        # branching helper function
        def create_branches(direction, num_links, spine_name, linksize_x, linksize_y, linksize_z):
                linksize = [random.uniform(self.minsize, self.maxsize), random.uniform(self.minsize, self.maxsize), random.uniform(self.minsize, self.maxsize)]
                prev_linksize = linksize 
                
                if direction == "+x":
                    link_name_string = "XLink"
                    joint_posn = [linksize_x / 2, linksize_y / 2, 0]
                    joint_axis = "1 0 0"   
                    link_posn = [linksize[0] / 2, 0, 0]
                elif direction == "-x":
                    link_name_string = "MinXLink"
                    joint_posn = [-0.5 * linksize_x, linksize_y / 2, 0]
                    joint_axis = "1 0 0"
                    link_posn = [-0.5 * linksize[0], 0, 0]
                elif direction == "+z":
                    link_name_string = "ZLink"
                    joint_posn = [0, linksize_y / 2, linksize_z / 2]
                    joint_axis = "0 0 1"
                    link_posn = [0, 0, linksize[2] / 2]
                    
                for j in range(num_links):
                    if j == 0: # first branch joint
                        parent_name = spine_name

                        y_bound = linksize_y # for + and -x
                        x_bound = linksize_x
                    else:
                        if direction == "+x":
                            joint_posn = [prev_linksize[0], 0, 0]
                        elif direction == "-x":
                            joint_posn = [-1 * prev_linksize[0], 0, 0]
                        elif direction == "+z":
                            joint_posn = [0, 0, prev_linksize[2]]

                        parent_name = spine_name + link_name_string + str(j - 1)

                        y_bound = prev_linksize[1]
                        x_bound = prev_linksize[0]

                    child_name = spine_name + link_name_string + str(j)

                    pyrosim.Send_Joint(name = parent_name + "_" + child_name, 
                                    parent = parent_name, child = child_name, 
                                    type = "revolute", 
                                    position = [joint_posn[0], joint_posn[1], joint_posn[2]], 
                                    jointAxis = joint_axis)

                    sensor_boolean = bool(random.getrandbits(1))

                    if sensor_boolean:
                        self.linkNames.append(child_name)
                        self.jointNames.append(parent_name + "_" + child_name)

                    if direction == "+z":
                        linksize[0] = min(linksize[0], x_bound)

                    pyrosim.Send_Cube(name = child_name, 
                                  pos = [link_posn[0], link_posn[1], link_posn[2]], 
                                  size = [linksize[0], min(linksize[1], y_bound), linksize[2]], # if you don't want to bound, just do x_linksize_y for the y size
                                  sensor_boolean = sensor_boolean)
                    
        # main program
        pyrosim.Start_URDF(f"body{self.myID}.urdf")

        # first link and first joint are absolute
        # after that, relative to prev joint 

        # generate all z positions randomly in a list
        num_links = self.num_branchlinks[0]
        linksize_z = np.array([random.uniform(self.minsize, self.maxsize) for j in range(num_links + 1)])

        # create root cube
        prev_linksize_x = random.uniform(self.minsize, self.maxsize)
        prev_linksize_y = random.uniform(self.minsize, self.maxsize)

        pyrosim.Send_Cube(name = "Link0", pos = [0, 0, linksize_z[0] / 2], size = [prev_linksize_x, prev_linksize_y, linksize_z[0]], sensor_boolean=False)

        for i in range(1, num_links):   
            linksize_x = random.uniform(self.minsize, self.maxsize)
            linksize_y = random.uniform(self.minsize, self.maxsize)

            parent_name = "Link" +  str(i - 1)
            child_name = "Link" +  str(i)

            if i == 1:
                jointposn_y = prev_linksize_y / 2
                jointposn_z = np.max(linksize_z) / 2
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

            # create branches!
            create_branches("+x", self.num_branchlinks[1], child_name, linksize_x, linksize_y, linksize_z[i])
            create_branches("-x", self.num_branchlinks[2], child_name, linksize_x, linksize_y, linksize_z[i])
            create_branches("+z", self.num_branchlinks[3], child_name, linksize_x, linksize_y, linksize_z[i])

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

        self.weights = np.array([
                np.array([np.random.rand() for i in range(len(self.jointNames))]) for j in range(len(self.linkNames))
        ])
        self.weights = (self.weights * 2) - 1

        # generate a synapse
        for currentRow in range(len(self.linkNames)):        
            for currentColumn in range(len(self.jointNames)):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + len(self.linkNames), weight = self.weights[currentRow][currentColumn])

        pyrosim.End()
    
    def Mutate(self): 
        check = random.randint(1, 10)

        if check == 1:
            # smaller blocks
            self.minsize *= 0.5
            self.maxsize *= 0.7
        elif check == 2:
            # bigger blocks
            self.minsize *= 1.2
            self.maxsize *= 1.5
        elif check == 3:
            # more x
            self.num_branchlinks[1] += 1
            self.num_branchlinks[2] += 1
        elif check == 4:
            # less x
            self.num_branchlinks[1] = max(0, self.num_branchlinks[1] - 1)
            self.num_branchlinks[2] = max(0, self.num_branchlinks[2] - 1)
            if self.num_branchlinks[1] == 0 and self.num_branchlinks[2] == 0:
                 self.minsize *= 0.7
        elif check == 5:
            # more y
            self.num_branchlinks[0] += 1
        elif check == 6:
            # less y
            self.num_branchlinks[0] = max(0, self.num_branchlinks[0] - 1)
            if self.num_branchlinks[0] == 0:
                 self.minsize *= 0.7
        elif check == 7:
            # more z
            self.num_branchlinks[3] += 1
        elif check == 8:
             # less z
             self.num_branchlinks[3] = max(0, self.num_branchlinks[3] - 1)
             if self.num_branchlinks[3] == 0:
                 self.minsize *= 0.7
        else:
            if (len(self.linkNames) - 1) < 0 or (len(self.jointNames) - 1) < 0:
                pass
            randomRow = random.randint(0, len(self.linkNames) - 1)
            randomColumn = random.randint(0, len(self.jointNames) - 1)
            self.weights[randomRow, randomColumn] = random.random() * 2 - 1

        self.Create_Body()
        self.Create_Brain()


    def Set_ID(self, id):
        self.myID = id