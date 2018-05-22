from classes.model import Model
from algorithms.runrandom import runRandom
import math
import random
import itertools
import sys 
import copy

def evolution(env, maxGenerations, popSize, birthRate, parentDominance):    
  
    # generate an initial population
    population = generateInitialPop(env, popSize)
    
    # initialize variable to store best score
    # runRandom is just for initialization
    bestModel = runRandom(env)
    bestModel = searchForOptimum(population, bestModel, env)


    for i in range(0, maxGenerations):

        # create children by crossover
        children = []
        for j in range(0, birthRate):
            children += reproduce(population, env, parentDominance)

        # check if a new best model has been made (a valid one)
        bestModel = searchForOptimum(children, bestModel, env)

        # # try to make children valid with a hillclimber
        # children = adaptiveMutation(children, env)

        # the new generation consists of both parents and children
        newGeneration = population + children

        # select the best based on fitness score to keep population size constant
        population = selection(newGeneration, popSize)
    
    return bestModel

def generateInitialPop(env, popSize):
    population = []
    for i in range(0, popSize):
        population.append(runRandom(env))

    return population

# check if a new best (valid!) solution is found, store that one 
def searchForOptimum(population, bestModel, env):

    # sort population by cost (lowest to highest)
    sortedPopulation = sorted(population, key=lambda x: x.cost, reverse=False)

    # keep checking for bestModel in sortedPopulation unless cost is too high anyway
    for model in sortedPopulation:
        
        # if the model cost exceeds upper bound the next once will so too
        # therefore do no update bestModel
        if model.cost > bestModel.cost:
            return bestModel

        # if model's costs are lower, check if solution is valid
        else: 
            if model.checkValidity() == True:
                # if so, update bestModel
                return model

    # if all models had a lower score, but none were valid
    return bestModel

# merge half of both chromosomes to create new chromosome (may result in invalid child)
def reproduce(population, env, parentDominance):
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
        chromosomeY = modelToChromosome(yModel)

        # create children 
        chromosomeChildX, genesToCheckX = fertilize(chromosomeX, chromosomeY, parentDominance)
        chromosomeChildY, genesToCheckY = fertilize(chromosomeY, chromosomeX, parentDominance)

        # convert child back to type model
        childX = chromosomeToModel(chromosomeChildX, env)
   
        # childY = chromosomeToModel(chromosomeChildY, env)   

        # conflict resolvement after fertilization, make child viable 
        # check in advance is not necessary, since without conflict resolvement child is not viable
        newChild = resolveConflict(childX, genesToCheckX, env)

        # if conflict resolvement does not lead to a viable child, try again up to 100 times
        count = 0
        while newChild is None and count<1000:
            count += 1
            newChild = resolveConflict(childX, genesToCheckX, env)

        # if conflict resolvement does not lead to a viable child, try again up to 100 times
        if newChild is not None:
            newChildren.append(newChild) 
        else:
            print("KILL")

    return newChildren

def resolveConflict(child, genesToCheck, env):
    freeHouses = []
    random.shuffle(genesToCheck)

    temp_child = copy.deepcopy(child)

    # check which houses exceeds battery's maximum capacity, and disconnect those from battery
    for gene in genesToCheck:
        # if overloaded
        if (temp_child.modelBatteries[gene[1]-1].checkOverload()):
            
            # remove house from battery

            for house in temp_child.modelBatteries[gene[1]-1].houses:
                if house.idHouse == gene[0]:
                    temp_child.modelBatteries[gene[1]-1].houses.remove(house)


            # save houseID
            freeHouses.append(gene[0])

    # assign free houses to battery with free capacity
    for i in range(0, len(freeHouses)):
        free = True
        freeBatteries = list(range(len(temp_child.modelBatteries)))
        while (free): 
            try:        
                batteryIndex = random.choice(freeBatteries)
                house = env.houses[freeHouses[i]-1]
                
                # if capacity is enough to assign house
                if (temp_child.modelBatteries[batteryIndex].checkCapacity(env.batteries, house)):
                    # assign house
                    temp_child.modelBatteries[batteryIndex].houses.append(house)
                    free = False
                else:
                    freeBatteries.remove(batteryIndex)
            except IndexError:
                # if solution doesn't fit, try again in different order
                # solution not garantueed?
                # print("index error")
                # print("total houses = {}".format(sum([len(x.houses) for x in temp_child.modelBatteries])))
                return 
    temp_child.printDistributionHouses()
    return temp_child

# fitness proportionate selection
def selection(newGeneration, popSize):
    
    selection = []

    # choose fitness function: LowHighScale, TotalCostScale, CostRank
    fitnessList = fitnessCostRank(newGeneration)

    # get random value and locate corresponding model
    for i in range(0, popSize):         
        value = random.random() 
        found = False

        for j in range(0, len(fitnessList)):
            if found == False: 
                value -= fitnessList[j][0]

                # append chosen model to new population and recalculate the probality values
                if value < 0:
                    selection.append(newGeneration[fitnessList[j][1] - 1])
                    newGeneration.remove(newGeneration[fitnessList[j][1] - 1])
                    fitnessList = fitnessCostRank(newGeneration)
                    found = True
    for mo in selection:
        print(mo.cost)
    return selection

