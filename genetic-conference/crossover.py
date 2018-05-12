from random import *
from macros import *

"""
    Generate a roulette wheel based on the fitness score of the individuals.
    This approach is based on the Fitness Proportionate Selection genetic operator.
    Returns a list of individual object and roulette slice pairs.
"""
def generate_roulette(scores):
    roulette, prob = [], 0.0
    fit_sum = sum([score[1] for score in scores])

    for score in scores:
        prob = prob + (score[1] / fit_sum)
        roulette.append((score, prob))

    return roulette


"""
    Spin the previously generated roulette x times, x being the number of cromossomes in the population times two.
    Returns a list of pairs of parents which will crossover.
"""
def spin_roulette(roulette, population):
    relations = []

    def find_slice(spin):
        for i, _ in enumerate(roulette):
            if spin < roulette[i][1]: return roulette[i][0][0]

    def make_slice_pair():
        spin_1, spin_2 = uniform(0.0, 1.0), uniform(0.0, 1.0)
        return (find_slice(spin_1), find_slice(spin_2))

    for _ in range(len(roulette)):
        relations.append(make_slice_pair())

    return relations


"""
    TODO: Specify how the crossover is done.
    Crossover two cromossomes.
    Returns the resulting child.
"""
def xover_parents(mother, father):
    print("Mother: ", mother)
    print("Father: ", father, "\n")

    return mother



"""
    Crossover this generation's entire population.
    Returns a list of crossed-over children.
"""
def xover_population(couples):
    children = []

    for couple in couples: 
        child = xover_parents(couple[0], couple[1])
        children.append(child)

    return children