import csv
import os
from functions.distancetable import makedistancetable
from functions.helperfunctions import importhouses
from functions.helperfunctions import importbatteries
from classes.battery import battery
from classes.house import house

houses = importhouses(r"..\data\wijk2_huizen.csv")
batteries = importbatteries(r"..\data\wijk2_batterijen.csv")

makedistancetable(batteries, houses)

