from defs import *
from objects import *


random.seed()

#step1 - initial population
population = init_random_population()
#introduce perfect genome to see population rapidly go towards it and change number of cycles to ~10
#schedule = Schedule()
#schedule.DNA = [1,1,1,1,1,1,1,1,1,1]
#population[0] = schedule


i = 0
while(i != 1):

    #step2 - select for matching
    selection_prob = selection_probabilities(population)
    select_piechart = create_selection_piechart(selection_prob)
    selected_for_matching = select_for_match(population, select_piechart)


    #step3 - match
    matches = match(selected_for_matching)
    print("Matches:", matches)

    #step4 - cross-over

    #step5 - mutations

    #step6 - (terminate?)

    #print of population
    for schedule in population:
        schedule.print()
    print(selected_for_matching,'\n\n')

    newpop = []
    for idx in selected_for_matching:
        newpop.append(population[idx])

    
    #Criar intervalos, gerar random numbers NUMBER_OF_CROMOSSOMES times, emparelhar esses, cruzal-los, mutá-los 
    i+=1



