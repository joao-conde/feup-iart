from random import *
from macros import *
from fitness import calculate_fitness
from utilities import generate_except


def mutate_room(conference):
    conference[randint(0, len(conference)-1)]['room'] = randint(1, NUMBER_OF_ROOMS)
    return conference
    
def mutate_day(conference):
    conference[randint(0, len(conference)-1)]['day'] = randint(1, 3)
    return conference


def mutate_time(conference):
    conference[randint(0, len(conference)-1)]['time'] = generate_except(0, MAX_START_BLOCK, INVALID_BLOCKS)
    return conference


def mutate_conference(conference):
    attribute = randint(1,3)
    if attribute == 1: return mutate_room(conference)
    if attribute == 2: return mutate_day(conference)
    if attribute == 3: return mutate_time(conference)


"""
    
"""
def mutate_population(population, scores):
    for i in range(len(population)):
        if uniform(0,1) < MUTATION: 
            population[i] = mutate_conference(population[i])
            scores[i] = calculate_fitness(population[i])

    return (population, scores)


