from intervals import *
from macros import *
from statistics import stdev, mean
from utilities import *
import itertools
import time



"""
    Computes the fitness score of this generation's population.
    Returns a list of individual's score.
"""
def calculate_pop_fitness(population):
    scores = []

    for individual in population:
        scores.append(calculate_fitness(individual))

    return scores


"""
    Applies a variety of tests to a provided individual and returns an average of calculated scores.
"""
def calculate_fitness(individual):
    scores = []

    if FIT_SCHEDULE_COLLISIONS: 
        scores.append(WEIGHT_SCHEDULE_COLL * score_collisions(individual))

    if FIT_BREAK_COLLISIONS:
        scores.append(WEIGHT_BREAK_COLL * score_break_collisions(individual))

    if FIT_SPEAKER_OCC:
        scores.append(WEIGHT_SPEAKER_COLL * score_speaker_occupation(individual))
        
    if FIT_SESSIONS_THEME:
        scores.append(WEIGHT_SESSION_THEME * score_sessions_theme(individual))

    if FIT_SESSIONS_BALANCE:
        scores.append(WEIGHT_SESSION_BALANCE * score_sessions_balance(individual))

    return (1 - sum(scores)) * 100

""" 
    Receives a talk dictionary entry and returns the interval of time allocated to that resource.
"""
def construct_interval(talk):
    return Interval([talk.get('time'), talk.get('time') + talk.get('paper').duration // 10])

"""
    Scores an individual, based on the number of conflicting talks.
    The grading system follows the formula: 100 - 100/TalkNo * CollisionNo.
"""
def score_collisions(individual):
    conflicts = 0
    breaks = [Interval([COFFEE_1_START, COFFEE_1_END]), Interval([LUNCH_START, LUNCH_END]), Interval([COFFEE_2_START, COFFEE_2_END])]

    # Generates a list of organized intervals.
    s_talks, i_talks = [], []

    for day_i in range(3):
        for room_i in range(NUMBER_OF_ROOMS):
            room_talk = [talk for talk in individual if talk['room'] == room_i + 1 and talk['day'] == day_i + 1]
            s_talks.append(room_talk)

    for i in range(3 * NUMBER_OF_ROOMS):
        intervals = [construct_interval(talk) for talk in s_talks[i]]
        i_talks.append(intervals)
        
    # Counts the number of paper-paper conflicts.
    conflicts += sum([count_paper_collisions(sit) for sit in i_talks])
        
    return conflicts/len(individual)

"""
    Counts collisions between paper time intervals
"""
def count_paper_collisions(intervals):
    conflicts = 0

    for ia, ib in itertools.combinations(intervals, 2):
        if ((ia < ib and (ia.upper > ib.lower or ib.lower < ia.upper)) or 
            (ia > ib and (ib.upper > ia.lower or ia.lower < ib.upper)) or
            (ia in ib) or (ib in ia) or (ia == ib)): 
            
            conflicts += 1
            
    return conflicts


"""
    Evaluates talk collisions with conference scheduled breaks
"""
def score_break_collisions(individual):
    violations = [talk['paper'].id for talk in individual if talk['time'] in INVALID_BLOCKS or talk['time']+talk['paper'].duration//BLOCK_TIME in INVALID_BLOCKS]
    return len(violations)/len(individual)


"""
    Penalizes sessions with a wide variety of different themes
"""
def score_sessions_theme(individual):

    diversity = 0

    for room_i in range(NUMBER_OF_ROOMS):
        room_i_morning_session_themes_list= [talk['paper'].themes for talk in individual if talk['room'] == room_i+1 and talk['time'] >= MORNING_SESSION_START and talk['time'] <= MORNING_SESSION_END]
        themes = []
        for theme_list in room_i_morning_session_themes_list: themes.extend(theme_list)
        theme_set = set(themes)
        
        if len(theme_set) != 1: diversity += len(theme_set)

        themes = []
        room_i_afternoon_session_themes_list= [talk['paper'].themes for talk in individual if talk['room'] == room_i+1 and talk['time'] >= AFTERNOON_SESSION_START and talk['time'] <= AFTERNOON_SESSION_END]
        for theme_list in room_i_afternoon_session_themes_list: themes.extend(theme_list)
        theme_set = set(themes)
        
        if len(theme_set) != 1: diversity += len(theme_set)

        
    return diversity/len(individual)
    


'''
    Same speaker required in 2 or more rooms at the same time, per day
'''
def score_speaker_occupation(individual):
    
    collisions = 0

    day1 = [talk for talk in individual if talk['day'] == 1]
    day2 = [talk for talk in individual if talk['day'] == 2]
    day3 = [talk for talk in individual if talk['day'] == 3]  

    collisions += score_collisions_speaker(day1)
    collisions += score_collisions_speaker(day2)
    collisions += score_collisions_speaker(day3)

    return collisions/len(individual)



'''
    Speaker required in 2 or more rooms in the same time
'''
def score_collisions_speaker(day_talks):
    collisions = 0
    daily_speakers = set([talk['paper'].speaker for talk in day_talks])

    for speaker in daily_speakers:
        sp_talks = [talk for talk in day_talks if talk['paper'].speaker == speaker]

        intervals = [construct_interval(talk) for talk in sp_talks]
    
        collisions += count_paper_collisions(intervals)
    
    return collisions


"""
    Evaluates if a session that has talks is balanced i.e. that there is at least 2 full-paper talks.
"""
def score_sessions_balance(individual):
    unbalance = 0

    day1 = [talk for talk in individual if talk['day'] == 1]
    day2 = [talk for talk in individual if talk['day'] == 2]
    day3 = [talk for talk in individual if talk['day'] == 3]  

    unbalance += score_sessions_balance_day(day1)
    unbalance += score_sessions_balance_day(day2)
    unbalance += score_sessions_balance_day(day3)
    
    return unbalance // (3 * len(individual))

"""
    Evaluates the sessions balance of that day.
"""
def score_sessions_balance_day(day_talks):
    
    balance = 0

    for room_i in range(NUMBER_OF_ROOMS):
        morning_session_durations = [talk['paper'].duration for talk in day_talks if talk['time'] >= MORNING_SESSION_START and talk['time'] <= MORNING_SESSION_END]
        afternoon_session_durations = [talk['paper'].duration for talk in day_talks if talk['time'] >= AFTERNOON_SESSION_START and talk['time'] <= AFTERNOON_SESSION_END]
        
        morning_full_papers = 0
        for duration in morning_session_durations:
            if duration == FULL_PAPER_DUR: 
                morning_full_papers += 1
                if morning_full_papers >= 2: break


        afternoon_full_papers = 0
        for duration in afternoon_session_durations:
            if duration == FULL_PAPER_DUR: 
                afternoon_full_papers += 1
                if afternoon_full_papers >= 2: break

        
        balance += (morning_full_papers / 2 + afternoon_full_papers / 2) / 2

    return 1 - (balance / NUMBER_OF_ROOMS)
