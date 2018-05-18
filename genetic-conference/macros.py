# Genetic constants
GENERATIONS = 2000
NUMBER_OF_CROMOSSOMES = 20
MUTATION = 0.01
DESIRED_FITNESS = 98


# Break Scheduling
COFFEE_1_START =    6
COFFEE_1_END =      8
LUNCH_START =       21
LUNCH_END =         29
COFFEE_2_START =    48
COFFEE_2_END =      50

# Conference limitations
NUMBER_OF_ROOMS =   5
MAX_START_BLOCK =   57

INVALID_MORNING = [x for x in range(COFFEE_1_START,COFFEE_1_END + 1)]
INVALID_LUNCH = [x for x in range(LUNCH_START, LUNCH_END + 1)]
INVALID_AFTERNOON = [x for x in range(COFFEE_2_START, COFFEE_2_END + 1)]

INVALID_BLOCKS = set(INVALID_MORNING + INVALID_LUNCH + INVALID_AFTERNOON)
print(INVALID_BLOCKS)

# Fitness parameters
FIT_COLLISIONS =    True
FIT_ROOM_OCC =      False
FIT_SPEAKER_OCC =   False
FIT_SESSIONS =      False

# Spreadsheet parameters
SHEET_COL_START =   3
SHEET_ROW_START =   4
