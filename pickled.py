import sys
from simulation import SIMULATION

# this gets the second string in the interpreter after python3
solutionID = sys.argv[1]

# create an object -- an instance of the SIMULATION class -- called simulation
simulation = SIMULATION('GUI', solutionID, "best_robots/")
simulation.run()

simulation.Get_Fitness()