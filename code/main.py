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

env = Environment(r"..\data\wijk3_huizen.csv", r"..\data\wijk3_batterijen.csv", 3)

# test and visualise
listOfRandom = []
for i in range(0, 1000):
    model = runRandom(env)
    listOfRandom.append(model.cost)

listOfHillClimber = []
for i in range(0, 1000):
    model = hillClimber(env, 1000)
    listOfHillClimber.append(model.cost)


# listOfEvolution = []
# for i in range(0, 1000):
#     model = evolution(env, 10, 10)
#     listOfEvolution.append(model.cost)

# plot histograms
arrayMultiplePlot = []
arrayMultiplePlot.append(listOfRandom)
arrayMultiplePlot.append(listOfHillClimber)
plotHistMultiple(arrayMultiplePlot, ["random", "hillclimber"], 4, 1000)
plotHist(listOfRandom, 1, 1000, "random")
plotHist(listOfHillClimber, 2, 1000, "hillclimber")
# plotHist(listOfEvolution, 3, 10, "evolution")

hillModel = hillClimber(env, 1000)
plotIterativeSearch(hillModel.listOfCosts, 1, "hillclimber")

