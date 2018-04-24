import os
import csv
from classes.battery import Battery
from classes.house import House

def importhouses(housescsv):
    # load data and connect
    with open(housescsv, 'r') as f:
        reader = csv.reader(f)
        itemsHouse = list(reader)

    houseObjectList = []
    i = 1
    for itemH in itemsHouse:
        house = House(i, int(itemH[0]), int(itemH[1]), float(itemH[2]))
        houseObjectList.append(house)
        i += 1

    return houseObjectList
    
def importbatteries(batteriescsv):
    with open(batteriescsv, 'r') as f:
        reader = csv.reader(f)
        itemsBattery = list(reader)
    
    batObjectList = []
    i = 1
    for itemB in itemsBattery:
        battery = Battery(i, int(itemB[0]), int(itemB[1]), float(itemB[2]))
        batObjectList.append(battery)
        i += 1
    
    return batObjectList
