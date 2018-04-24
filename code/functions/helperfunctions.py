import os
import csv
from classes.battery import battery
from classes.house import house

def importhouses(housescsv):
    # load data and connect
    with open(housescsv, 'r') as f:
        reader = csv.reader(f)
        itemshouse = list(reader)

    houseObjectList = []
    i = 1
<<<<<<< HEAD
    for itemH in itemsHouse:
        house = House(i, int(itemH[0]), int(itemH[1]), float(itemH[2]))
        houseObjectList.append(house)
        i += 1
=======
    for itemh in itemshouse:
        home = house()
        home.idhouse = i
        home.x = itemh[0] 
        home.y = itemh[1]
        home.cap = itemh[2]
        houses.append(home)
        i = i + 1
>>>>>>> 1ade9e18c6211433f18293b2d3200bdd069d4644
    
    return houseObjectList
    
def importbatteries(batteriescsv):
    with open(batteriescsv, 'r') as f:
        reader = csv.reader(f)
        itemsbattery = list(reader)
    
<<<<<<< HEAD
    batObjectList = []
    i = 1
    for itemB in itemsBattery:
        battery = Battery(i, int(itemB[0]), int(itemB[1]), float(itemB[2]))
        batObjectList.append(battery)
        i += 1
=======
    batteries = []
    j = 1
    for itemb in itemsbattery:
        bat = battery()
        bat.idbattery = j
        bat.x = itemb[0] 
        bat.y = itemb[1]
        bat.maxcapacity = itemb[2]
        batteries.append(bat)
        j = j + 1
>>>>>>> 1ade9e18c6211433f18293b2d3200bdd069d4644
    
    return batObjectList
