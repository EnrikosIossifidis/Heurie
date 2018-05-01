import csv
import os
from functions.distancetable import makeDistanceTable
from functions.runrandom import runRandom
from functions.visualisation import visVillage
from functions.helperfunctions import importHouses
from functions.helperfunctions import importBatteries
from classes.model import Model
from classes.environment import Environment

houses = importHouses(r"..\data\wijk3_huizen.csv")
batteries = importBatteries(r"..\data\wijk3_batterijen.csv")
env = Environment(houses, batteries)

dt = makeDistanceTable(env)

for i in range (0,2):
    model = runRandom(env, dt)
    print(model.cost)
    visVillage(env, model)

