from entities import *

#functions and "constants" here

NUMBER_OF_CROMOSSOMES = 6
CROMOSSOME_SIZE = 10

#initial population - random genes
def initRandomPopulation():
    population = []
    for i in range(NUMBER_OF_CROMOSSOMES):
        schedule = Schedule()
        schedule.randomizeGenome(CROMOSSOME_SIZE)
        population.append(schedule)
    
    return population

def selectionProbabilities(population):
    selectP = []
    totalFitness = 0
    for schedule in population:
        totalFitness += schedule.fitness()

    for schedule in population:
        selectP.append(schedule.fitness()/totalFitness)

    return selectP