import os
import csv
from classes.battery import battery
from classes.house import house

def importhouses(housescsv):
    # load data and connect
    with open(housescsv, 'r') as f:
        reader = csv.reader(f)
        itemshouse = list(reader)

    houses = []
    i = 1
    for itemh in itemshouse:
        home = house()
        home.idhouse = i
        home.x = itemh[0] 
        home.y = itemh[1]
        home.cap = itemh[2]
        houses.append(home)
        i = i + 1
    
    return houses
    
def importbatteries(batteriescsv):
    with open(batteriescsv, 'r') as f:
        reader = csv.reader(f)
        itemsbattery = list(reader)
    
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
    
    return batteries
