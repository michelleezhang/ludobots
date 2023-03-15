import os
from parallelHillclimber import PARALLEL_HILL_CLIMBER

phc = PARALLEL_HILL_CLIMBER()

os.system('rm brain*.nndf')
os.system('rm body*.urdf')
os.system('rm fitness*.txt')

phc.Evolve()
phc.Show_Best()