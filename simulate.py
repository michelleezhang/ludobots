import pybullet as p
import time as time

# This creates an object, physicsClient, which handles the physics, 
# and draws the results to a Graphical User Interface (GUI).

physicsClient = p.connect(p.GUI)

# tells pybullet to read in the world described in box.sdf
p.loadSDF("box.sdf")

for i in range(1000):
    # "steps" (moves forward) the physics inside the world for a small amount of time
    p.stepSimulation()

    # sleep() suspends execution for the given number of seconds
    time.sleep(1/60)

    print(i)

p.disconnect()
