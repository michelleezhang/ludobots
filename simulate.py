import pybullet as p
import pybullet_data
import time as time
import pyrosim.pyrosim as pyrosim
import numpy as numpy

# This creates an object, physicsClient, which handles the physics, 
# and draws the results to a Graphical User Interface (GUI).

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# add gravity
p.setGravity(0,0,-9.8)

# add a floor
planeId = p.loadURDF("plane.urdf")
# body
robotId = p.loadURDF("body.urdf")

# tells pybullet to read in the world described in box.sdf
p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)

# initializing numpy vectors
backLegSensorValues = numpy.zeros(100)
frontLegSensorValues = numpy.zeros(100)

for i in range(100):
    # "steps" (moves forward) the physics inside the world for a small amount of time
    p.stepSimulation()

    # storing sensor values
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    # sleep() suspends execution for the given number of seconds
    time.sleep(1/60)

    #print(i)

numpy.save('data/backLegSensorValues.npy', backLegSensorValues)
numpy.save('data/frontLegSensorValues.npy', frontLegSensorValues)

p.disconnect()
print(backLegSensorValues)