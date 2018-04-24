import csv
import os
from functions.distancetable import makedistancetable
from functions.runrandom import runrandom
from functions.helperfunctions import importhouses
from functions.helperfunctions import importbatteries
from classes.battery import Battery
from classes.house import House


houses = importhouses(r"..\data\wijk1_huizen.csv")
batteries = importbatteries(r"..\data\wijk1_batterijen.csv")

dt = makedistancetable(batteries, houses)

# would be nice to do this like a hundred times
print("costs:")
print(runrandom(batteries, houses, dt))

   


    