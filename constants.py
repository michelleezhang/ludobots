import numpy as numpy
pi_four = numpy.pi / 4.0

num_iterations = 1000
time_step = 1/1000 #60

max_force = 100
amplitude = pi_four
frequency = 40
offset = 0

numberOfGenerations = 3 #10
populationSize = 5 # 10

numSensorNeurons = 6 # number of things in linkNames (in solution.py)
numMotorNeurons = 16 # number of things in jointNames (in solution.py)
motorJointRange = 0.2