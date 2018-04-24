import csv
import os
from Functions.distancetable import makedistancetable
from Functions.helperfunctions import importhouses
from Functions.helperfunctions import importbatteries
from classes.battery import Battery
from classes.house import House

houses = importhouses(r"..\data\wijk2_huizen.csv")
batteries = importbatteries(r"..\data\wijk2_batterijen.csv")

dt = makedistancetable(batteries, houses)
print(dt)

