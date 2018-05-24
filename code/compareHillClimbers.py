import csv
import os
from algorithms.runrandom import runRandom
from algorithms.evolutionnocon import evolutionNoCon
from algorithms.hillclimber import hillClimber
from algorithms.depthfirst import depthFirstBnB 
from functions.visualisation import visVillage
from functions.plothist import plotHist
from functions.plothistmultiple import plotHistMultiple
from functions.plotiterativesearch import plotIterativeSearch
from classes.model import Model
from classes.environment import Environment

env = Environment(r"..\data\wijk2_huizen.csv", r"..\data\wijk2_batterijen.csv", 2)

n = 5
listOfHillClimber1 = []
listOfHillClimber3 = []
listOfHillClimber5 = []
listOfHillClimberNoCon = []

    # add legend

it = 1000


for i in range(0, n):
    print(i)
    model = runRandom(env)
    model1 = hillClimber(env, model, it, 1) 
    print(model1.cost)
    listOfHillClimber1.append(model1.cost)
print(listOfHillClimber1)
    # model3 = hillClimber(env, model, it, 3)
    # model3.write()
    # listOfHillClimber3.append(model3.cost)
    # model5 = hillClimber(env, model, it, 5)
    # model5.write()
    # listOfHillClimber5.append(model5.cost)
    # modelNoCon = hillClimberNoCon(env, it)
    # listOfHillClimberNoCon.append(modelNoCon.cost)
# plotHistMultiple([listOfHillClimberNoCon], ["HC 3 moves (i = 10000)"], 8, n, 1)
plotHistMultiple([listOfHillClimber1], ["HC 1 move (i = 1000)"], 1, n, 2)