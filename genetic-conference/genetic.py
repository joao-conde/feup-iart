import re
from morph import flatten
from conference import *
from random import *
from macros import *
from fitness import *
from crossover import *

def parse_paper_file(file_path):
    file = open(file_path, 'r')
    papers, paper_list = [], file.readlines()

    for id, paper in enumerate(paper_list):
        m = re.search(r'(?P<title>.+) \| (?P<speaker>.+) \| (?P<themes>.+) \| (?P<duration>20|30)', paper)
        papers.append(Paper(id, m.group('title'), m.group('speaker'), m.group('themes').split(', '), m.group('duration')))

    file.close()
    return papers

# Initialize <Paper, Room, Day, TimeBlock, Speaker> tuples.
def init_paper_rep(papers):
    genotype = ''

    for paper in papers:
        p_id = format(paper.id, f'0{ID_BIT_ENCODING}b')
        p_room = format(randint(1, NUMBER_OF_ROOMS), f'0{ROOM_BIT_ENCODING}b')
        p_day = format(randint(1, 3), f'0{DAY_BIT_ENCODING}b')
        p_block = format(randint(0, MAX_START_BLOCK), f'0{BLOCK_BIT_ENCODING}b')

        genotype += f'{p_id}{p_room}{p_day}{p_block}'

    return genotype

def init_initial_population(papers):
    population = []

    for i in range(NUMBER_OF_CROMOSSOMES):
        genotype = init_paper_rep(papers)
        print(f'\nGenerated genotype #{i+1}: \n{genotype}')
        population.append(genotype)
    
    return population

def convert_rep(genotype):
    r = re.findall(r'.{19}', genotype)
    conferences = []
    
    for i, paper_tuple in enumerate(r):
        m = re.match(r'(?P<id>.{6})(?P<room>.{4})(?P<day>.{2})(?P<block>.{7})', paper_tuple)
        d = {key: int(value, 2) for key, value in m.groupdict().items()}  # Converts tuple to a dictionary with integer values.
        conferences.append(d)

    return conferences
    
papers = parse_paper_file('papers.txt')
population = init_initial_population(papers)

for i, genotype in enumerate(population):
    print(f'\nConverting genotype #{i+1} to phenotype...')
    conferences = convert_rep(genotype)
    calculate_fitness(papers, conferences)

print(convert_rep(population[0]), convert_rep(population[1]))
crossover = single_point_xover(population[0], population[1])
print(convert_rep(crossover[0]), convert_rep(crossover[1]))






