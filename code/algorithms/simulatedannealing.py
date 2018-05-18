from classes.model import Model
from algorithms.runrandom import runRandom
import random
import math

def simAnneal(env, iterations, maxTemp):

    # create a list with all the lowest costs per iteration for plotting purposes
    costs = []

    # run a random as a starting state
    boundModel = runRandom(env)

    # run the algorithm for the amount of iterations given
    for i in range(0, iterations):
        climberModel = boundModel
        modelClimbed = climbHill(climberModel)

        # calculate the costs of the returned model
        modelClimbed.calculateCosts(env.distanceTable)

        # get the current temp
        temp = curTempExp(i, maxTemp, iterations)

        # get a random number between 0 and 1
        randomNum = random.random()

        # compare the result and anneal
        if (acceptation(boundModel, modelClimbed, temp) > randomNum):
            boundModel = modelClimbed

        # append lowest costs to the list for comparison    
        costs.append(boundModel.cost)

    # return the list of costs for plotting
    boundModel.listOfCosts = costs

    return boundModel

def climbHill(model):

    # get the batteries from themodel
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

def curTempLinear(iteration, maxTemp, iterationTotal):
    return (-(maxTemp/iterationTotal) * iteration) + maxTemp

def curTempLog(iteration, maxTemp, iterationTotal):
    print()
    # return maxTemp/(math.log(iteration + 1))
    # return (maxTemp*(iterationTotal/maxTemp)**(iteration/iterationTotal))

def curTempExp(iteration, maxTemp, iterationTotal):
    return(maxTemp**(iteration/iterationTotal))

def acceptation(boundModel, modelClimbed, temp):
    if (modelClimbed.cost < boundModel.cost):

        # if the new costs are lower, return 1
        return 1.0
    
    # else return the calculation for the acceptation
    print(math.exp((boundModel.cost - modelClimbed.cost) / temp))
    return math.exp((boundModel.cost - modelClimbed.cost) / temp)