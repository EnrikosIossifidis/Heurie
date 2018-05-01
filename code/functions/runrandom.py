'''Randomly assigns houses to batteries, considering capacity restrictions - returns total cable distance (and which houses are assigned to which battery)'''
import random
import sys
from classes.model import Model

def runRandom(env, dt):
    
    modelBatteries = []
    for i in range (0,len(env.batteries)):
        battery = Model.Battery(i+1)
        modelBatteries.append(battery)

    # assign every house to a random battery of which the capacity is still sufficient
    for house in env.houses:
        batIndexes = list()
        for i in range(0,len(env.batteries)):
            batIndexes.append(i)
        assignToRandomBattery(batIndexes, env.batteries, house, modelBatteries)

    # calculate the costs of this option
    cost = calculateCost(modelBatteries, dt)

    model = Model(cost, modelBatteries)
    # just some prints that are handy for now

    # for battery in batteries:
    #     for housesAssign in battery.house:
    #         print("Battery, house: ")
    #         print(battery.idBattery, housesAssign.idHouse)
    
    # for battery in batteries:
    #     print("battery.maxcapacity, battery.curcapacity, amount of houses per battery") 
    #     print(battery.maxcapacity, battery.curcapacity, len(battery.house)) 
    return model


def assignToRandomBattery(batIndexes, batteries, house, modelBatteries):
    secureRandom = random.Random()
    try:
        batIndex = secureRandom.choice(batIndexes)
        # print(batIndex)
    except IndexError:
        return 0
        
    # if the capacity has enough room, assign house to battery 
    if (modelBatteries[batIndex].curCapacity + house.cap)<=batteries[batIndex].maxCapacity:
        modelBatteries[batIndex].houses.append(house)
        modelBatteries[batIndex].curCapacity += house.cap
    # else retrieve a random index again (this way it can happen that it chooses 1 >> is full >> it 2 >> is full >> it chooses 1 again... this creates a loop)
    else:
        batIndexes.remove(batIndex) 
        assignToRandomBattery(batIndexes, batteries, house, modelBatteries)

def calculateCost(batteries, dt):
    cost = 0
    for battery in batteries:
        for house in battery.houses:
            cost += dt[house.idHouse][battery.idBattery]
    return cost

