import csv
import os
from functions.distanceTable import makedistancetable
from functions.helperfunctions import importhouses
from functions.helperfunctions import importbatteries
from classes.battery import battery
from classes.house import house

<<<<<<< HEAD
houses = importhouses(r"..\data\wijk2_huizen.csv")
batteries = importbatteries(r"..\data\wijk2_batterijen.csv")

makedistancetable(batteries, houses)

=======
houses = importHouses(r"C:\Users\enrik\Documents\GitHub\Heurie\data\wijk3_huizen.csv")
batteries = importBatteries(r"C:\Users\enrik\Documents\GitHub\Heurie\data\wijk3_batterijen.csv")
dt = makeDistanceTable(batteries, houses)
print(dt)
>>>>>>> 0e6b5cee310735465518c97c2817b4b641b64005
