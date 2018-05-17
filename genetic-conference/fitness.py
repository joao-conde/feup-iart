from intervals import *
from macros import *
from statistics import stdev, mean
import itertools



"""
    Computes the fitness score of this generation's population.
    Returns a list of pairs which map the individual and its score.
"""
def calculate_pop_fitness(population):
    scores = []

    for individual in population:
        scores.append((individual, calculate_fitness(individual)))

    return scores


"""
    Applies a number of tests to a provided individual and returns an average of calculated scores.
"""
def calculate_fitness(individual):
    scores = []

    if FIT_COLLISIONS: 
        scores.append(score_collisions(individual))

    if FIT_ROOM_OCC:
        scores.append(score_room_occupation(individual))

    if FIT_SPEAKER_OCC:
        scores.append(score_speaker_occupation(individual))

    return mean(scores)


"""
    Scores an individual, based on the number of conflicting talks.
    The grading system follows the formula: 100 - 100/TalkNo * CollisionNo.
    TODO: For now, it's considering collisions even it is in separate rooms.
    TODO: Also, it's only considering inner collisions, when it should detect edge.
"""
def score_collisions(individual):

    # Receives a talk dictionary entry and returns the interval of time allocated to that resource.
    def construct_interval(talk):
        return Interval([talk.get('time'), talk.get('time') + talk.get('paper').duration // 10])

    intervals, conflicts = [construct_interval(talk) for talk in individual], 0
    breaks = [Interval([COFFEE_1_START, COFFEE_1_END]), Interval([LUNCH_START, LUNCH_END]), Interval([COFFEE_2_START, COFFEE_2_END])]

    # Counts the number of paper-paper conflicts.
    for ia, ib in itertools.combinations(intervals, 2):
        if (ia in ib) : conflicts += 1

    # Counts the number of paper-break conflicts.
    conflicts += len([inter for inter in intervals if any((inter in x) for x in breaks)])
        
    return 100 - 100 // len(individual) * conflicts  # Calculate fitness score.


"""
    Scores an individual, based on the balance of room occupation.
    TODO: Variance calculation isn't perfectly fine.
"""
def score_room_occupation(individual):
    rooms, counts = [talk.get('room') for talk in individual], []

    for room_i in range(NUMBER_OF_ROOMS):
        counts.append(rooms.count(room_i))

    return 100 - stdev(counts) / len(individual) * 100


"""
"""
def score_sessions(individual):
    pass
    #for room_i in range(NUMBER_OF_ROOMS):
    


'''
    Speakers requeridos ao mesmo tempo
'''
def score_speaker_occupation(individual):
    return 0



def get_most_fit(pop_scores):
    scores = [el[1] for el in pop_scores]
    return pop_scores[scores.index(max(scores))][0]

def get_worst_fit_pos(pop_scores):
    scores = [el[1] for el in pop_scores]
    return scores.index(min(scores))


