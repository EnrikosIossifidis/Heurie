import csv
import os
from algorithms.runrandom import runRandom
from algorithms.depthfirst import depthFirstBnB 
from functions.visualisation import visVillage
from classes.model import Model
from classes.environment import Environment

env = Environment(r"..\data\wijk3_huizen.csv", r"..\data\wijk3_batterijen.csv", 3)

for i in range (0,2):
    model = runRandom(env)
    model.setName("random", i)
    model.printResult()

    visVillage(env, model)

print(depthFirstBnB(model, env, dt))

