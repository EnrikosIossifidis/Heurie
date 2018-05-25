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

def evolution(env, maximumGenerations, populationSize, crossoversPerParent, matingPartners, parentDominance, mutationProbability, crossoverProbability):   
    
    # check if population size is at least 2
    # at a small popSize there's a risk of killing every child
    if populationSize < 2:
        print("The population must at least have size 2")
    
    # create unique name for report
    reportFileName = "run_evolution_" + "v" + str(env.village) + "_" + str(int(time.time())) + ".txt"

    # print info
    writeProgress(reportFileName, "NEW RUN \nVillage " + str(env.village))
    info = "maxGen = " + str(maximumGenerations) + ", popSize = " + str(populationSize) + ", crossoversPerParent = " + str(crossoversPerParent) + ", matingPartners = " + str(matingPartners) + ", parentDominance = " + str(parentDominance) + ", mutationProb = " + str(mutationProbability) + ", crossoverProb = " + str(crossoverProbability)
    writeProgress(reportFileName, info)

    # generate an initial population
    population = generateInitialPop(env, populationSize)
     
    # initialize variable to store best score
    # runRandom is just for initialization
    bestModel = runRandom(env)
    bestModel = searchForOptimum(population, bestModel, reportFileName, env)

    # loop through reproduction progress while scanning for solution
    for i in range(0, maximumGenerations):

        # print time
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        update = "At " + str(st) + " - giving birth to generation " + str(i) + "\npopSize: " + str(len(population))
        writeProgress(reportFileName, update)
        
        # create children by crossover
        children = []
        for j in range(0, matingPartners):
            children += reproduce(population, env, parentDominance, crossoversPerParent, mutationProbability, crossoverProbability)

        # check if
        if children is not None:
            # check if empty
            if len(children) != 0:

                # check if a new best model has been made (a valid one)
                bestModel = searchForOptimum(children, bestModel, reportFileName, env)

                # the new generation consists of both parents and children
                newGeneration = children

                # select the best based on fitness score to keep population size constant
                population = selection(newGeneration, populationSize)

            if len(children) == 0:
                print('no new children')

        if children is None:
            print('no new children')
    
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
    
    # if the model cost exceeds upper bound the next once will so too
    # therefore do no update bestModel
    if possibleBestModel.cost < bestModel.cost:

        # if model's costs are lower:
        # inform user
        message = "New improvement detected: " + str(possibleBestModel.cost)
        writeProgress(reportFileName, message)
        possibleBestModel.write(env)

        # and update model
        return possibleBestModel

    # if all models had a lower score, but none were valid
    else:
        return bestModel

# merge half of both genomes to create new genome (may result in invalid child)
def reproduce(population, env, parentDominance, crossoversPerParent, mutationProbability, crossoverProbability):
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

        # convert parents (of type model) to type genome
        genomeX = modelToGenome(xModel, False)
        genomeY = modelToGenome(yModel, False)

        # create children 
        newChildren = createChildren(genomeX, genomeY, parentDominance, crossoversPerParent, env, mutationProbability, crossoverProbability)       
    return newChildren

def createChildren(genomeX, genomeY, parentDominance, crossoverPerParent, env, mutationProb, crossoverProb):
    # perform crossover
    unviableChildren = []
    for i in range(0, crossoverPerParent):
        genomeChildX, genesToCheckX = crossover(genomeX, genomeY, parentDominance, crossoverProb)
        genomeChildY, genesToCheckY = crossover(genomeY, genomeX, parentDominance, crossoverProb)

        # convert children back to type model
        childX = genomeToModel(genomeChildX, env) 
        childY = genomeToModel(genomeChildY, env)  

        unviableChildren.append({'genome': childX, 'genesToCheck': genesToCheckX})
        unviableChildren.append({'genome': childY, 'genesToCheck': genesToCheckY})
    
    # mutate children based on mutationProb
    for child in unviableChildren:
        if mutationProb > random.random():
            mutant = mutation(child['genome'], env)
            child['genome'] = mutant

    # # perform mututions to resolve conflicts with constraints
    # viableChildren = []
    # for children in unviableChildren:
    #     birth = makeViable(children['genome'], children['genesToCheck'], env)
    #     if birth is not None:
    #         viableChildren.append(birth)

    # # convert not mathcing constraints
    viableChildren = []
    for children in unviableChildren:
        birth = children['genome']
        if birth is not None:
            viableChildren.append(birth)

    return viableChildren


def makeViable(child, genesToCheck, env):
    # conflict resolvement after fertilization, make child viable 
    # check in advance is not necessary, since without conflict resolvement child is not viable
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
                # solution not garantueed?
                # print("total houses = {}".format(sum([len(x.houses) for x in temp_child.modelBatteries])))
                return 

    return temp_child
