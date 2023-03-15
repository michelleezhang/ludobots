import numpy as np
import random

seed = 1

pi_four = np.pi / 4.0

num_iterations = 1000
time_step = 1/100 # 1/200

max_force = 200
amplitude = pi_four
frequency = 10
offset = np.pi / 8.0

numberOfGenerations = 1 #500
populationSize = 1 # 10

# numSensorNeurons = 4 # number of things in linkNames (in solution.py)
# numMotorNeurons = 2 # number of things in jointNames (in solution.py)
motorJointRange = 0.3