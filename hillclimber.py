from solution import SOLUTION
import constants as c
import copy


class HILL_CLIMBER:
    def __init__(self):
        self.parent = SOLUTION()

    def Evolve(self):
        self.parent.Evaluate('GUI')

        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
        
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate('DIRECT')
        self.Print()
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)
        # self.child will receive a copy of self.parent's weights and fitness
    
    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child
        
    def Print(self):
        print('Parent fitness: ', self.parent.fitness, ' and child fitness: ', self.child.fitness)

    def Show_Best(self):
        self.parent.Evaluate('GUI')