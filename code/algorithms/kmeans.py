from classes.environment import Environment
from classes.model import Model

def KMeans(env):

    toBeAssigned = list(range(1, 151))
    kMeansModel = Model()

    for house in env.houses:
        batteryDistance = []
        for battery in env.batteries:
            batteryDistance.append([env.distanceTable[house.idHouse][battery.idBattery], battery.idBattery])
        if house.idHouse in toBeAssigned:
            print(min(batteryDistance))
        

