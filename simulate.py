import pybullet as p
import pybullet_data
import time as time
import pyrosim.pyrosim as pyrosim
import numpy as numpy
#import random

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

amplitude_front = numpy.pi / 4.0
amplitude_back = numpy.pi / 4.0 

frequency_front = 3
frequency_back = 2

phaseOffset_front = 0
phaseOffset_back = numpy.pi / 4.0

# original: amp = numpy.pi / 4.0, freq = 1 or 10, off = 0 or numpy.pi / 4.0 

count = 1000
# initializing numpy vectors
backLegSensorValues = numpy.zeros(count)
frontLegSensorValues = numpy.zeros(count)

x = numpy.linspace(0, 2 * numpy.pi, count)
targetAngles_front = amplitude_front * numpy.sin(frequency_front * x + phaseOffset_front)
targetAngles_back = amplitude_back * numpy.sin(frequency_back * x + phaseOffset_back)
# x = numpy.sin(x)
#targetAngles = ((x - (-1)) / (1 - (-1)) ) * ((numpy.pi/4.0) - (-numpy.pi/4.0)) + (-numpy.pi/4.0)

numpy.save('data/targetAngles_back.npy', targetAngles_back)
numpy.save('data/targetAngles_front.npy', targetAngles_front)

for i in range(count):
    # "steps" (moves forward) the physics inside the world for a small amount of time
    p.stepSimulation()

    # storing sensor values
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    # simulate a motor that supplies force to one of the robot's joints.
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = "Torso_BackLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = targetAngles_back[i], #random.uniform(-math.pi/2.0, math.pi/2.0),
        maxForce = 50)
    
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = "Torso_FrontLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = targetAngles_front[i], #random.uniform(-math.pi/2.0, math.pi/2.0),
        maxForce = 50)

    # sleep() suspends execution for the given number of seconds
    time.sleep(1/260) #60

    #print(i)

numpy.save('data/backLegSensorValues.npy', backLegSensorValues)
numpy.save('data/frontLegSensorValues.npy', frontLegSensorValues)

p.disconnect()
print(backLegSensorValues)