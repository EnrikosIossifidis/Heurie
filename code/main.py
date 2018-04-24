import csv
import os
from Functions.distanceTable import makeDistanceTable
from Functions.helperfunctions import importHouses
from Functions.helperfunctions import importBatteries
from classes.Battery import Battery
from classes.House import House

houses = importHouses(r"C:\Users\enrik\Documents\GitHub\Heurie\data\wijk1_huizen.csv")
batteries = importBatteries(r"C:\Users\enrik\Documents\GitHub\Heurie\data\wijk1_batterijen.csv")

makeDistanceTable(batteries, houses)

