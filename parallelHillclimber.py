from solution import SOLUTION
import constants as c
import copy
import os
import numpy as np

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system('rm brain*.nndf')
        os.system('rm body*.urdf')
        os.system('rm fitness*.txt')

        self.parents = {}
        self.nextAvailableID = 0

        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        
        self.fitnessArray = []
        self.currGen = 0

        
    def Evolve(self):
        self.Evaluate(self.parents)

        for currentGeneration in range(c.numberOfGenerations):
            self.currGen = currentGeneration
            self.Evolve_For_One_Generation()

        return self.fitnessArray
    
        # save the best fitness at each generation 
        # after the ith cycle of evaluation, iterate over all parents to find the best fitness, 
        # and then store this value at the ith position of a one-dimensional array

        
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}

        for i in self.parents: #range(len(self.parents)):
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
    
    def Mutate(self):
        for i in self.children: #range(len(self.children)):
            self.children[i].Mutate()

    def Select(self):
        curr_gen_fitnessArray = np.zeros((len(self.parents)))

        #jumping
        for i in self.parents: #range(len(self.parents)):
            if self.parents[i].fitness < self.children[i].fitness:
                self.parents[i] = self.children[i]
            
            curr_gen_fitnessArray = np.append(curr_gen_fitnessArray, self.parents[i].fitness)
        
        # the values of curr_gen_fitnessArray are actually the max fitness values of each gen
        self.fitnessArray.append(np.max(curr_gen_fitnessArray))

        
    def Print(self):
        print('\n')
        for key in self.parents.keys():
            print('Parent fitness: ', self.parents[key].fitness, ' and child fitness: ', self.children[key].fitness)
        print('\n')


    def Show_Best(self):
        # jumping
        max_fitness = self.parents[0].fitness
        max_parent = 0

        for i in self.parents: #range(len(self.parents)):
            max_fitness = max(self.parents[i].fitness, max_fitness)
            max_parent = i
        print('MAX', max_fitness)

        self.parents[max_parent].Start_Simulation('GUI')

        os.system(f"cp body{self.parents[max_parent].myID}.urdf best_robots/body{c.seed}_{max_parent}_{self.currGen}.urdf")
        os.system(f"cp brain{self.parents[max_parent].myID}.nndf best_robots/brain{c.seed}_{max_parent}_{self.currGen}.nndf")
        
        os.system('rm brain*.nndf')
        os.system('rm body*.urdf')
        os.system('rm fitness*.txt')
    
        self.parents[max_parent].Start_Simulation('GUI')

    def Evaluate(self, solutions):
        for i in solutions: #range(len(self.parents)):
            solutions[i].Start_Simulation('DIRECT')

        for i in solutions: #range(len(self.parents)):
            solutions[i].Wait_For_Simulation_To_End()
        