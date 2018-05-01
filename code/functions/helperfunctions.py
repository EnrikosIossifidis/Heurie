import os
import csv
from classes.environment import Environment

def importHouses(housesCsv):

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
    
def importBatteries(batteriesCsv):

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
