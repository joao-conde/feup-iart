from defs import *

random.seed()

#step1 - initial population
population = initRandomPopulation()


#print of population
for schedule in population:
    schedule.print()




#select match cross mutate terminate?
i = 0
while(i != 1):
    #step2 - selection
    #List with the respective probability for each element in population to be selected for matching
    selectionProb = selectionProbabilities(population)
    print(selectionProb)
    #Criar intervalos, gerar random numbers NUMBER_OF_CROMOSSOMES times, emparelhar esses, cruzal-los, mutá-los 
    i+=1







