from classes.model import Model
from algorithms.runrandom import runRandom
import random
import itertools

# define constants/parameters
MAX_GENERATIONS = 10
POP_SIZE = 10

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
        children = reproduce(population)
        bestModel = searchForOptimum(children, bestModel)
        newGeneration = population + children
        population = selection(newGeneration)
    
    # print score
    print("best later: " + str(bestModel.cost))
 
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

def reproduce(population):
    newChildren = []
    partnerOptions = list(range(len(population)))

    # randomly determine couples
    partners = []
    for i in range(0, 5):
        lenListX = list(range(len(partnerOptions)))
        xDet = random.choice(lenListX)
        x = partnerOptions.pop(xDet)
        lenListY = list(range(len(partnerOptions)))
        yDet = random.choice(lenListY)
        y = partnerOptions.pop(yDet)
        partners.append([x,y])

    # make babies for every couple
    for i in range (0, len(partners)):
        couple = partners[i]
        xModel = population[couple[0]] 
        yModel = population[couple[1]]
        newChildren.append(xModel)  

        # convert model to chromosomeX
        chromosomeX = []*150
        for bat in xModel.modelBatteries:
            for house in bat.houses:
                chromosomeX.append([house.idHouse, bat.idBattery])

        # sort chromosome by house id        
        chromosomeX.sort(key=lambda tup: tup[0])      

        # convert model to chromosomeY
        chromosomeY = []*150
        for bat in xModel.modelBatteries:
            for house in bat.houses:
                chromosomeY.append([house.idHouse, bat.idBattery])
        
        # sort chromosome by house id    
        chromosomeY.sort(key=lambda tup: tup[0])    

        # copy first half to child
        chromosomeChildX = []*150
        chromosomeChildY = []*150

        fromOtherParentX = list(range(1,151))
        fromOtherParentY = list(range(1,151))
                
        for gene in range(0, 74):
            randomGeneX = random.choice(chromosomeX)           
            fromOtherParentX[randomGeneX[0]-1] = 0            
            chromosomeChildX.append(randomGeneX)
            
            randomGeneX = random.choice(chromosomeX)           
            fromOtherParentX[randomGeneX[0]-1] = 0            
            chromosomeChildX.append(randomGeneX)

        # copy second half to child
        for gene in range(0, 74):
            randomGeneX = random.choice(chromosomeX)           
            fromOtherParentX[randomGeneX[0]-1] = 0            
            chromosomeChildX.append(randomGeneX)


            


    return newChildren

# chance still has to be incorporated in this
def selection(newGeneration):
    newGenerationSorted = sorted(newGeneration, key=lambda x: x.cost, reverse=False)
    selection = []
    for i in range(0,POP_SIZE):
        selection.append(newGenerationSorted[i])
    return selection
