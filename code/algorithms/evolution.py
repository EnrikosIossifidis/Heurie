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
    print("best initial: " + str(bestModel.cost))
    # generate an initial population
    population = generateInitialPop(env)

    # check for optimum
    bestModel = searchForOptimum(population, bestModel)
    print("best later: " + str(bestModel.cost))

    # calculate fitness

    # reproduce
    for i in range(0, MAX_GENERATIONS):
        children = reproduce(population)
        bestModel = searchForOptimum(children, bestModel)
        newGeneration = population + children
        population = selection(newGeneration)
 
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
    newPopulation = []
    partnerOptions = list(range(len(population)))
    print(partnerOptions)

    # randomly determine couples
    partners = []
    for i in range(0, 9):
        x = partnerOptions.pop(random.choice(partnerOptions))
        print(x)
        print(partnerOptions)
        y = partnerOptions.pop(random.choice(partnerOptions))
        print(y)
        print(partnerOptions)
        partners.append([x,y])
    print(partners)


    # partners = [[1,2],[3,4],[5,6],[7,8],[9,10]]
    # print(partners)
    
    # make babies for every couple
    for i in range (0, len(partners)):
        couple = partners[i]
        print(couple[0])
        # xModel = population(couple[0]) 
        # yModel = population(couple[1])  
        newPopulation.append(population[0])

    return newPopulation

# chance still has to be incorporated in this
def selection(newGeneration):
    newGenerationSorted = sorted(newGeneration, key=lambda x: x.cost, reverse=False)
    selection = []
    for i in range(0,POP_SIZE):
        selection.append(newGenerationSorted[i])
    return selection




