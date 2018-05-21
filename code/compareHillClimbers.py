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

env = Environment(r"..\data\wijk3_huizen.csv", r"..\data\wijk3_batterijen.csv", 3)

it = 70

listOfHillClimber1 = []
listOfHillClimber3 = []
listOfHillClimber5 = []
listOfHillClimberNoCon = []
listOfHillClimberRelax = []


for i in range(0, it):
    print(i)
    model1 = hillClimber(env, it, 1)
    listOfHillClimber1.append(model1.cost)
    model3 = hillClimber(env, it, 3)
    listOfHillClimber3.append(model3.cost)
    model5 = hillClimber(env, it, 5)
    listOfHillClimber5.append(model5.cost)
    modelNoCon = hillClimberNoCon(env, it)
    listOfHillClimberNoCon.append(modelNoCon.cost)
    modelRelax = hillClimber(env, it, 1)
    listOfHillClimberRelax.append(modelRelax.cost)

plotHistMultiple([listOfHillClimber1, listOfHillClimber3, listOfHillClimber5, listOfHillClimberNoCon], ["HC 1 move", "HC 3 moves", "HC 5 moves", "no constraints (1 move)", "relaxation"], 1, it, 3)