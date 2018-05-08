from classes.model import Model
from algorithms.runrandom import runRandom
import random

def hillClimber(env, iterations):

    # create a list with all the lowest costs per iteration for plotting purposes
    costs = []

    # run a random as a starting state
    boundModel = runRandom(env)

    # calculate the costs of the random
    boundModel.CalculateCosts

    # run the algorithm for the amount of iterations given
    for i in range(0, iterations):
        climberModel = boundModel
        modelClimbed = climbHill(climberModel)

        # calculate the costs of the returned model
        modelClimbed.CalculateCosts(env.distanceTable)

        # compare the costs to the bound state
        if (modelClimbed.cost < boundModel.cost):

            # if costs is lower, set the new bound state
            boundModel = modelClimbed

        # append lowest costs to the list for comparison    
        costs.append(boundModel.cost)

    return boundModel

def climbHill(model):

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