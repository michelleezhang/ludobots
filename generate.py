import pyrosim.pyrosim as pyrosim

# uses pyrosim to generate a link (aka object)
# stores in world.sdf file

def CreateWorld():
    # spcifies to pyrosim the file where world info is stored
    pyrosim.Start_SDF("world.sdf")

    pyrosim.Send_Cube(name="Box", pos=[-2, 2, 0.5], size=[1, 1, 1])

    # close sdf file
    pyrosim.End()

def CreateRobot():
    length, width, height = 1, 1, 1
    # z = 0.5
    x, y, z = 0, 0, 1.5
    # urdf files --- the Unified Robot Description Format --- are often used for describing a robot
    pyrosim.Start_URDF("body.urdf")

    # Only the first link in a robot --- the "root" link --- has an absolute position. 
    # Every other link has a position relative to its "upstream" joint.
    # Joints with no upstream joint have absolute positions. Every other joint has a position relative to its upstream joint.

    pyrosim.Send_Cube(name="Torso", pos=[x, y, z], size=[length, width, height])

    pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0.5, 0, 1])
    pyrosim.Send_Cube(name="BackLeg", pos=[0.5, 0, -0.5], size=[length, width, height])

    pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [-0.5, 0, 1])
    pyrosim.Send_Cube(name="FrontLeg", pos=[-0.5, 0, -0.5], size=[length, width, height])

    # # cube arch
    # pyrosim.Send_Cube(name="Link0", pos=[x, y, z], size=[length, width, height])
    # # adds a join between Torso and Leg
    # pyrosim.Send_Joint( name = "Link0_Link1" , parent= "Link0" , child = "Link1" , type = "revolute", position = [0, 0, 1])
    # pyrosim.Send_Cube(name="Link1", pos=[0, 0, 0.5], size=[length, width, height])
    # # second link and joint
    # pyrosim.Send_Joint( name = "Link1_Link2" , parent= "Link1" , child = "Link2" , type = "revolute", position = [0, 0, 1])
    # pyrosim.Send_Cube(name="Link2", pos=[0, 0, 0.5], size=[length, width, height])
    # # third link and joint
    # pyrosim.Send_Joint( name = "Link2_Link3" , parent= "Link2" , child = "Link3" , type = "revolute", position = [0, 0.5, 0.5])
    # pyrosim.Send_Cube(name="Link3", pos=[0, 0.5, 0], size=[length, width, height])
    # # fourth link and joint
    # pyrosim.Send_Joint( name = "Link3_Link4" , parent= "Link3" , child = "Link4" , type = "revolute", position = [0, 1, 0])
    # pyrosim.Send_Cube(name="Link4", pos=[0, 0.5, 0], size=[length, width, height])
    # # fifth link and joint
    # pyrosim.Send_Joint( name = "Link4_Link5" , parent= "Link4" , child = "Link5" , type = "revolute", position = [0, 0.5, -0.5])
    # pyrosim.Send_Cube(name="Link5", pos=[0, 0, -0.5], size=[length, width, height])
    # # sixth link and joint
    # pyrosim.Send_Joint( name = "Link5_Link6" , parent= "Link5" , child = "Link6" , type = "revolute", position = [0, 0, -1])
    # pyrosim.Send_Cube(name="Link6", pos=[0, 0, -0.5], size=[length, width, height])

    pyrosim.End()

CreateWorld()
CreateRobot()