'''Randomly assigns houses to batteries, considering capacity restrictions - returns total cable distance (and which houses are assigned to which battery)'''
import random
import sys

def runRandom(batteries, houses, dt):

    # assign every house to a random battery of which the capacity is still sufficient
    for house in houses:
        batIndexes = list()
        for i in range(0,len(batteries)):
            batIndexes.append(i)
        assignToRandomBattery(batIndexes, batteries, house)

    # calculate the costs of this option
    cost = calculateCost(batteries, dt)

    # just some prints that are handy for now

    # for battery in batteries:
    #     for housesAssign in battery.house:
    #         print("Battery, house: ")
    #         print(battery.idBattery, housesAssign.idHouse)
    
    # for battery in batteries:
    #     print("battery.maxcapacity, battery.curcapacity, amount of houses per battery") 
    #     print(battery.maxcapacity, battery.curcapacity, len(battery.house)) 
    return {'cost': cost, 'batteries': batteries, 'houses': houses, 'dt': dt}


def assignToRandomBattery(batIndexes, batteries, house):
    secureRandom = random.Random()
    try:
        batIndex = secureRandom.choice(batIndexes)
        print(batIndex)
    except IndexError:
        return 0
        
    # if the capacity has enough room, assign house to battery 
    if (batteries[batIndex].curCapacity + house.cap)<=batteries[batIndex].maxCapacity:
        batteries[batIndex].house.append(house)
        house.battery = batteries[batIndex].idBattery
        batteries[batIndex].curCapacity += house.cap
    # else retrieve a random index again (this way it can happen that it chooses 1 >> is full >> it 2 >> is full >> it chooses 1 again... this creates a loop)
    else:
        batIndexes.remove(batIndex) 
        assignToRandomBattery(batIndexes, batteries, house)

def calculateCost(batteries, dt):
    cost = 0
    for battery in batteries:
        for house in battery.house:
            cost += dt[house.idHouse][battery.idBattery]
    return cost

