import sys
from simulation import SIMULATION

# this gets the second string in the interpreter after python3
directOrGUI = sys.argv[1] 

# create an object -- an instance of the SIMULATION class -- called simulation
simulation = SIMULATION(directOrGUI)
simulation.run()

simulation.Get_Fitness()

