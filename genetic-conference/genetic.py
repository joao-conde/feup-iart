import re
from morph import flatten
from conference import *
from random import *
from macros import *
from fitness import *
from crossover import *
from utilities import *

"""
    Genetic Algorithm based scheduler application entry point.
"""
def main():
    print('\n⏳  Genetic Conference Scheduler (v1.0)')
    
    # Initialize population.
    papers = parse_paper_file(input('Paper file path: '))
    wb_path = input('Spreadsheet path: ')

    population = init_population(papers)

    for gen_no in range(GENERATIONS):
        # export_to_spreadsheet(wb_path, population)
        print(f'Handling generation #{gen_no + 1}...\n')
        population = manage_generation(population)


"""
"""
def manage_generation(population):
    # Evaluate each individual from the population.
    scores = calculate_pop_fitness(population)

    # Crossover selection.
    roulette = generate_roulette(scores)
    couples = spin_roulette(roulette, population)

    # Crossover initialization.
    children = xover_population(couples)

    # Mutate resulting children.
    zombies = mutate_population(children)

    # Return new generation.
    return zombies


"""
    Parses each line of a user-created file containing papers and returns a list of Paper objects.
    Each line in the file follows the syntax: <PaperTitle> | <Author> | <Topic>[, Topic] | <20,30>
"""
def parse_paper_file(file_path):
    file = open(file_path, 'r')
    papers, paper_list = [], file.readlines()

    for id, paper in enumerate(paper_list):
        m = re.search(r'(?P<title>.+) \| (?P<speaker>.+) \| (?P<themes>.+) \| (?P<duration>20|30)', paper)
        paper_obj = Paper(id, m.group('title'), m.group('speaker'), m.group('themes').split(', '), m.group('duration'))
        papers.append(paper_obj)

    file.close()
    return papers


"""
    Generates a semi-random population composed of NUMBER_OF_CROMOSSOMES macro number of individuals.
    The population is a list of possible schedules of a conference, which is itself a list of talk schedules.
"""
def init_population(papers):
    population = []

    """
        Generates a semi-random individual in its binary representation.
        The genotype is composed of a dictionary containing a pointer for the paper object, talk's room, day
        and starting ten minute block for it.
    """
    def init_conference(papers):
        conference = []
        
        for paper in papers:
            gen_room, gen_day, gen_block = randint(1, NUMBER_OF_ROOMS), randint(1, 3), randint(0, MAX_START_BLOCK)
            conference.append({'paper': paper, 'room': gen_room, 'day': gen_day, 'time': gen_block})
        return conference

    for _ in range(NUMBER_OF_CROMOSSOMES):
        population.append(init_conference(papers))

    return population


"""
    Computes the fitness score of this generation's population.
    Returns a list of pairs which map the individual and its score.
"""
def calculate_pop_fitness(population):
    scores = []

    for individual in population:
        scores.append((individual, calculate_fitness(individual)))

    return scores


main()