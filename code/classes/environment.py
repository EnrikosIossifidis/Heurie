import csv
import numpy as np
from classes.model import Model

class Environment:
    
    class Battery:
        def __init__(self, id, xCoor, yCoor, batCap):
            self.idBattery = id
            self.x = xCoor
            self.y = yCoor
            self.maxCapacity = batCap

    class House:
        def __init__(self, id, xCoor, yCoor, houseCap):
            self.idHouse = id
            self.x = xCoor
            self.y = yCoor
            self.cap = houseCap

    def __init__(self, houses, batteries, id):
        self.batteries = self.importBatteries(batteries)
        self.houses = self.importHouses(houses)
        self.distanceTable = self.createDistanceTable()
        self.village = "Village " + str(id)

    def importHouses(self, housesCsv):

        # read the houses from the csv
        with open(housesCsv, 'r') as f:
            reader = csv.reader(f)
            itemsHouse = list(reader)

        houseObjectList = []

        # start the house id with 1
        i = 1

        # load the houses into the house list
        for itemH in itemsHouse:
            house = Environment.House(i, int(itemH[0]), int(itemH[1]), float(itemH[2]))
            houseObjectList.append(house)
            i += 1

        return houseObjectList

    def importBatteries(self, batteriesCsv):

        # read the batteries from the csv
        with open(batteriesCsv, 'r') as f:
            reader = csv.reader(f)
            itemsBattery = list(reader)
        
        batObjectList = []
        
        # make sure the battery id does start with a 1
        i = 1

        # load the batteries into the battery list
        for itemB in itemsBattery:
            battery = Environment.Battery(i, int(itemB[0]), int(itemB[1]), float(itemB[2]))
            batObjectList.append(battery)
            i += 1
        
        return batObjectList

    def createDistanceTable(self):
            
        # create column for each battery
        distancetable = np.array(range(len(self.batteries) + 1))

        # append idHouse to left column
        for house in self.houses:
            row = [house.idHouse]

            # append distance to each battery for every house
            for bat in self.batteries:
                row.append(abs(house.x-bat.x)+abs(house.y-bat.y))

            # convert list into numpy array and add each house
            np.asarray(row)
            distancetable = np.vstack([distancetable, row])

        return(distancetable)

    def createModelBatteries(self, batteries):

        modelBatteries = []
        
        for i in range (0, len(batteries)):
            modelBatteries.append(Model.Battery(i+1))

        return modelBatteries

