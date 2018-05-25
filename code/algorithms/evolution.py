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

def evolution(env, maximumGenerations, populationSize, crossoversPerParent, matingPartners, parentDominance, mutationProbability, crossoverProbability, conflictResolvement):   
    
    # check if population size is at least 2
    # at a small popSize there's a risk of killing every child
    if populationSize < 2:
        print("Search is not possible: the population must at least have size 2")  
    else:  
          
        # create search id and log 
        timeIdStart =  int(time.time())
        reportFileName = "run_evolution_" + "v" + str(env.village) + "_" + str(timeIdStart) + ".txt"
        writeProgress(reportFileName, "NEW RUN \nVillage " + str(env.village))
        algorithmId = "maximumGenerations = " + str(maximumGenerations) + ", populationSize = " + str(populationSize) + ", crossoversPerParent = " + str(crossoversPerParent) + ", matingPartners = " + str(matingPartners) + ", parentDominance = " + str(parentDominance) + ", mutationProbability = " + str(mutationProbability) + ", crossoverProbability = " + str(crossoverProbability) + ", conflictResolvement = " + str(conflictResolvement)
        writeProgress(reportFileName, algorithmId)

        # generate an initial population
        population = generateInitialPop(env, populationSize)
        
        # search for best individual
        bestModel = population[0]
        bestModel = searchForOptimum(population, bestModel, reportFileName, env)

        # create new generations of children until maximum is reached 
        for i in range(0, maximumGenerations):

            # log
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            update = "At " + str(st) + " - giving birth to generation " + str(i) + "\npopSize: " + str(len(population))
            writeProgress(reportFileName, update)
            
            # create children by crossover
            children = []
            for j in range(0, matingPartners):
                children += reproduce(population, env, parentDominance, crossoversPerParent, mutationProbability, crossoverProbability, conflictResolvement)

            # check if empty
            if len(children) != 0:

                # check if a new best model has been made (a valid one)
                bestModel = searchForOptimum(children, bestModel, reportFileName, env)

                # select the best based on fitness score to keep population size constant
                population = selection(children, populationSize)

            if len(children) == 0:
                print('no new children')
        
        # log and save parameters to model
        writeProgress(reportFileName, "FINISH")
        bestModel.setName(algorithmId, timeIdStart)

        # return the best solution found
        return bestModel

def generateInitialPop(env, popSize):

    # initialize population
    population = []

    # append random individuals to population
    for i in range(0, popSize):
        population.append(runRandom(env))

    return population

# checks if a new best (valid!) solution is found, store that one 
def searchForOptimum(population, bestModel, reportFileName, env):

    # sort population by cost (lowest to highest)
    sortedPopulation = sorted(population, key=lambda x: x.cost, reverse=False)

    # take individual with lowest cost
    possibleBestModel = sortedPopulation[0]
    
    # check if cost is lower than found previously
    if possibleBestModel.cost < bestModel.cost:

        # if model's costs are lower, inform the user
        message = "New improvement detected: " + str(possibleBestModel.cost)
        writeProgress(reportFileName, message)

        # keep track of solutions in separate file 
        possibleBestModel.write(env)

        # update model
        return possibleBestModel

    # if all models had a lower score, but none were valid
    else:
        # do no update model
        return bestModel

# merges half of both genomes to create new genome 
def reproduce(population, env, parentDominance, crossoversPerParent, mutationProbability, crossoverProbability, conflictResolvement):  
 
    # randomly determine couples
    partnerOptions = list(range(len(population)))
    partners = []
    for i in range(0, int(len(population)/2)):
        lenListX = list(range(len(partnerOptions)))
        xDet = random.choice(lenListX)
        x = partnerOptions.pop(xDet)
        lenListY = list(range(len(partnerOptions)))
        yDet = random.choice(lenListY)
        y = partnerOptions.pop(yDet)
        partners.append([x,y])

    # make children for every couple
    newChildren = []
    for i in range (0, len(partners)):
        couple = partners[i]
        xModel = population[couple[0]] 
        yModel = population[couple[1]]

        # convert parents (of type model) to type genome
        genomeX = modelToGenome(xModel, False)
        genomeY = modelToGenome(yModel, False)

        # create children 
        newChildren.extend(createChildren(genomeX, genomeY, parentDominance, crossoversPerParent, env, mutationProbability, crossoverProbability, conflictResolvement))       
    
    return newChildren