def fitnessLowHighScale(newGeneration):
  
    # calculate sum of fitness
    populationCost = []
    
    for i in range(0, len(newGeneration)):
        populationCost.append([newGeneration[i].cost, i + 1])

    # array of probalility intervals, normalized in range lowest and highest cost
    newGenLowHigh = [sorted(populationCost)[0][0], sorted(populationCost)[-1][0]]
    totalFitnessScore = 0
    fitnessList = []

    # calculate fitness for each model
    for i in range(0, len(populationCost)):
        fitness1 = 1 - (populationCost[i][0] - newGenLowHigh[0]) / (newGenLowHigh[1] - newGenLowHigh[0])
        populationCost[i][0] = fitness1
        totalFitnessScore += fitness1
        fitnessList.append(populationCost[i])
    
    # recalculate fitness so that scores are between 0 and 1
    fitnessList[0][0] = fitnessList[0][0] / totalFitnessScore
    for j in range(1, len(fitnessList)):
        fitnessList[j][0] = fitnessList[j - 1][0] + (fitnessList[j][0] / totalFitnessScore) 

    return fitnessList

def fitnessTotalCostScale(newGeneration):
    
    # calculate sum of fitness
    populationCost = []
    
    for i in range(0, len(newGeneration)):
        populationCost.append([newGeneration[i].cost, i + 1])

    totalCost = 0
    for model in populationCost:
        totalCost += model[0]

    # create a array that indicates the intervals of probabilities
    fitnessList = []
    previousProp = 0
    for model in populationCost:
        prop = previousProp + model/totalCost
        fitnessList.append(prop)
        previousProp = prop
    
    return fitnessList

def fitnessCostRank(newGeneration):
    
    # calculate scores with either CostScale or LowHighScale
    chromosomeFitnesses = fitnessTotalCostScale(newGeneration)
    length = len(chromosomeFitnesses)
    totalranks = 0
    fitnessList = []

    # calculate fitness of each model by subtracting cullumative element
    for i in range(0, length):
        if i == 0:
            fitnessList.append([chromosomeFitnesses[i][0] - chromosomeFitnesses[i][0], i + 1])
        fitnessList.append([chromosomeFitnesses[i][0] - chromosomeFitnesses[i - 1][0], i + 1])
        totalranks += i

    # recalculate models so that the scores fit between 0 and 1
    fitnessList[0][0] = fitnessList[0][0] / totalranks
    for k in range(1, length):
        fitnessList[k][0] = fitnessList[k - 1][0] + (1 - ((k + 1) / totalranks))
    
    # total value fitnessList == population - 1 because the worst model is value 0
    return fitnessList
        
# converts model class to chromosome format
def modelToChromosome(model):
    chromosome = []*150
    for bat in model.modelBatteries:
        for house in bat.houses:
            chromosome.append([house.idHouse, bat.idBattery])
    
    return chromosome

# converts chromosome format to model class
def chromosomeToModel(chromosome, env):

        # create the array of batteries with the id starting at 1
        modelBatteries = []
        for i in range (0, len(env.batteries)):
            battery = Model.Battery(i+1)
            modelBatteries.append(battery)

         # create child model
        newModel = Model(modelBatteries)

        for battery in newModel.modelBatteries:
            battery.setMaxCapacity(env)


        # fill list of houses belonging to battery in new model according to chromosome
        for gene in chromosome:
            for house in env.houses:
                if house.idHouse == (gene[0]):
                    corHouse = house
                    newModel.modelBatteries[gene[1]-1].houses.append(corHouse)

        newModel.calculateCosts(env.distanceTable)

        # print(sorted([x.idHouse for x in newModel.modelBatteries[0].houses], key=lambda x:x))
   
        return newModel

def fertilize(chromosomeX, chromosomeY, parentDominance):
    ## z = sorted(chromosomeX, key=lambda tup: tup[0])
        
    # initialize arrays 
    chromosomeChild = []*150
    fromOtherParent = list(range(1,len(chromosomeX)+1))
        
    # copy first share of genes to child
    random.shuffle(chromosomeX)

    for gene in range(0, int(len(chromosomeX)/(1/parentDominance))):
        
        # pick first item from shuffled list 
        randomGene = chromosomeX[gene]    

        # remove gene from the "still has to be added" list
        # fromOtherParent[randomGene[0]-1] = 0   
        fromOtherParent.remove(randomGene[0])

        # add chosen gene to child         
        chromosomeChild.append(randomGene)              

    # copy second half to child
    # add the house nrs that are not included yet 
    fromOtherParentTuples = []

    for housenr in fromOtherParent:            
        for geneY in chromosomeY:
            if (geneY[0] == housenr):
                chromosomeChild.append(geneY)     
                fromOtherParentTuples.append(geneY)              

    return chromosomeChild, fromOtherParentTuples

def adaptiveMutation(individuals, env):
    for model in individuals:
        # print(model.checkValidity(env))

        # attempt to improve non valid model with hillclimber
        if model.checkValidity(env) == False:
            shadowModel = adapt(model)
            count = 0 

            # as long as no better model is found:
            while not shadowModel.checkValidity(env) == True and count < 100:
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