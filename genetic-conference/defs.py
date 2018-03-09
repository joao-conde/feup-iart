from objects import *

#functions and "constants" here

NUMBER_OF_CROMOSSOMES = 6
CROMOSSOME_SIZE = 10

#initial population - random genes
def init_random_population():
    population = []
    for i in range(NUMBER_OF_CROMOSSOMES):
        schedule = Schedule()
        schedule.randomize_genome(CROMOSSOME_SIZE)
        population.append(schedule)
    
    return population

def selection_probabilities(population):
    selectP = []
    totalFitness = 0
    for schedule in population:
        totalFitness += schedule.fitness()

    for schedule in population:
        selectP.append(schedule.fitness()/totalFitness)

    return selectP

def create_selection_piechart(selectProbs):
    intervals = []
    lowerB = 0
    for prob in selectProbs:
        interval = Interval(lowerB, lowerB + prob)
        intervals.append(interval)
        lowerB += prob
    return intervals

def select_for_match(population, selectionPieChart):
    popIndexes = []
    for i in range(NUMBER_OF_CROMOSSOMES):
        rand = random.uniform(0,1)
        for index in range(len(selectionPieChart)):
            if(selectionPieChart[index].contains(rand)) : 
                popIndexes.append(index)
                break
                
    return popIndexes