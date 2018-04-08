import re
from morph import flatten
from conference import *
from random import *
from macros import *

'''
Até agora, o código dá parse aos papers inseridos manualmente pelo usuário em papers.txt e 
aplica regex a cada linha do ficheiro, criando objetos da classe Paper (método init_papers).

O algoritmo genético irá operar sobre o tuplo <id_paper, room_no, day, block_start, speaker_index>.
Para cada paper existe um tuplo destes, sendo a representação apenas uma lista de onde, quando e
quem dá cada talk.

Gera-se um tuplo para cada talk em init_paper_tuple, aleatoriamente. As macros usadas são o número
de bits usado para codificar certo atributo (4 bits para codificar o número da sala).

No fim, o genótipo é composto por todos os tuplos seguidos. Repete-se o processo NUMBER_OF_CROMOSSOMES
vezes e temos a população inicial. A conversão para objeto Presentation é no método generate_conference,
que ainda está incompleto (só gera apresentações e não uma conferência inteira, embora já tenha dados
para tal). Tem uma data de regex manhoso para não estar a encher o código de merda desnecessária.
'''

def init_papers(file_path):
    file = open(file_path, 'r')
    papers, paper_list = [], file.readlines()

    for id, paper in enumerate(paper_list):
        m = re.search(r'(?P<title>.+) \| (?P<authors>.+) \| (?P<themes>.+) \| (?P<duration>20|30)', paper)
        papers.append(Paper(id, m.group('title'), m.group('authors').split(', '), m.group('themes').split(', '), m.group('duration')))

    file.close()
    return papers

# Initialize <Paper, Room, Day, TimeBlock, Speaker> tuples.
def init_paper_tuple(papers):
    genotype = ''

    for paper in papers:
        p_id = format(paper.id, f'0{ID_BIT_ENCODING}b')
        p_room = format(randint(1, NUMBER_OF_ROOMS), f'0{ROOM_BIT_ENCODING}b')
        p_day = format(randint(1, 3), f'0{DAY_BIT_ENCODING}b')
        p_block = format(randint(0, MAX_START_BLOCK), f'0{BLOCK_BIT_ENCODING}b')
        p_speaker = format(randint(0, len(paper.authors) - 1), f'0{SPEAKER_BIT_ENCODING}b')

        genotype += f'{p_id}{p_room}{p_day}{p_block}{p_speaker}'

    return genotype

def init_initial_population(papers):
    population = []

    for i in range(NUMBER_OF_CROMOSSOMES):
        genotype = init_paper_tuple(papers)
        print(f'\nGenerated genotype #{i+1}: \n{genotype}')
        population.append(genotype)
    
    return population

def generate_conference(genotype):
    r = re.findall(r'.{22}', genotype)
    
    for i, paper_tuple in enumerate(r):
        m = re.match(r'(?P<id>.{6})(?P<room>.{4})(?P<day>.{2})(?P<block>.{7})(?P<speaker>.{3})', paper_tuple)
        d = {key: int(value, 2) for key, value in m.groupdict().items()}  # Converts tuple to a dictionary with integer values.

        paper = papers[d.get('id')]
        presentation = Presentation(i, paper, paper.authors[d.get('speaker')], d.get('block'))
        print(vars(presentation))
    
papers = init_papers('papers.txt')
population = init_initial_population(papers)

for i, genotype in enumerate(population):
    print(f'\nConverting genotype #{i+1} from binary to Conference object...')
    generate_conference(genotype)





