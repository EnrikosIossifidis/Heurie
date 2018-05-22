import csv
import os
from algorithms.runrandom import runRandom
from algorithms.evolutionnocon import evolutionNoCon
from algorithms.hillclimber import hillClimber
from algorithms.hillclimbernocon import hillClimberNoCon
from algorithms.hillclimberrelaxation import hillClimberRelax
from algorithms.depthfirst import depthFirstBnB 
from functions.visualisation import visVillage
from functions.plothist import plotHist
from functions.plothistmultiple import plotHistMultiple
from functions.plotiterativesearch import plotIterativeSearch
from classes.model import Model
from classes.environment import Environment

env = Environment(r"..\data\wijk1_huizen.csv", r"..\data\wijk1_batterijen.csv", 3)

n = 5
listOfHillClimber1 = []
listOfHillClimber3 = []
listOfHillClimber5 = []
listOfHillClimberNoCon = []

    # add legend

it = 5

for i in range(0, n):
    print(i)
    model = runRandom(env)
    model1 = hillClimber(env, model, it, 1)
    model1.write()
    # listOfHillClimber1.append(model1.cost)
    # model3 = hillClimber(env, model, it, 3)
    # model3.write()
    # listOfHillClimber3.append(model3.cost)
    # model5 = hillClimber(env, model, it, 5)
    # model5.write()
    # listOfHillClimber5.append(model5.cost)
    # modelNoCon = hillClimberNoCon(env, it)
    # listOfHillClimberNoCon.append(modelNoCon.cost)
# plotHistMultiple([listOfHillClimberNoCon], ["HC 3 moves (i = 10000)"], 8, n, 1)
plotHistMultiple([listOfHillClimber1, listOfHillClimber3, listOfHillClimber5, listOfHillClimberNoCon], ["HC 1 move (i = 10000)", "HC 3 moves (i = 10000)", "HC 5 moves (i = 10000)", "no constraints (1 move) (i = 1000)"], 1, n, 1)