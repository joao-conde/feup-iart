import random


#creates an interval from ]lb, up]
class Interval():
    
    def __init__(self, lb, ub):
        self.lb = lb
        self.ub = ub

    def contains(self,x):
        return (x > self.lb and x <= self.ub)

    def print(self):
        print("Interval ]",self.lb,',',self.ub,']')

class Schedule():
    
    def __init__(self):
        self.DNA = []

    def randomize_genome(self, genomeSize):
        for j in range(genomeSize):
            self.DNA.append(random.randint(0, 1))

    def fitness(self):
        return self.DNA.count(1)

    def print(self):
        print("My genome is",self.DNA,"and my value is",self.fitness())

    