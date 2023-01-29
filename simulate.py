import sys
from simulation import SIMULATION

# this gets the second string in the interpreter after python3
directOrGUI = sys.argv[1] 
solutionID = sys.argv[2]

# create an object -- an instance of the SIMULATION class -- called simulation
simulation = SIMULATION(directOrGUI, solutionID)
simulation.run()

simulation.Get_Fitness()

