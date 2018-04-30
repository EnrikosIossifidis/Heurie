import csv
import os
from functions.distancetable import makedistancetable
from functions.runrandom import runrandom
from functions.visualisation import visvillage
from functions.helperfunctions import importhouses
from functions.helperfunctions import importbatteries
from classes.battery import Battery
from classes.house import House


houses = importhouses(r"..\data\wijk3_huizen.csv")
batteries = importbatteries(r"..\data\wijk3_batterijen.csv")

dt = makedistancetable(batteries, houses)

for i in range (0,2):
    result = runrandom(batteries, houses, dt)
    print(result['cost'])

visvillage(result['batteries'], result['houses'])