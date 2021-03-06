from random import *
from macros import *
from fitness import calculate_pop_fitness

"""
    Generate a roulette wheel based on the fitness score of the individuals.
    This approach is based on the Fitness Proportionate Selection genetic operator.
    Returns a list of individual object and roulette slice pairs.
"""
def generate_roulette(population, scores):
    roulette, prob = [], 0.0
    fit_sum = sum(scores)

    for i, score in enumerate(scores):
        prob += (score / fit_sum)
        roulette.append((population[i], prob))

    return roulette


"""
    Spin the previously generated roulette x times, x being the number of cromossomes in the population times two.
    Returns a list of pairs of parents which will crossover.
"""
def spin_roulette(roulette, population):
    relations = []

    def find_slice(spin):
        for i, _ in enumerate(roulette):
            if spin < roulette[i][1]: return roulette[i][0]

    def make_slice_pair():
        spin_1, spin_2 = uniform(0.0, 1.0), uniform(0.0, 1.0)
        return (find_slice(spin_1), find_slice(spin_2))

    for _ in range(NUMBER_OF_CROMOSSOMES // 2):
        relations.append(make_slice_pair())

    return relations



"""
    Crossover two cromossomes.
    50% chance for each talk of the schedule to be swapped with the other schedule talk (of the same paper).
    Returns the resulting child.
"""
def xover_parents(mother, father):
    #print("\n------CROSSOVER------\n")
    child1 , child2 = [] , []

    for presentation1, presentation2 in zip(mother, father):
        if randint(0,1) != 0:
            child1.append(presentation1)
            child2.append(presentation2)
        else:
            child1.append(presentation2)
            child2.append(presentation1)

    return [child1,child2]


"""
    Crossover this generation's entire population.
    Returns a list of crossed-over children.
"""
def xover_population(couples):
    children = []

    for couple in couples: 
        childs = xover_parents(couple[0], couple[1])
        children.extend(childs)

    return children


"""
    Immortality policy that preserves the fittest element intact for the next generation.
    Still allows crossover with the fittest.
"""
def immortality_policy(children, scores, fittest):
    children[scores.index(min(scores))] = fittest
    return children
    
