from classes.environment import Environment
from classes.model import Model
import numpy as np
import random

def kMeans(env, iterations):

    kMeansEnv = env

    for i in range(0, iterations):
        batteries = assignHousesToBatteries(kMeansEnv)
        # kMeansEnv = moveBatteriesToCenter(batteries, kMeansEnv)

    return kMeansEnv

def assignHousesToBatteries(kMeansEnv):

    toBeAssigned = list(range(1, 151))

    modelBatteries = kMeansEnv.createModelBatteries()
    dt = createBatteryDistanceTable(kMeansEnv)

    for battery in kMeansEnv.batteries:
        batteryDistance = []
        
        for house in kMeansEnv.houses:
            batteryDistance.append([dt[battery.idBattery][house.idHouse], house.idHouse])
        batteryDistance = sorted(batteryDistance)
        modelBatteries[battery.idBattery - 1].batteryDistanceList = batteryDistance
  
    i = 0
    X = 0
    while(toBeAssigned != list([0]*150)):
        # print(i)
        if i == 150:
            i = 0
            X += 1
            print(toBeAssigned)
            # print(i)
            if X == 2:
                toBeAssigned = list([0]*150)
        for battery in modelBatteries:
            # print(battery.batteryDistanceList)
            nearestNeighbour = battery.batteryDistanceList[i]
            print(battery.batteryDistanceList[54])
            nearestNeighbourID = nearestNeighbour[1]

            # check in de lijst
            if nearestNeighbourID in toBeAssigned:
                print("Batterij en huis: ")
                print(battery.idBattery)
                print(nearestNeighbourID)
                kMeansHouse = kMeansEnv.houses[nearestNeighbourID - 1]
                
                print("is check true?: ")
                print(battery.checkCapacity(kMeansEnv.batteries, kMeansHouse))
                if battery.checkCapacity(kMeansEnv.batteries, kMeansHouse):
                    print("nearest neighbourID: ")
                    print(nearestNeighbourID - 1)
                    toBeAssigned[nearestNeighbourID - 1] = 0
                    battery.houses.append(kMeansHouse)
                    print("Fit in")
                else:
                    print("I wont fit")
        i+=1

    for battery in modelBatteries:
        houseIdList = []
        for house in battery.houses:
            houseIdList.append(house.idHouse)
        print("Battery data: ") 
        print(battery.idBattery)   
        print(battery.curCapacity)
        print(houseIdList)
    house = kMeansEnv.houses[53]
    print(house.cap)

    # print(toBeAssigned)
    # return modelBatteries

def moveBatteriesToCenter(modelBatteries, kMeansEnv):
    envBatteries = kMeansEnv.batteries

    for battery in modelBatteries:
        batteryNewX = 0
        batteryNewY = 0

        for house in battery.houses:

            # add house x to batteryNewX
            batteryNewX += house.x

            # add house y to batteryNewY
            batteryNewY += house.y
        
        batteryNewX = batteryNewX/len(battery.houses)
        batteryNewY = batteryNewY/len(battery.houses)

        newEnvBattery = envBatteries[battery.idBattery - 1]

        newEnvBattery.x = batteryNewX
        newEnvBattery.y = batteryNewY
    
        envBatteries[battery.idBattery - 1] = newEnvBattery
    
    kMeansEnv.batteries = envBatteries
    return kMeansEnv



# rewrite k-means
# nieuw distance table vanuit de batterij
# sorteer distancetable op afstand
# laat batterijen om de beurt een huis kiezen
# check capaciteit
# zodra een huis gekozen is streep het huis weg uit de lijst
# doorgaan tot alle huizen zijn toegewezen en het klopt
# Dan de 2e functie

def createBatteryDistanceTable(kmeansEnv):
        
    # create column for each house
    batteryDistanceTable = np.array(range(len(kmeansEnv.houses) + 1))

    # append batteryId to left column
    for battery in kmeansEnv.batteries:
        row = [battery.idBattery]

        # append distance to each house for every battery
        for house in kmeansEnv.houses:
            row.append(abs(battery.x-house.x)+abs(battery.y-house.y))

        # convert list into numpy array and add each battery
        np.asarray(row)
        batteryDistanceTable = np.vstack([batteryDistanceTable, row])

    return(batteryDistanceTable)