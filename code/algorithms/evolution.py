from classes.model import Model
from algorithms.runrandom import runRandom
import random
import itertools

# define constants/parameters
MAX_GENERATIONS = 1
POP_SIZE = 4

def evolution(env):    

    # initialize variable to store best score
    bestModel = runRandom(env)
    
    # amount of houses
    houses = env.houses

    # generate an initial population
    population = generateInitialPop(env)
    print("best initial: " + str(bestModel.cost))

    # check for optimum
    bestModel = searchForOptimum(population, bestModel)
    
    # reproduce
    for i in range(0, MAX_GENERATIONS):
        children = reproduce(population, env)
        bestModel = searchForOptimum(children, bestModel)
        newGeneration = population + children
        population = selection(newGeneration)
    
    # print score
    print("best later: " + str(bestModel.cost))
    return bestModel
 
def generateInitialPop(env):
    population = []
    for i in range(0, POP_SIZE):
        population.append(runRandom(env))
        # print("cost of population item " + str(i) + ": " + str(population[i].cost))
    return population

# kan dit efficienter?
# check if a new best solution is found, store that one 
def searchForOptimum(population, bestModel):

    # sort population by cost (lowest to highest)
    sortedPopulation = sorted(population, key=lambda x: x.cost, reverse=False)

    # compare lowest cost to lowest stored cost, save best
    if sortedPopulation[0].cost < bestModel.cost:
        return sortedPopulation[0]
    else:
        return bestModel

def reproduce(population, env):
    newChildren = []
    partnerOptions = list(range(len(population)))

    # randomly determine couples
    partners = []
    for i in range(0, int(len(population)/2)):
        lenListX = list(range(len(partnerOptions)))
        xDet = random.choice(lenListX)
        x = partnerOptions.pop(xDet)
        lenListY = list(range(len(partnerOptions)))
        yDet = random.choice(lenListY)
        y = partnerOptions.pop(yDet)
        partners.append([x,y])

    # make babies for every couple
    for i in range (0, len(partners)):
        print("partners")
        print(partners)
        print("i = ")
        print(i)
        couple = partners[i]
        xModel = population[couple[0]] 
        yModel = population[couple[1]]

        # convert parents to chromosomes
        chromosomeX = modelToChromosome(xModel)
        chromosomeXcopy = modelToChromosome(xModel)
        chromosomeY = modelToChromosome(yModel)
        chromosomeYcopy = modelToChromosome(yModel)

        chromosomeChildX, chromosomeChildY = fertilize(chromosomeX, chromosomeY)

        # back to child 
        childX = chromosomeToModel(chromosomeChildX, env)
        childY = chromosomeToModel(chromosomeChildY, env)    

        print(childX.cost)
        newChildren.append(childX) 

    print("newChildren")
    print(newChildren)        
    return newChildren

# chance still has to be incorporated in this
def selection(newGeneration):
    newGenerationSorted = sorted(newGeneration, key=lambda x: x.cost, reverse=False)
    selection = []
    for i in range(0,POP_SIZE):
        selection.append(newGenerationSorted[i])
    return selection

# methods belong to reproduction
def modelToChromosome(model):
    chromosome = []*150
    for bat in model.modelBatteries:
        for house in bat.houses:
            chromosome.append([house.idHouse, bat.idBattery])
    
    # random.shuffle(chromosome)
    print("length chromosome")
    print(len(chromosome))
    print(chromosome)
    return chromosome

def chromosomeToModel(chromosome, env):

        # create the array of batteries with the id starting at 1
        modelBatteries = []
        for i in range (0,len(env.batteries)):
            battery = Model.Battery(i+1)
            modelBatteries.append(battery)

         # create child model
        newModel = Model(modelBatteries)

        # fill list of houses belonging to battery in new model according to chromosome
        for gene in chromosome:
            house = env.houses[gene[0]-1]
            newModel.modelBatteries[gene[1]-1].houses.append(house)
        
        newModel.calculateCosts(env.distanceTable)
        return newModel

def fertilize(chromosomeX, chromosomeY):
    chromosomeXcopy = chromosomeX
    chromosomeYcopy = chromosomeY
         
    # copy first half of genes to child
    chromosomeChildX = []*150
    chromosomeChildY = []*150

    ## !!
    print("length!")
    print(len(chromosomeX))
    fromOtherParentX = list(range(1,len(chromosomeX)+2))
    fromOtherParentY = list(range(1,len(chromosomeX)+2))
        
    for gene in range(0, int(len(chromosomeX)/2)):
        # child parent X
        # pick first item from shuffled list      
        randomGeneX = chromosomeX[0]
        chromosomeX.pop(0)              
        fromOtherParentX[randomGeneX[0]-1] = 0            
        chromosomeChildX.append(randomGeneX)
        
        # child parent Y
        randomGeneY = chromosomeY[0]
        chromosomeY.pop(0)             
        fromOtherParentY[randomGeneY[0]-1] = 0            
        chromosomeChildY.append(randomGeneY)

    # copy second half to child
    # child parent X
    for housenr in fromOtherParentX:            
        for geneY in chromosomeYcopy:
            if (geneY[0] == housenr):
                chromosomeChildX.append(geneY)

    # child parent Y
    for housenr in fromOtherParentY:            
        for geneX in chromosomeXcopy:
            if (geneX[0] == housenr):
                chromosomeChildY.append(geneX)        
    # chromosomeChildX.sort(key=lambda tup: tup[0])

    # check newly added genes regarding contraints   

    # adaptive mutation

    return chromosomeChildX, chromosomeChildY