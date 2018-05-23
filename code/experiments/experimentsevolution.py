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

def runEvolution(env, iterations, maxGen, popSize, birthsPerCouple, matingPartners, parentDominance, type):
    listOfEv = []
    for i in range(0, iterations):
        model = evolution(env, maxGen, popSize, birthsPerCouple, matingPartners, parentDominance)
        listOfEv.append(model.cost)
        model.write()
        visVillage(env, model)
    return {'results': listOfEv, 'maxGen': maxGen, 'popSize': popSize, 'birthsPerCouple': birthsPerCouple, 'matingPartners': matingPartners, 'pDom': parentDominance, 'type': type}  

def testEvolution(env, plotNumber):
    ## input par should also be an array of dicts with run parameters
    data = []

    ## change parameters here to determine how the algoritm should be tested
    iterations = 10
    data.append(runEvolution(env, iterations, 10, 10, 1, 2, 0.5, "small tryout"))
    data.append(runEvolution(env, iterations, 5, 10, 1, 1, 0.5, "selection inverted still"))
    data.append(runEvolution(env, iterations, 2, 15, 1, 1, 0.5, "selection inverted still"))

    plotHistMultiple(data, iterations, env.village, plotNumber)

## start of test
env = Environment(r"..\data\wijk3_huizen.csv", r"..\data\wijk3_batterijen.csv", 3)

# env, plotnumber 
testEvolution(env, 1)




