import numpy as numpy
import matplotlib.pyplot as plt
import os
from parallelHillclimber import PARALLEL_HILL_CLIMBER
import constants as c
import random 

for i in range(10):
    random.seed(i + 1) # picks one set of random numbers
    phc = PARALLEL_HILL_CLIMBER()
    fitnessArray = phc.Evolve()

    # for j in range(len(fitnessArray)):
    #     os.system(f"cp body{j}.urdf best_robots/body{c.seed}_{j}.urdf")
    #     os.system(f"cp brain{j}.nndf creatures/brain{c.seed}_{j}.nndf")

    # input("Press Enter to Continue")
    # phc.Show_Best()
    plt.plot(fitnessArray, label = 'Seed ' + str(i + 1))
    # print('CURRENT: ', i)

plt.xlabel('Generation')
plt.ylabel('Max fitness')
plt.show()
