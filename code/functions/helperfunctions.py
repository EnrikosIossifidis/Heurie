import os
import csv
from classes.Battery import Battery
from classes.House import House

def importHouses(housesCsv):
    # load data and connect
    with open(housesCsv, 'r') as f:
        reader = csv.reader(f)
        itemsHouse = list(reader)

    houses = []
    i = 1
    for itemH in itemsHouse:
        house = House()
        house.idHouse = i
        house.x = itemH[0] 
        house.y = itemH[1]
        house.cap = itemH[2]
        houses.append(house)
        i = i + 1
    
    return houses
    
def importBatteries(batteriesCsv):
    with open(batteriesCsv, 'r') as f:
        reader = csv.reader(f)
        itemsBattery = list(reader)
    
    batteries = []
    j = 1
    for itemB in itemsBattery:
        battery = Battery()
        battery.idBattery = j
        battery.x = itemB[0] 
        battery.y = itemB[1]
        battery.maxCapacity = itemB[2]
        batteries.append(battery)
        j = j + 1
    
    return batteries
