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
        house = house()
        house.idhouse = i
        house.x = itemh[0] 
        house.y = itemh[1]
        house.cap = itemh[2]
        houses.append(house)
        i = i + 1
    
    return houses
    
def importbatteries(batteriescsv):
    with open(batteriescsv, 'r') as f:
        reader = csv.reader(f)
        itemsbattery = list(reader)
    
    batteries = []
    j = 1
    for itemb in itemsbattery:
        battery = battery()
        battery.idbattery = j
        battery.x = itemb[0] 
        battery.y = itemb[1]
        battery.maxcapacity = itemb[2]
        batteries.append(battery)
        j = j + 1
    
    return batteries
