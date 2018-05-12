from intervals import IntInterval
import itertools

"""
    Applies a number of tests to a provided individual and returns an average of scores.
"""
def calculate_fitness(individual):
    return score_collisions(individual)


"""
    Scores an individual, based on the number of conflicting talks.
    The grading system follows the formula: 100 - 100/TalkNo * CollisionNo.
"""
def score_collisions(individual):

    # Receives a talk dictionary entry and returns the interval of time allocated to that resource.
    def construct_interval(talk):
        return IntInterval([talk.get('time'), talk.get('time') + talk.get('paper').duration // 10])

    intervals, conflicts = [construct_interval(talk) for talk in individual], 0

    # Counts the number of conflicts on the papers.
    for ia, ib in itertools.combinations(intervals, 2):
        if ia in ib: conflicts += 1

    return 100 - 100 // len(individual) * conflicts  # Calculate fitness score.






    

