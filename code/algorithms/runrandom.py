import random
import sys
from classes.model import Model

def runRandom(env):

    # keep randomizing until a model that meets constraints is found
    random = randomize(env)
    while random == False:
        random = randomize(env)
    return random

def randomize(env):

    modelBatteries = []

    # create the array of batteries with the id starting at 1
    for i in range (0, len(env.batteries)):
        maxCap = env.batteries[i].maxCapacity
        battery = Model.Battery(i+1)
        modelBatteries.append(battery)

    # assign every house to a random battery of which the capacity is still sufficient
    listOfHouses = env.houses
    random.shuffle(listOfHouses)

    # assign random battery to every house
    for house in listOfHouses:
        batIndexes = []
        for i in range(0,len(env.batteries)):
            batIndexes.append(i)
        assignToRandomBattery(batIndexes, env.batteries, house, modelBatteries)
    
    # check if every house is connected
    totalHouses = 0
    for battery in modelBatteries:
        totalHouses += len(battery.houses)
    
    if totalHouses == len(env.houses):

        # assign all the values into a model
        model = Model(modelBatteries)

        # calculate the costs of this option
        model.calculateCosts(env.distanceTable)

        return model
    
    else:
        return False

def assignToRandomBattery(batIndexes, batteries, house, modelBatteries):
 
    secureRandom = random.Random()
 
    try: 
        batIndex = secureRandom.choice(batIndexes)
    except IndexError:
        return False

    randomBat = modelBatteries[batIndex]

    # if the capacity has enough room, assign house to battery 
    if randomBat.checkCapacity(batteries, house) == True:
        randomBat.houses.append(house)
        modelBatteries[batIndex].curCapacity += house.cap

    # else retrieve a random index again
    else:
        batIndexes.remove(batIndex) 
        assignToRandomBattery(batIndexes, batteries, house, modelBatteries)

