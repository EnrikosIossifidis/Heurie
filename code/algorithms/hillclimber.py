from classes.model import Model
from algorithms.runrandom import runRandom
import random

def hillClimber(env, iterations, trials):

    # create a list with all the lowest costs per iteration for plotting purposes
    costs = []

    # run a random as a starting state
    boundModel = runRandom(env)

    # run the algorithm for the amount of iterations given
    for i in range(0, iterations):
        climberModel = boundModel

        check = False
        while check == False:
            for j in range(0, trials):
                modelClimbed = climbHill(climberModel)  
            check = modelClimbed.checkValidity(env)

        # calculate the costs of the returned model
        modelClimbed.calculateCosts(env.distanceTable)

        # compare the costs to the bound state
        if (modelClimbed.cost < boundModel.cost):

            # if costs is lower, set the new bound state
            boundModel = modelClimbed

            # append lowest costs to the list for comparison    
        costs.append(boundModel.cost)

    # return the list of costs for plotting
    boundModel.listOfCosts = costs

    return boundModel

def climbHill(model):

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
