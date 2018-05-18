from intervals import *
from macros import *
from statistics import stdev, mean
from utilities import *
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
        
    if FIT_SESSIONS:
        scores.append(score_sessions(individual))

    print(scores)

    return mean(scores)


# Receives a talk dictionary entry and returns the interval of time allocated to that resource.
def construct_interval(talk):
    return Interval([talk.get('time'), talk.get('time') + talk.get('paper').duration // 10])

"""
    Scores an individual, based on the number of conflicting talks.
    The grading system follows the formula: 100 - 100/TalkNo * CollisionNo.
    TODO: For now, it's considering collisions even it is in separate rooms.
"""
def score_collisions(individual):

    

    intervals, conflicts = [construct_interval(talk) for talk in individual], 0
    breaks = [Interval([COFFEE_1_START, COFFEE_1_END]), Interval([LUNCH_START, LUNCH_END]), Interval([COFFEE_2_START, COFFEE_2_END])]

    # Counts the number of paper-paper conflicts.
    conflicts += count_paper_collisions(intervals)

    # Counts the number of paper-break conflicts.
    conflicts += len([inter for inter in intervals if any((inter in x) for x in breaks)])
        
    return 100 - 100 // len(individual) * conflicts  # Calculate fitness score.


"""
"""
def count_paper_collisions(intervals):
    conflicts = 0

    for ia, ib in itertools.combinations(intervals, 2):
        if ((ia < ib and (ia.upper > ib.lower or ib.lower < ia.upper)) or 
            (ia > ib and (ib.upper > ia.lower or ia.lower < ib.upper)) or
            (ia in ib) or (ib in ia) or (ia == ib)): 
                print(ia, ib)
                conflicts += 1

    return conflicts


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
    room_talks = []

    for room_i in range(NUMBER_OF_ROOMS):
        for day_i in range(3):
            room_talk = [talk for talk in individual if talk['room'] == room_i + 1 and talk['day'] == day_i + 1]
            room_talks.append(room_talk)

    return 100
    


'''
    Same speaker required in 2 or more rooms at the same time
'''
def score_speaker_occupation(individual):
    
    collisions = 0

    day1 = [talk for talk in individual if talk['day'] == 1]
    day2 = [talk for talk in individual if talk['day'] == 2]
    day3 = [talk for talk in individual if talk['day'] == 3]  

    collisions += score_collisions_speaker(day1)
    collisions += score_collisions_speaker(day2)
    collisions += score_collisions_speaker(day3)

    return 100 - collisions / len(individual) * 100


def score_collisions_speaker(day_talks):
    collisions = 0
    daily_speakers = set([talk['paper'].speaker for talk in day_talks])

    for speaker in daily_speakers:
        sp_talks = [talk for talk in day_talks if talk['paper'].speaker == speaker]

        for talk in sp_talks:
            collisions += count_collisions(construct_interval(talk))

    return collisions


def count_collisions(intervals):
    return 0


def get_most_fit(pop_scores):
    scores = [el[1] for el in pop_scores]
    return pop_scores[scores.index(max(scores))][0]

def get_worst_fit_pos(pop_scores):
    scores = [el[1] for el in pop_scores]
    return scores.index(min(scores))


