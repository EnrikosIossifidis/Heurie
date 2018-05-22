from classes.model import Model
from algorithms.runrandom import runRandom
import random

def hillClimber(env, model, iterations, moves):

    # create a list with all the lowest costs per iteration for plotting purposes
    costs = []

    # run a random as a starting state
    boundModel = model

    climberModel = boundModel

    # run the algorithm for the amount of iterations given
    for i in range(0, iterations):
        check = False
        while check == False:
            climbedModel = climberModel
            for j in range(0, moves):
                 climbedModel = climbHill(climbedModel)  
            check = climbedModel.checkValidity(env)

        # calculate the costs of the returned model
        climbedModel.calculateCosts(env.distanceTable)
        print(boundModel.cost)
        print(climbedModel.cost)
        # compare the costs to the bound state
        if (climbedModel.cost < boundModel.cost):

            # if costs is lower, set the new bound state
            boundModel = climbedModel

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
    batterySendingHouse = batteries[randomBatteries[0]]

    if allowSending(batterySendingHouse):
        # set the upperbounds for the houses randomizer
        setUpperboundBattery1 = len(batterySendingHouse.houses)

        # get a random house
        randomHouseId = random.randint(0, (setUpperboundBattery1 - 1))

        # get the houses on the random places
        house1 = batterySendingHouse.houses[randomHouseId]

        # get battery receiving the house
        batteryReceivingHouse = batteries[randomBatteries[1]]

        if allowPlacement(batteryReceivingHouse):
            # add the house to the other battery
            batteries[randomBatteries[1]].houses.append(house1)
            houses = batterySendingHouse.houses
            houses.pop(randomHouseId)
            batteries[randomBatteries[0]].houses = houses

    # return the model
    returnModel = Model(batteries)
    return returnModel

def allowPlacement(battery):
    length = len(battery.houses)
    if length < 35:
        return True
    else:
        # print("Not accepted in allow Placement")
        return False

def allowSending(battery):
    length = len(battery.houses)
    if length > 25:
        return True
    else:
        # print("Not accepted in allow Sending")
        return False    