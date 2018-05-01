from intervals import IntInterval
import itertools

def calculate_fitness(papers, talks):
    # TODO: Eventually add more here.
    return get_collision_count(papers, talks)

# TODO: Room isn't counted in the collision.
def get_collision_count(papers, talks):

    # Receives a talk dictionary entry and returns the interval of time allocated to that resource.
    def construct_interval(talk):
        return IntInterval([talk.get('block'), talk.get('block') + papers[talk.get('id')].duration // 10])

    intervals, conflicts = [construct_interval(talk) for talk in talks], 0

    # Counts the number of conflicts on the papers.
    for ia, ib in itertools.combinations(intervals, 2):
        if ia in ib: conflicts += 1
    
    return 100 - 100 // len(talks) * conflicts  # Calculate fitness score.







    

