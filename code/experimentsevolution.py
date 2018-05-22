import csv
import os
from algorithms.runrandom import runRandom
from algorithms.evolution import evolution
from algorithms.hillclimber import hillClimber
from algorithms.depthfirst import depthFirstBnB 
from functions.visualisation import visVillage
from functions.plothist import plotHist
from functions.plothistmultiplepop import plotHistMultiple
from functions.plotiterativesearch import plotIterativeSearch
from classes.model import Model
from classes.environment import Environment

def runEvolution(env, iterations, maxGen, popSize, birthRate, parentDominance, type):
    listOfEv = []
    for i in range(0, iterations):
        model = evolution(env, maxGen, popSize, birthRate, parentDominance)
        listOfEv.append(model.cost)
        print(model.cost)
    return {'results': listOfEv, 'maxGen': maxGen, 'popSize': popSize, 'birthRate': birthRate, 'pDom': parentDominance, 'type': type}  

def testEvolution(env, plotNumber):
    ## input par should also be an array of dicts with run parameters
    data = []

    ## change parameters here to determine how the algoritm should be tested
    iterations = 10
    data.append(runEvolution(env, iterations, 10, 50, 1, 0.2, "no "))
    data.append(runEvolution(env, iterations, 10, 100, 1, 0.2, "no "))
    data.append(runEvolution(env, iterations, 10, 50, 1, 0.2, "no "))

    plotHistMultiple(data, iterations, env.village, plotNumber)

## start of test
env = Environment(r"..\data\wijk3_huizen.csv", r"..\data\wijk3_batterijen.csv", 3)

 
testEvolution(env, 7)




