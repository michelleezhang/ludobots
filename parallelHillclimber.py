from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system('rm brain*.nndf')
        os.system('rm fitness*.txt')

        self.parents = {}
        self.nextAvailableID = 0

        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        
    def Evolve(self):
        self.Evaluate(self.parents)
    
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
        
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}

        for i in range(len(self.parents)):
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
    
    def Mutate(self):
        for i in range(len(self.children)):
            self.children[i].Mutate()

    def Select(self):
        for i in range(len(self.parents)):
            if self.parents[i].fitness > self.children[i].fitness:
                self.parents[i] = self.children[i]

        # #jumping
        # for i in range(len(self.parents)):
        #     if self.parents[i].fitness < self.children[i].fitness:
        #         self.parents[i] = self.children[i]
        
    def Print(self):
        print('\n')
        for key in self.parents.keys():
            print('Parent fitness: ', self.parents[key].fitness, ' and child fitness: ', self.children[key].fitness)
        print('\n')

    def Show_Best(self):
        min_fitness = self.parents[0].fitness
        for i in range(len(self.parents)):
            min_fitness = min(self.parents[i].fitness, min_fitness)
        
        for i in range(len(self.parents)):
            if self.parents[i].fitness == min_fitness:
                self.parents[i].Start_Simulation('GUI')
        
        # # jumping
        # max_fitness = self.parents[0].fitness
        # for i in range(len(self.parents)):
        #     max_fitness = max(self.parents[i].fitness, max_fitness)
        
        # for i in range(len(self.parents)):
        #     if self.parents[i].fitness == max_fitness:
        #         self.parents[i].Start_Simulation('GUI')

    def Evaluate(self, solutions):
        for i in range(len(self.parents)):
            solutions[i].Start_Simulation('DIRECT')

        for i in range(len(self.parents)):
            solutions[i].Wait_For_Simulation_To_End()
        