from classes.model import Model
from algorithms.runrandom import runRandom
import random
import itertools

def evolutionNoCon(env, maxGenerations, popSize):    
  
    # generate an initial population
    population = generateInitialPop(env, popSize)
    
    # initialize variable to store best score
    # runRandom is just for initialization
    bestModel = runRandom(env)
    bestModel = searchForOptimum(population, bestModel, env)

    for i in range(0, maxGenerations):
        print(i)
        # create children by crossover
        children = reproduce(population, env)

        # check if a new best model has been made (a valid one)
        bestModel = searchForOptimum(children, bestModel, env)

        # # try to make children valid with a hillclimber
        # children = adaptiveMutation(children, env)

        # the new generation consists of both parents and children
        newGeneration = population + children

        # select the best based on fitness score to keep population size constant
        population = selection(newGeneration, popSize)
    
    # search for optimum in final population
    bestModel = searchForOptimum(population, bestModel, env)

    return bestModel

# def checkValidity(env, model):
#     # print("houses per battery:")
#     # for battery in model.modelBatteries:
#     #     print(len(battery.houses))
   
#     for i in range(0, len(model.modelBatteries)):
#         totCapHouses = 0
#         for house in model.modelBatteries[i].houses:
#             totCapHouses += house.cap
#         # print("cap Battery")
#         # print(env.batteries[i].maxCapacity)
        
#         # print("cap Houses")
#         # print(totCapHouses)

#         # break out of loop and return False if capacity of battery is exceeded
#         if totCapHouses > env.batteries[i].maxCapacity:
#             return False
#     # if capacity is not exceeded in any battery, return True
#     return True

def generateInitialPop(env, popSize):
    population = []
    for i in range(0, popSize):
        population.append(runRandom(env))
        # print("cost of population item " + str(i) + ": " + str(population[i].cost))
    return population

# check if a new best (valid!) solution is found, store that one 
def searchForOptimum(population, bestModel, env):

    # sort population by cost (lowest to highest)
    sortedPopulation = sorted(population, key=lambda x: x.cost, reverse=False)

    # check if lowest cost is low enough to be new best score

    if sortedPopulation[0].cost < bestModel.cost:
        # if so return best
        return sortedPopulation[0]
    else:
        # if not, return previous
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
        couple = partners[i]
        xModel = population[couple[0]] 
        yModel = population[couple[1]]

        # convert parents to chromosomes
        chromosomeX = modelToChromosome(xModel)
        chromosomeXcopy = modelToChromosome(xModel)
        chromosomeY = modelToChromosome(yModel)
        chromosomeYcopy = modelToChromosome(yModel)

        chromosomeChildX, chromosomeChildY = fertilize(chromosomeX, chromosomeXcopy, chromosomeY, chromosomeYcopy)

        # back to child 
        childX = chromosomeToModel(chromosomeChildX, env)
        childY = chromosomeToModel(chromosomeChildY, env)    

        newChildren.append(childX) 
        newChildren.append(childY) 
        
    return newChildren

# fitness proportionate selection
def selection(newGeneration, popSize):
    selection = []

    # calculate sum of fitness
    totalCost = 0
    for model in newGeneration:
        totalCost += model.cost

    # create a array that indicates the intervals of probabilities
    propList = []
    previousProp = 0
    for model in newGeneration:
        prop = previousProp + model.cost/totalCost
        propList.append(prop)
        previousProp = prop

    # get random value and locate corresponding model
    for i in range(0, popSize):         
        value = random.random() 

        found = False
        for j in range(0, len(propList)):
            if found == False: 
                value -= propList[j]
                if value < 0:
                    selection.append(newGeneration[j])
                    found = True; 
    return selection

        
# methods belong to reproduction
def modelToChromosome(model):
    chromosome = []*150
    for bat in model.modelBatteries:
        for house in bat.houses:
            chromosome.append([house.idHouse, bat.idBattery])
    
    random.shuffle(chromosome)
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

def fertilize(chromosomeX, chromosomeXcopy, chromosomeY, chromosomeYcopy):
    z = sorted(chromosomeX, key=lambda tup: tup[0])
         
    # copy first half of genes to child
    chromosomeChildX = []*150
    chromosomeChildY = []*150

    fromOtherParentX = list(range(1,len(chromosomeX)+1))
    fromOtherParentY = list(range(1,len(chromosomeX)+1))
        
    for gene in range(0, int(len(chromosomeX)/2)):
        # child parent X
        # pick first item from shuffled list      
        randomGeneX = chromosomeX[0]
        chromosomeX.pop(0)              

        # remove gene from the "still has to be added" list
        fromOtherParentX[randomGeneX[0]-1] = 0   
        # add chosen gene to child         
        chromosomeChildX.append(randomGeneX)
                
        # child parent Y
        randomGeneY = chromosomeY[0]
        chromosomeY.pop(0)             

        # remove gene from the "still has to be added" list
        fromOtherParentY[randomGeneY[0]-1] = 0            
        chromosomeChildY.append(randomGeneY)


    # copy second half to child
    # add the house nrs that are not included yet 
    # child parent X
    for housenr in fromOtherParentX:            
        for geneY in chromosomeYcopy:
            if (geneY[0] == housenr):
                chromosomeChildX.append(geneY)


    # chromosomeChildY = chromosomeChildX
    # child parent Y
    for housenr in fromOtherParentY:            
        for geneX in chromosomeXcopy:
            if (geneX[0] == housenr):
                chromosomeChildY.append(geneX)        
    # chromosomeChildX.sort(key=lambda tup: tup[0])

      # adaptive mutation


    return chromosomeChildX, chromosomeChildY

def adaptiveMutation(individuals, env):
    for model in individuals:
        print(model.checkValidity(env))
        # attempt to improve non valid model with hillclimber
        if model.checkValidity(env) == False:
            shadowModel = adapt(model)
            count = 0 

            # as long as no better model is found:
            while not shadowModel.checkValidity(env) == True and count < 1000:
                count += 1
                shadowModel = adapt(model)

                # make three switches on the same model, check in between 
                shortSwitchCount = 0
                while not shadowModel.checkValidity(env) == True and shortSwitchCount < 10:
                    shortSwitchCount += 1
                    shadowModel = adapt(shadowModel)
                    if shadowModel == True:
                        print("Adapted to true!")
                        model = shadowModel                              
    return individuals
        

def adapt(model):

    # get the batteries from the model
        batteries = model.modelBatteries

        # get a random battery
        randomBatteries =(random.randint(0, len(batteries)-1), random.randint(0, len(batteries)-1))

        # set the upperbounds for the houses randomizer
        setUpperboundBattery1 = len(batteries[randomBatteries[0]].houses)
        setUpperboundBattery2 = len(batteries[randomBatteries[1]].houses)

        # get a random house
        randomHouses = (random.randint(0, (setUpperboundBattery1 - 1)), random.randint(0, (setUpperboundBattery2 - 1)))

        # get the houses on the random places
        house1 = batteries[randomBatteries[0]].houses[randomHouses[0]]
        house2 = batteries[randomBatteries[1]].houses[randomHouses[1]]

        # switch the houses with each other
        batteries[randomBatteries[0]].houses[randomHouses[0]] = house2
        batteries[randomBatteries[1]].houses[randomHouses[1]] = house1

        # return the model
        returnModel = Model(batteries)
        return returnModel