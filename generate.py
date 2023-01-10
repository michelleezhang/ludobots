import pyrosim.pyrosim as pyrosim

# uses pyrosim to generate a link (aka object)
# stores in world.sdf file

# spcifies to pyrosim the file where world info is stored
pyrosim.Start_SDF("boxes.sdf")

x, y, z = 0, 0, 0.5

for a in range(5):
    for b in range(5):
        length, width, height = 1, 1, 1

        # store a box with initial 3D posn and dimensions in box.sdf
        for i in range(10):
            pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])
            length, width, height = length * 0.9, width * 0.9, height * 0.9
            z += height
        
        x += 1
        z = 0.5
    x = 0
    y += 1

# close sdf file
pyrosim.End()