import re
import copy
from morph import flatten
from paper import *
from random import *
from macros import *
from fitness import *
from crossover import *
from mutation import *
from utilities import *

import time

#logger = open('logger.txt', 'w+')

"""
    Genetic Algorithm based scheduler application entry point.
"""
def main():
    #initialize random seed 
    seed(time.time())
    print('\n⏳  Genetic Conference Scheduler (v3.4)')
    
    # Initialize population.
    #papers = parse_paper_file(input('Paper file path: '))
    papers = parse_paper_file("papers_mock.txt")
    
    #wb_path = input('Spreadsheet path: ')
    
    population = init_population(papers)
    for gen_no in range(GENERATIONS):
        print(f'-----Handling generation #{gen_no + 1}-----\n')
        population = manage_generation(population)


"""
"""
def manage_generation(population):

    # Evaluate each individual from the population.
    scores = calculate_pop_fitness(population)
    max_score = max(scores)
    fittest = copy.deepcopy(population[scores.index(max_score)])

    print(f"\n\nELITE:{max_score}\n\n")
    #print_conference(fittest)
    #logger.write(str(max_score) + "\n")

    for i, score in enumerate(scores):
        if score >= DESIRED_FITNESS:
            #print_conference(population[i])
            export_to_spreadsheet('results.xlsx', population[i])
            #input('')
            #time.sleep(2)
            pass

    # Crossover selection.
    roulette = generate_roulette(population, scores)
    couples = spin_roulette(roulette, population)

    # Crossover initialization.
    children = xover_population(couples)

    # Mutate resulting children.
    zombies_tuple = mutate_population(children, scores)
    zombies, scores = zombies_tuple[0], zombies_tuple[1]

    # Elitism - replace the worst child of gen N by the best of gen N-1
    population = elitism_policy(zombies, scores, fittest)

    # Return new generation.
    return population


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
        Generates a semi-random individual.
        The genotype is composed of a dictionary containing a pointer for the paper object, talk's room, day
        and starting ten minute block for it.
    """
    def init_conference(papers):
        conference = []
        
        
        for paper in papers:
            gen_room, gen_day, gen_block = randint(1, NUMBER_OF_ROOMS), randint(1, 3), generate_except(0, MAX_START_BLOCK, INVALID_BLOCKS)
            conference.append({'paper': paper, 'room': gen_room, 'day': gen_day, 'time': gen_block})
            
        return conference

    for _ in range(NUMBER_OF_CROMOSSOMES):
        population.append(init_conference(papers))

    return population



#program entry point
main()