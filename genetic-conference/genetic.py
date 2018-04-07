from conference import *
from random import *
from morph import flatten

NUMBER_OF_CROMOSSOMES = 6
NUMBER_OF_ROOMS = 3
MAX_START_BLOCK = 64    # Talks start from 9AM to 6:40PM.

def hard_coded_insertion():
    papers = []

    papers.append(Paper(0, ['Minsky', 'Hofstadter'], ['AI', 'Machine Learning'], 30))
    papers.append(Paper(1, ['Russell', 'Minsky'], ['Machine Learning'], 20))
    papers.append(Paper(2, ['Norvig', 'Kurzweil'], ['AI', 'Medicine'], 30))

    return papers

def init_random_conference(papers):
    days, sessions, presentations = [], [], []

    # Generate a random presentation for each paper.
    for id, paper in enumerate(papers):
        author = randint(0, len(paper.authors))
        block = randint(0, MAX_START_BLOCK)

        presentations.append(Presentation(id, paper, author, block))

    # Generate random sessions for each presentation.
    themes = list(set(flatten([pres.paper.themes for pres in presentations])))

    for id in range(0, len(presentations) - 1):
        k = randint(1, len(presentations))
        sessions.append(Session(id, choice(themes), choices(presentations, k=k), randint(1, NUMBER_OF_ROOMS)))

    # Generate random days.
    for id in range(3):
        days.append(Day(id, choice(sessions)))

    return Conference(days)

def generate_initial_population():
    papers = hard_coded_insertion()
    
    for i in range(NUMBER_OF_CROMOSSOMES):
        conference = init_random_conference(papers)
        conference.export_to_spreadsheet()

generate_initial_population()








