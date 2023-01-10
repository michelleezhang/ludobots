import pyrosim.pyrosim as pyrosim

# uses pyrosim to generate a link (aka object)
# stores in world.sdf file

# spcifies to pyrosim the file where world info is stored
pyrosim.Start_SDF("box.sdf")

# store a box with initial 3D posn and dimensions in box.sdf
pyrosim.Send_Cube(name="Box", pos=[0, 0, 0.5], size=[1, 1, 1])

# close sdf file
pyrosim.End()