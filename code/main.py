import csv
import os
from functions.distancetable import makeDistanceTable
from functions.runrandom import runRandom
from functions.visualisation import visVillage
from functions.helperfunctions import importHouses
from functions.helperfunctions import importBatteries
from classes.battery import Battery
from classes.house import House

houses = importHouses(r"..\data\wijk3_huizen.csv")
batteries = importBatteries(r"..\data\wijk3_batterijen.csv")

dt = makeDistanceTable(batteries, houses)


for i in range (0,2):
    result = runRandom(batteries, houses, dt)
    print(result['cost'])

visVillage(result['batteries'], result['houses'])
