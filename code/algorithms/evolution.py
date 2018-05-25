from classes.model import Model
from algorithms.runrandom import runRandom
import math
import random
import itertools
import sys 
import copy
import time
import datetime
import csv

def evolution(env, maxGenerations, popSize, birthsPerCouple, matingPartners, parentDominance):   
    
    # check if population size is at least 2 at a small popSize there's a risk of killing every child
    if popSize < 2:
        print("The population must at least have size 2")
    
    # create unique name for report
    reportFileName = "run_evolution_" + "v" + str(env.village) + "_" + str(int(time.time())) + ".csv"

    # print info
    writeProgress(reportFileName, "NEW RUN")
    writeProgress(reportFileName, "Village " + str(env.village))
    info = "maxGen = " + str(maxGenerations) + ", popSize = " + str(popSize) + ", birthsPerCouple = " + str(birthsPerCouple) + ", matingPartners = " + str(matingPartners) + ", parentDominance = " + str(parentDominance)
    writeProgress(reportFileName, info)

    # generate an initial population
    population = generateInitialPop(env, popSize)
     
    # initialize variable to store best score
    # runRandom is just for initialization
    bestModel = runRandom(env)
    bestModel = searchForOptimum(population, bestModel, reportFileName, env)

    # loop through reproduction progress while scanning for solution
    for i in range(0, maxGenerations):

        # print time
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        update = "At " + str(st) + " - giving birth to generation " + str(i)
        writeProgress(reportFileName, update)
        

        # create children by crossover
        children = []
        for j in range(0, matingPartners):
            children += reproduce(population, env, parentDominance, birthsPerCouple)

        if children is not None:

            # check if a new best model has been made (a valid one)
            bestModel = searchForOptimum(children, bestModel, reportFileName, env)

            # the new generation consists of both parents and children
            newGeneration = population + children

            # select the best based on fitness score to keep population size constant
            population = selection(newGeneration, popSize)
    
    writeProgress(reportFileName, "FINISH")
    return bestModel

def generateInitialPop(env, popSize):
    population = []
    for i in range(0, popSize):
        population.append(runRandom(env))

    return population

# check if a new best (valid!) solution is found, store that one 
def searchForOptimum(population, bestModel, reportFileName, env):

    # sort population by cost (lowest to highest)
    sortedPopulation = sorted(population, key=lambda x: x.cost, reverse=False)

    # take individual with lowest score
    possibleBestModel = sortedPopulation[0]
    
    # if the model cost exceeds upper bound the next once will so too therefore do no update bestModel
    if possibleBestModel.cost < bestModel.cost:

        # if model's costs are lower, inform the user
        message = "New improvement detected: " + str(possibleBestModel.cost)
        writeProgress(reportFileName, message)
        writeProgress(reportFileName, str(modelToChromosome(possibleBestModel, True)))
        possibleBestModel.write(env)

        # and update model
        return possibleBestModel

    # if all models had a lower score, but none were valid
    else:
        return bestModel

# merge half of both chromosomes to create new chromosome (may result in invalid child)
def reproduce(population, env, parentDominance, birthsPerCouple):
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
        chromosomeX = modelToChromosome(xModel, False)
        chromosomeY = modelToChromosome(yModel, False)

        # create children 
        newChildren = createChildren(chromosomeX, chromosomeY, parentDominance, birthsPerCouple, env)       
    return newChildren

def createChildren(chromosomeX, chromosomeY, parentDominance, birthsPerCouple, env):
    unviableChildren = []
    for i in range(0, birthsPerCouple):
        chromosomeChildX, genesToCheckX = fertilize(chromosomeX, chromosomeY, parentDominance)
        chromosomeChildY, genesToCheckY = fertilize(chromosomeY, chromosomeX, parentDominance)

        # convert children back to type model
        childX = chromosomeToModel(chromosomeChildX, env) 
        childY = chromosomeToModel(chromosomeChildY, env)  

        unviableChildren.append({'chromosome': childX, 'genesToCheck': genesToCheckX})
        unviableChildren.append({'chromosome': childY, 'genesToCheck': genesToCheckY})
    
    viableChildren = []
    for children in unviableChildren:
        birth = makeViable(children['chromosome'], children['genesToCheck'], env)
        if birth is not None:
            viableChildren.append(birth)
    return viableChildren


def makeViable(child, genesToCheck, env):

    # conflict resolvement after fertilization, make child viable check in advance is not necessary, since without conflict resolvement child is not viable
    newChild = resolveConflict(child, genesToCheck, env)

    # if conflict resolvement does not lead to a viable child, try again up to 100 times
    count = 0
    while newChild is None and count<300:
        count += 1
        newChild = resolveConflict(child, genesToCheck, env)

    # if conflict resolvement does not lead to a viable child, try again up to 100 times
    if newChild is not None:
        
        return newChild

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

    # assign free houses to closest battery with free capacity
    for i in range(0, len(freeHouses)):

        # retrieve house object to place
        for house in env.houses: 
            if house.idHouse == freeHouses[i]:
                houseToPlace = house
                
        # rank preference for batteries of this house on distance
        freeBatteries = []
        for battery in temp_child.modelBatteries:

            # retrieve distance to specific house
            distance = env.distanceTable[houseToPlace.idHouse][battery.idBattery]

            # put in list
            freeBatteries.append([battery.idBattery, distance])
        
        # sort list of batteries to pick from on distance
        freeBatteries = sorted(freeBatteries, key=lambda tup: tup[1])

        # as long as house is not assigned:
        free = True
        while (free): 
            try:        
                # pick first battery from options
                batteryIndex = freeBatteries[0][0]-1

                # if capacity of battery is enough to assign house
                if (temp_child.modelBatteries[batteryIndex].checkCapacity(env.batteries, houseToPlace)):

                    # assign house
                    temp_child.modelBatteries[batteryIndex].houses.append(houseToPlace)
                    free = False

                # otherwise remove battery from list of options
                else:
                    freeBatteries.pop(0)

            except IndexError:

                # if solution doesn't fit, try again in different order
                return 

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
def modelToChromosome(model, sort):
    chromosome = []*150
    for bat in model.modelBatteries:
        for house in bat.houses:
            chromosome.append([house.idHouse, bat.idBattery])
    
    if sort == True:
        chromosome = sorted(chromosome, key=lambda tup: tup[0])
    
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
        return newModel

def fertilize(chromosomeX, chromosomeY, parentDominance):

    chromTempX = copy.deepcopy(chromosomeX)
    chromTempY = copy.deepcopy(chromosomeY)

    # initialize arrays 
    chromosomeChild = []*150
    fromOtherParent = list(range(1,len(chromTempX)+1))
        
    # copy first share of genes to child
    random.shuffle(chromTempX)

    for geneIndex in range(0, int(len(chromTempX)/(1/parentDominance))):

        # pick item from shuffled list 
        randomGene = chromTempX[geneIndex]  

        # remove gene from the "still has to be added" list
        fromOtherParent.remove(randomGene[0])

        # add chosen gene to child         
        chromosomeChild.append(randomGene)              

    # copy second half to child and add the house nrs that are not included yet 
    fromOtherParentTuples = []

    for housenr in fromOtherParent:            
        for geneY in chromTempY:
            if (geneY[0] == housenr):
                chromosomeChild.append(geneY)     
                fromOtherParentTuples.append(geneY)              

    return chromosomeChild, fromOtherParentTuples

def writeProgress(reportFileName, message):
    filePathName = "..\\results\personalresults\\" + reportFileName

    with open(filePathName,'a', newline='') as f:
        writer = csv.writer(f)
        print(message)
        writer.writerow([message])

        

