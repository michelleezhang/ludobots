from solution import SOLUTION
import constants as c
import copy
import os
import numpy as np
import matplotlib.pyplot as plt

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
        
        # NEW
        # self.curr_gen_fitnessArray = []
        self.fitnessArray = []
        # self.fitnessArray = np.zeros((c.numberOfGenerations+1,c.populationSize))
        # self.maxArray = np.zeros(c.numberOfGenerations+1)
        
        # END NEW

        
    def Evolve(self):
        self.Evaluate(self.parents)

        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

        # print('hii', self.fitnessArray)

        return self.fitnessArray

        # plt.plot(self.fitnessArray)
        # plt.ylabel('Max fitness')
        # plt.show()

            # save the best fitness at each generation 
            # After the ith cycle of evaluation,
            # iterate over all parents to find the best fitness, 
            # and then store this value at the ith position of a one-dimensional array. 
            # Then at the end of evolution you can just plot this array without modification

        
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
    
    def Mutate(self): # 0.25, 1.0, [3, 0, 0, 0], [6, 2, 2, 2]
        minsize, maxsize, minbranch, maxbranch = 0.5, 1.1, [3, 0, 0, 0], [6, 2, 2, 2]

        for i in self.children: #range(len(self.children)):
            minsize, maxsize, minbranch, maxbranch = self.children[i].Mutate(minsize, maxsize, minbranch, maxbranch)

    def Select(self):
        # curr_gen_fitnessArray = [] 
        curr_gen_fitnessArray = np.zeros((len(self.parents)))

        #jumping
        for i in self.parents: #range(len(self.parents)):
            if self.parents[i].fitness < self.children[i].fitness:
                self.parents[i] = self.children[i]
            
            curr_gen_fitnessArray = np.append(curr_gen_fitnessArray, self.parents[i].fitness)
            # curr_gen_fitnessArray.append(self.parents[i].fitness)
        
        # the values of curr_gen_fitnessArray are actually the max fitness values of each gen
        # print('hyy', curr_gen_fitnessArray)

        self.fitnessArray.append(np.max(curr_gen_fitnessArray))
        
        # self.fitnessArray = np.append(self.fitnessArray, curr_gen_fitnessArray)
        # print('hii', self.fitnessArray)

        # so now we have an array where each entry is each population's max fitness

        # self.fitnessArray = np.append(self.fitnessArray, np.max(curr_gen_fitnessArray))
        # print('hii', self.fitnessArray)
        
        
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
    
        self.parents[max_parent].Start_Simulation('GUI')

    def Evaluate(self, solutions):
        for i in solutions: #range(len(self.parents)):
            solutions[i].Start_Simulation('DIRECT')

        for i in solutions: #range(len(self.parents)):
            solutions[i].Wait_For_Simulation_To_End()
        