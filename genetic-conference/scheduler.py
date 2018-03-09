from defs import *
from objects import *


random.seed()

#step1 - initial population
population = init_random_population()


#print of population
for schedule in population:
    schedule.print()


#select match cross mutate terminate?
i = 0
while(i != 1):
    #step2 - selection for matching
    selection_prob = selection_probabilities(population)
    select_piechart = create_selection_piechart(selection_prob)
    selectedForMatching = select_for_match(population, select_piechart)

    print(selectedForMatching)


    #Criar intervalos, gerar random numbers NUMBER_OF_CROMOSSOMES times, emparelhar esses, cruzal-los, mutá-los 
    i+=1



