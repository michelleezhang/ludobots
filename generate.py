import pyrosim.pyrosim as pyrosim
import random

# uses pyrosim to generate a link (aka object)
# stores in world.sdf file

def CreateWorld():
    # specifies to pyrosim the file where world info is stored
    pyrosim.Start_SDF("world.sdf")

    pyrosim.Send_Cube(name="Box", pos=[-2, 2, 0.5], size=[1, 1, 1])

    # close sdf file
    pyrosim.End()

def Generate_Body():
    # urdf files --- the Unified Robot Description Format --- are often used for describing a robot
    pyrosim.Start_URDF("body.urdf")

    length, width, height = 1, 1, 1

    # Only the first link in a robot --- the "root" link --- has an absolute position. 
    # Every other link has a position relative to its "upstream" joint.
    # Joints with no upstream joint have absolute positions. Every other joint has a position relative to its upstream joint.

    pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[length, width, height])

    pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0.5, 0, 1])
    pyrosim.Send_Cube(name="BackLeg", pos=[0.5, 0, -0.5], size=[length, width, height])

    pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [-0.5, 0, 1])
    pyrosim.Send_Cube(name="FrontLeg", pos=[-0.5, 0, -0.5], size=[length, width, height])

    pyrosim.End()

def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")

    # create a "sensor neuron" (receives values from sensors)
    # this one gets value from sensors in Torso
    pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")

    pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
    pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")

    pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
    pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

    # generate a synapse
    # this one connects neuron 0 to neuron 3 with a synaptic with weight 1.0.
    pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 3 , weight = -1.0 )
    pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 3 , weight = -1.0 )

    pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 4 , weight = -1.0 )
    pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 4 , weight = -1.0 )


    for i in range(0, 3):           # 0, 1, 2
        for j in range(3, 5):       #3, 4
            w = random.uniform(-1, 1)
            pyrosim.Send_Synapse( sourceNeuronName = i , targetNeuronName = j , weight = w )

    pyrosim.End()

CreateWorld()
Generate_Body()
Generate_Brain()

