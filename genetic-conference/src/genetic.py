import re
import copy
import signal
import sys

from paper import *
from random import *
from macros import *
from fitness import *
from crossover import *
from mutation import *
from utilities import *

import time

logger = None

"""
    Genetic Algorithm based scheduler application entry point.
"""
def main():

    seed(time.time())
    print('\n⏳  Genetic Conference Scheduler (v5.5)')
    
    # Read papers file, set excel sheet export filename and logger file
    papers = parse_paper_file('../files/' + input('Paper file path: '))    
    wb_path = input('Spreadsheet path: ')

    global EXPORT_PATH
    EXPORT_PATH += wb_path

    global logger
    logger = open('../files/' + EXPORT_PATH + '-logs.txt', 'w+')
    
    population = init_population(papers)
    for gen_no in range(GENERATIONS):
        print(f'----- Handling generation #{gen_no + 1} -----')
        population = manage_generation(gen_no, population)


"""
    Processes each generation applying fitness, crossover based on that and mutation.
    Returns the new population
"""
def manage_generation(gen_no, population):

    # Evaluate each individual from the population.
    scores = calculate_pop_fitness(population)
    max_score = max(scores)
    fittest = copy.deepcopy(population[scores.index(max_score)])
    
    #if ctrl+c hits the program, best scheduling is saved
    global TO_EXPORT
    TO_EXPORT = fittest

    print(f"\nFITTEST: {max_score}\n\n\n")
    logger.write("GEN No. " + str(gen_no+1) + " ELITE SCORE: " + str(max_score) + "\n")

    if max_score >= DESIRED_FITNESS: exit()
                

    #------------- GENETIC ALGORITHM -------------#

    # Crossover selection.
    roulette = generate_roulette(population, scores)
    couples = spin_roulette(roulette, population)

    # Crossover initialization.
    children = xover_population(couples)

    # Mutate resulting children.
    zombies_tuple = mutate_population(children, scores)
    zombies, scores = zombies_tuple[0], zombies_tuple[1]

    # Elitism - replace the worst child of gen N by the best of gen N-1
    population = immortality_policy(zombies, scores, fittest)

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


"""
    Saves the current best schedule to an excel sheet 
"""
def exit():
    export_to_spreadsheet('../files/' + EXPORT_PATH, TO_EXPORT)
    print("\n\nSaved best scheduling found to files/" + EXPORT_PATH + ".xlsx")
    sys.exit(0)

"""
    If CTRL+C is used, saves the current best schedule to an excel sheet
"""
def signal_handler(signal, frame): exit()

#program entry point
signal.signal(signal.SIGINT, signal_handler)
main()