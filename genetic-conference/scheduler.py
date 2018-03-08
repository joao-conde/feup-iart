from entities import *

initialPop = []
for i in range(NUMBER_OF_CROMOSSOMES):
    initialPop.append(Schedule())

for schedule in initialPop:
    schedule.randomizeGenome(CROMOSSOME_SIZE)
    schedule.print()
