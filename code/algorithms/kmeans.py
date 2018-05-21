from classes.environment import Environment
from classes.model import Model

def kMeans(env, iterations):

    kMeansEnv = env

    for i in range(0, iterations):
        batteries = assignHousesToBatteries(kMeansEnv)
        kMeansEnv = moveBatteriesToCenter(batteries, kMeansEnv)
    return kMeansEnv

def assignHousesToBatteries(kMeansEnv):

    toBeAssigned = list(range(1, 151))

    modelBatteries = kMeansEnv.createModelBatteries()

    for house in kMeansEnv.houses:
        batteryDistance = []
        for battery in kMeansEnv.batteries:
            batteryDistance.append([kMeansEnv.distanceTable[house.idHouse][battery.idBattery], battery.idBattery])
            # print([env.distanceTable[house.idHouse][battery.idBattery], battery.idBattery])
        
        if house.idHouse in toBeAssigned:
            # print((toBeAssigned[house.idHouse-1]))
            toBeAssigned[house.idHouse-1] = 0
            nearestNeighbour = min(batteryDistance)
            battery = modelBatteries[nearestNeighbour[1]-1]
            if battery.checkCapacity(battery.idBattery, kMeansEnv.batteries, battery.houses, house):
                print("Yay i fit!")
                battery.houses.append(house)
            else:
                print("I don't fit")
                
                check = True
                while (check):
                    i = 1
                    batteryDistance = sorted(batteryDistance)
                    print(batteryDistance)
                    nearestNeighbour = batteryDistance[i]
                    battery = modelBatteries[nearestNeighbour[1]-1]
                    if battery.checkCapacity(battery.idBattery, kMeansEnv.batteries, battery.houses, house):
                        print("Yay i fit in a different battery!")
                        battery.houses.append(house)
                        check = False
                    else:
                        print("second try wont fit neither")
                        i = i + 1
                        if (i == 3):
                            print("i wont fit anywhere")
                            check = False

            modelBatteries[nearestNeighbour[1]-1] = battery

    print(toBeAssigned)
    return modelBatteries

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