def createChildren(genomeX, genomeY, parentDominance, crossoverPerParent, env, mutationProb, crossoverProb, conflictResolvement):
    
    # perform crossover, for both X and Y being dominant
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

    # if conflict resolvement is enabled
    if conflictResolvement:

        # perform mututions to resolve conflicts with constraints
        viableChildren = []
        for children in unviableChildren:
            birth = makeViable(children['genome'], children['genesToCheck'], env)
            if birth is not None:
                viableChildren.append(birth)

    # if conflict resolvement is not enabled
    elif not conflictResolvement:

        # convert not matching constraints
        viableChildren = []
        for children in unviableChildren:
            birth = children['genome']
            if birth is not None:
                viableChildren.append(birth)

    return viableChildren


def makeViable(child, genesToCheck, env):

    # conflict resolvement after fertilization
    newChild = resolveConflict(child, genesToCheck, env)

    # if conflict resolvement does not lead to a viable child, try again up to 'count' times
    count = 0
    while newChild is None and count<500:
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

    # assign free houses to random battery with free capacity
    for i in range(0, len(freeHouses)):
        free = True
        freeBatteries = list(range(len(temp_child.modelBatteries)))
        while (free): 
            try:        
                batteryIndex = random.choice(freeBatteries)
                for house in env.houses: 
                    if house.idHouse == freeHouses[i]:
                        houseToPlace = house

                
                # if capacity is enough to assign house
                if (temp_child.modelBatteries[batteryIndex].checkCapacity(env.batteries, houseToPlace)):
                    # assign house
                    temp_child.modelBatteries[batteryIndex].houses.append(houseToPlace)
                    free = False
                else:
                    freeBatteries.remove(batteryIndex)
            except IndexError:

                # if solution doesn't fit, try again in different order
                return 

    return temp_child

# fitness proportionate selection
def selection(newGeneration, popSize):
    
    selection = []

    # choose fitness function: LowHighScale, TotalCostScale, CostRank
    fitnessList = fitnessLowHighScale(newGeneration)

    # get random value and locate corresponding model
    for i in range(0, popSize):         
        value = random.random() 
        found = False

        for j in range(0, len(fitnessList)):
            if found == False: 
                value -= fitnessList[j][0]

                # append chosen model to new population and recalculate the probability values
                if value < 0:
                    selection.append(newGeneration[fitnessList[j][1] - 1])
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

# converts object of type genome to model class
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

        # copy second half to child and add the houseIds that are not included yet 
        fromOtherParentTuples = []

        for housenr in fromOtherParent:            
            for geneY in genomeY:
                if (geneY[0] == housenr):
                    genomeChild.append(geneY)     
                    fromOtherParentTuples.append(geneY)              

        return genomeChild, fromOtherParentTuples
    
    else:
        return genomeX, []

# writes logs to a file that is specific for this search 
def writeProgress(reportFileName, message):
    filePathName = "..\\results\personalresults\\logs\\" + reportFileName

    message = "-----------------\n" + message

    with open(filePathName,'a', newline='') as f:
        writer = csv.writer(f, escapechar = ' ', quoting=csv.QUOTE_NONE)
        print(message)
        writer.writerow([message])

# takes a random house and assigns it to a random battery
def mutation(model, env):

    # get the batteries from the model
    batteries = model.modelBatteries

    # get a random battery
    randomBatteries =(random.randint(0, len(batteries)-1), random.randint(0, len(batteries)-1))
    batterySendingHouse = batteries[randomBatteries[0]]

    # set the upperbounds for the houses randomizer
    setUpperboundBattery1 = len(batterySendingHouse.houses)

    # get a random house
    randomHouseId = random.randint(0, (setUpperboundBattery1 - 1))

    # get the houses on the random places
    house1 = batterySendingHouse.houses[randomHouseId]

    # get battery receiving the house
    batteryReceivingHouse = batteries[randomBatteries[1]]

    # add the house to the other battery
    batteries[randomBatteries[1]].houses.append(house1)
    houses = batterySendingHouse.houses
    houses.pop(randomHouseId)
    batteries[randomBatteries[0]].houses = houses

    # return the model
    returnModel = Model(batteries)
    returnModel.calculateCosts(env.distanceTable)
    return returnModel




        

