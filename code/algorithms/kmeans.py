from classes.environment import Environment
from classes.model import Model
import numpy as np
import random

def kMeans(env, iterations):

    # copy env so it doesn't overwrite the original env
    kMeansEnv = env

    # for every iteration loop through the k-means
    for i in range(0, iterations):
        batteries = assignHousesToBatteries(kMeansEnv)
        kMeansEnv = moveBatteriesToCenter(batteries, kMeansEnv)

    # return the altered environment
    return kMeansEnv

def assignHousesToBatteries(kMeansEnv):

    # create a list with a number for every house
    toBeAssigned = list(range(1, 151))

    # get the batteries for a model and the distance table seen from the batteries
    modelBatteries = kMeansEnv.createModelBatteries()
    dt = createBatteryDistanceTable(kMeansEnv)

    # loop through every battery
    for battery in kMeansEnv.batteries:

        # create a distance list
        batteryDistance = []

        # for every house, add a tuple of the distance to the battery and the house ID to the distancelist
        for house in kMeansEnv.houses:
            batteryDistance.append([dt[battery.idBattery][house.idHouse], house.idHouse])

        # sort the distance list on distance from house to battery and add it to the modelBattery
        batteryDistance = sorted(batteryDistance)
        modelBatteries[battery.idBattery - 1].batteryDistanceList = batteryDistance
  
    # set the loop controllers
    i = 0
    x = 0

    # do this while the list is not empty
    while(toBeAssigned != list([0]*150)):

        # to make sure that after one loop, we use the addWithoutChecking and start with 0 again
        if i == 150:
            i = 0
            x = 1
            # print(toBeAssigned)
            # print("---------------")

        # first add houses with check and when x is not 0, add houses without check
        if x == 0:    
            checkAndAddHouses(modelBatteries, kMeansEnv, toBeAssigned, i)
        else:
            addWithoutChecking(modelBatteries, kMeansEnv, toBeAssigned, i)

        # add 1 to the iteration so it loops through every entry of the distancetable    
        i+=1
    
    # a print to check battery capacity and which house is attached to which battery
    # print(toBeAssigned)
    # for battery in modelBatteries:
    #     houseIdList = []
    #     for house in battery.houses:
    #         houseIdList.append(house.idHouse)
    #     print("Battery data: ") 
    #     print(battery.idBattery)   
    #     print(battery.curCapacity)
    #     print(houseIdList)
    #     print("---------------")

    return modelBatteries

def moveBatteriesToCenter(modelBatteries, kMeansEnv):

    # get the batteries from the environment
    envBatteries = kMeansEnv.batteries

    # loop through every battery and create an empty X and Y
    for battery in modelBatteries:
        batteryNewX = 0
        batteryNewY = 0

        # loop through every house
        for house in battery.houses:

            # add house x to batteryNewX
            batteryNewX += house.x

            # add house y to batteryNewY
            batteryNewY += house.y
        
        # calculate the average of the X and Y
        batteryNewX = batteryNewX/len(battery.houses)
        batteryNewY = batteryNewY/len(battery.houses)

        # create a new environment battery
        newEnvBattery = envBatteries[battery.idBattery - 1]

        # add the new X and Y coordinates
        newEnvBattery.x = batteryNewX
        newEnvBattery.y = batteryNewY
    
        # replace the old environment battery with the new environment battery
        envBatteries[battery.idBattery - 1] = newEnvBattery
    
    # replace the old environment batteries with the new environment batteries
    kMeansEnv.batteries = envBatteries
    return kMeansEnv

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

def checkAndAddHouses(modelBatteries, kMeansEnv, toBeAssigned, i):

    # loop through every battery
    for battery in modelBatteries:
            
            # get the tuple in the distance list on place i, and get the idHouse of that spot
            nearestNeighbour = battery.batteryDistanceList[i]
            nearestNeighbourID = nearestNeighbour[1]

            # check the list if the house is already assigned
            if nearestNeighbourID in toBeAssigned:

                # get the house object from the environment
                kMeansHouse = kMeansEnv.houses[nearestNeighbourID - 1]

                # check if the house is able to fit in the battery 
                if battery.checkCapacity(kMeansEnv.batteries, kMeansHouse):

                    # if it fits, update the list that the house is assigned and add the house to the battery
                    toBeAssigned[nearestNeighbourID - 1] = 0
                    battery.houses.append(kMeansHouse)

    return modelBatteries, toBeAssigned

def addWithoutChecking(modelBatteries, kMeansEnv, toBeAssigned, i):

    # loop through every battery
    for battery in modelBatteries:

        # get the tuple in the distance list on place i, and get the idHouse of that spot
        nearestNeighbour = battery.batteryDistanceList[i]
        nearestNeighbourID = nearestNeighbour[1]

        # check the list if the house is already assigned
        if nearestNeighbourID in toBeAssigned:

             # get the house object from the environment, update the list and assign it to a battery
            kMeansHouse = kMeansEnv.houses[nearestNeighbourID - 1]
            toBeAssigned[nearestNeighbourID - 1] = 0
            battery.houses.append(kMeansHouse)

    return modelBatteries, toBeAssigned