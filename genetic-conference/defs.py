from objects import *

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

#calculate selection probabilities for each individual
def selection_probabilities(population):
    selectP = []
    totalFitness = 0
    for schedule in population:
        totalFitness += schedule.fitness()

    for schedule in population:
        selectP.append(schedule.fitness()/totalFitness)

    return selectP

#create a 'pie chart' of probability for each individual to be chosen for matching
def create_selection_piechart(select_probs):
    intervals = []
    lowerB = 0
    for prob in select_probs:
        interval = Interval(lowerB, lowerB + prob)
        intervals.append(interval)
        lowerB += prob
    return intervals

#select individuals for matching based on the pie chart
def select_for_match(population, selection_piechart):
    pop_idx = []
    for i in range(NUMBER_OF_CROMOSSOMES):
        rand = random.uniform(0,1)
        for index in range(len(selection_piechart)):
            if(selection_piechart[index].contains(rand)) : 
                pop_idx.append(index)
                break
                
    return pop_idx

#matches individuals for cross-over
def match(selected_for_matching):
    matches = []

    for i in range(NUMBER_OF_CROMOSSOMES):
        rand1 = rand2 = 0
        
        while rand1 == rand2:
            rand1 = random.randint(0, len(selected_for_matching)-1)
            rand2 = random.randint(0, len(selected_for_matching)-1)
        
        match = [selected_for_matching[rand1], selected_for_matching[rand2]]
        matches.append(match)

    return matches