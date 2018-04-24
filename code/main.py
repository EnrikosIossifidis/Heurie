import csv
import os
from functions.distancetable import makedistancetable
from functions.helperfunctions import importhouses
from functions.helperfunctions import importbatteries
from classes.battery import Battery
from classes.house import House

houses = importhouses(r"..\data\wijk2_huizen.csv")
batteries = importbatteries(r"..\data\wijk2_batterijen.csv")

dt = makedistancetable(batteries, houses)
print(dt)