# fitness proportionate selection
def selection(newGeneration, popSize):
    
    selection = []
    print("population size before selection:", len(newGeneration))


    # choose fitness function: LowHighScale, TotalCostScale, CostRank
    fitnessList = fitnessLowHighScale(newGeneration)

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
                    
    print("population size after selection:", len(selection))
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
    genomeFitnesses = fitnessTotalCostScale(newGeneration)
    length = len(genomeFitnesses)
    totalranks = 0
    fitnessList = []

    # calculate fitness of each model by subtracting cullumative element
    for i in range(0, length):
        if i == 0:
            fitnessList.append([genomeFitnesses[i][0] - genomeFitnesses[i][0], i + 1])
        fitnessList.append([genomeFitnesses[i][0] - genomeFitnesses[i - 1][0], i + 1])
        totalranks += i

    # recalculate models so that the scores fit between 0 and 1
    fitnessList[0][0] = fitnessList[0][0] / totalranks
    for k in range(1, length):
        fitnessList[k][0] = fitnessList[k - 1][0] + (1 - ((k + 1) / totalranks))
    
    # total value fitnessList == population - 1 because the worst model is value 0
    return fitnessList
        
# converts model class to genome format
def modelToGenome(model, sort):
    genome = []*150
    for bat in model.modelBatteries:
        for house in bat.houses:
            genome.append([house.idHouse, bat.idBattery])
    
    if sort == True:
        genome = sorted(genome, key=lambda tup: tup[0])
    
    return genome

# convert object of type genome to model class
def genomeToModel(genome, env):

        # create the array of batteries with the id starting at 1
        modelBatteries = []
        for i in range (0, len(env.batteries)):
            battery = Model.Battery(i+1)
            modelBatteries.append(battery)

         # create child model
        newModel = Model(modelBatteries)

        for battery in newModel.modelBatteries:
            battery.setMaxCapacity(env)

        # fill list of houses belonging to battery in new model according to genome
        for gene in genome:
            for house in env.houses:
                if house.idHouse == (gene[0]):
                    corHouse = house
                    newModel.modelBatteries[gene[1]-1].houses.append(corHouse)

        newModel.calculateCosts(env.distanceTable)

        # print(sorted([x.idHouse for x in newModel.modelBatteries[0].houses], key=lambda x:x))
   
        return newModel

def crossover(genomeX, genomeY, parentDominance, crossoverProb):
    # check if a crossover should occur for this pair
    if crossoverProb > random.random():

        # initialize arrays 
        genomeChild = []*150
        fromOtherParent = list(range(1,len(genomeX)+1))
            
        # copy first share of genes to child
        random.shuffle(genomeX)

        for geneIndex in range(0, int(len(genomeX)/(1/parentDominance))):

            # pick item from shuffled list 
            randomGene = genomeX[geneIndex]  

            # remove gene from the "still has to be added" list
            fromOtherParent.remove(randomGene[0])

            # add chosen gene to child         
            genomeChild.append(randomGene)              

        # copy second half to child
        # add the house nrs that are not included yet 
        fromOtherParentTuples = []

        for housenr in fromOtherParent:            
            for geneY in genomeY:
                if (geneY[0] == housenr):
                    genomeChild.append(geneY)     
                    fromOtherParentTuples.append(geneY)              

        return genomeChild, fromOtherParentTuples
    
    else:
        return genomeX, []

def writeProgress(reportFileName, message):
    filePathName = "..\\results\personalresults\\logs\\" + reportFileName

    message = "-----------------\n" + message

    with open(filePathName,'a', newline='') as f:
        writer = csv.writer(f, escapechar = ' ', quoting=csv.QUOTE_NONE)
        print(message)
        writer.writerow([message])

def mutation(model, env):
    newModel = switchGenes(model)  
    newModel.calculateCosts(env.distanceTable)
    return newModel

def switchGenes(model):

    # get the batteries from themodel
    batteries = model.modelBatteries

    # get a random battery
    randomBattery1 = random.randint(0, 4)
    randomBattery2 = random.randint(0, 4)

    # set the upperbounds for the houses randomizer
    setUpperboundBattery1 = 0
    setUpperboundBattery1 = len(batteries[randomBattery1].houses)
    setUpperboundBattery2 = 0
    setUpperboundBattery2 = len(batteries[randomBattery2].houses)

    # get a random house
    randomHouse1 = random.randint(0, (setUpperboundBattery1 - 1))
    randomHouse2 = random.randint(0, (setUpperboundBattery2 - 1))

    # get the houses on the random places
    house1 = batteries[randomBattery1].houses[randomHouse1]
    house2 = batteries[randomBattery2].houses[randomHouse2]

    # switch the houses with each other
    batteries[randomBattery1].houses[randomHouse1] = house2
    batteries[randomBattery2].houses[randomHouse2] = house1

    # return the model
    returnModel = Model(batteries)
    return returnModel




        

