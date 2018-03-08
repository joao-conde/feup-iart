import random

class Schedule():
    
    def __init__(self):
        self.DNA = []

    def randomizeGenome(self, genomeSize):
        for j in range(genomeSize):
            self.DNA.append(random.randint(0, 1))

    def fitness(self):
        return self.DNA.count(1)

    def print(self):
        print("My genome is",self.DNA,"and my value is",self.fitness())

    