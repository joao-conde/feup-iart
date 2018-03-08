from defs import *

class Schedule():
    
    def __init__(self):
        self.DNA = []

    def randomizeGenome(self, genomeSize):
        for i in range(genomeSize):
            self.DNA.append(1)

    def print(self):
        print("My genome is",self.DNA)