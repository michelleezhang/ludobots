import numpy as numpy
pi_four = numpy.pi / 4.0

num_iterations = 5000
time_step = 1/300 #60

max_force = 200
amplitude = pi_four
frequency = 10
offset = numpy.pi / 8.0

numberOfGenerations = 1 #10
populationSize = 1 # 10

numSensorNeurons = 2 # number of things in linkNames (in solution.py)
numMotorNeurons = 2 # number of things in jointNames (in solution.py)
motorJointRange = 0.3