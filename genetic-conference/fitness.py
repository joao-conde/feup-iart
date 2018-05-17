from intervals import IntInterval
from macros import *
import itertools

"""
    Applies a number of tests to a provided individual and returns an average of scores.
"""
def calculate_fitness(individual):
    return score_collisions(individual)


"""
    Scores an individual, based on the number of conflicting talks.
    The grading system follows the formula: 100 - 100/TalkNo * CollisionNo.
    TODO: For now, it's considering collisions even it is in separate rooms.
"""
def score_collisions(individual):

    # Receives a talk dictionary entry and returns the interval of time allocated to that resource.
    def construct_interval(talk):
        return IntInterval([talk.get('time'), talk.get('time') + talk.get('paper').duration // 10])

    intervals, conflicts = [construct_interval(talk) for talk in individual], 0
    breaks = [IntInterval([COFFEE_1_START, COFFEE_1_END]), IntInterval([LUNCH_START, LUNCH_END]), IntInterval([COFFEE_2_START, COFFEE_2_END])]

    # Counts the number of paper-paper conflicts.
    for ia, ib in itertools.combinations(intervals, 2):
        if ia in ib: conflicts += 1

    # Counts the number of paper-break conflicts.
    break_conf = len([inter for inter in intervals if any((inter in x) for x in breaks)])
    print(break_conf)
        
        

    return 100 - 100 // len(individual) * conflicts  # Calculate fitness score.


"""
"""
def score_overlapping_breaks(individual):
    pass

    






    

