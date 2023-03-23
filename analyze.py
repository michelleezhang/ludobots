import numpy as numpy
import matplotlib.pyplot as plt
from parallelHillclimber import PARALLEL_HILL_CLIMBER
import random 

for i in range(10):
    random.seed(i + 1) # picks one set of random numbers
    phc = PARALLEL_HILL_CLIMBER()
    fitnessArray = phc.Evolve()

    plt.plot(fitnessArray, label = 'Seed ' + str(i + 1))

plt.xlabel('Generation')
plt.ylabel('Max fitness')
plt.show()
