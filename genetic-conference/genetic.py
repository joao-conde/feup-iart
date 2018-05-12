import re
from morph import flatten
from conference import *
from random import *
from macros import *
from fitness import *
from crossover import *

"""
    Genetic Algorithm based scheduler application entry point.
"""
def main():
    print('\n⏳  Genetic Conference Scheduler (v1.0)\n')
    
    # Initialize population.
    papers = parse_paper_file(input('Paper file path: '))
    population = init_population(papers)

    # Evaluate each individual from the population.
    scores = calculate_pop_fitness(population)

    # Crossover selection.
    roulette = generate_roulette(scores)
    couples = spin_roulette(roulette, population)

    # Crossover initialization.
    children = xover_population(couples)


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


"""
    Generates a semi-random population composed of NUMBER_OF_CROMOSSOMES macro number of individuals.
    The population is a list of possible schedules of a conference, which is itself a list of talk schedules.
"""
def init_population(papers):
    population = []

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

# ------------- OLD CODE ----------------------------
"""
    Based on the provided list of Paper objects, generates a semi-random population.
    A population is composed of multiple possible schedules for the conference.
"""
def init_population_old(papers):
    population = []

    for i in range(NUMBER_OF_CROMOSSOMES):
        genotype = init_paper_rep(papers)
        print(f'\nGenerated genotype #{i+1}: \n{genotype}')
        population.append(genotype)
    
    return population


"""
    Generates a semi-random individual in its binary representation.
    The genotype follows the tuple representation: <PaperId, PaperRoom, PaperDay, PaperTimeBlock>.
"""
def init_paper_rep(papers):
    genotype = ''

    for paper in papers:
        p_id = format(paper.id, f'0{ID_BIT_ENCODING}b')
        p_room = format(randint(1, NUMBER_OF_ROOMS), f'0{ROOM_BIT_ENCODING}b')
        p_day = format(randint(1, 3), f'0{DAY_BIT_ENCODING}b')
        p_block = format(randint(0, MAX_START_BLOCK), f'0{BLOCK_BIT_ENCODING}b')

        genotype += f'{p_id}{p_room}{p_day}{p_block}'

    return genotype



def convert_rep(genotype):
    r = re.findall(r'.{19}', genotype)
    conferences = []
    
    for i, paper_tuple in enumerate(r):
        m = re.match(r'(?P<id>.{6})(?P<room>.{4})(?P<day>.{2})(?P<block>.{7})', paper_tuple)
        d = {key: int(value, 2) for key, value in m.groupdict().items()}  # Converts tuple to a dictionary with integer values.
        conferences.append(d)

    return conferences
"""
for i, genotype in enumerate(population):
    print(f'\nConverting genotype #{i+1} to phenotype...')
    conferences = convert_rep(genotype)
    calculate_fitness(papers, conferences)

print(convert_rep(population[0]), convert_rep(population[1]))
crossover = single_point_xover(population[0], population[1])
print(convert_rep(crossover[0]), convert_rep(crossover[1]))
"""





