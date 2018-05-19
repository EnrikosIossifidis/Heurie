from classes.model import Model
from classes.environment import Environment
from algorithms.depthfirst import createModelBatteries
from algorithms.runrandom import runRandom
from algorithms.hillclimber import hillClimber
from algorithms.simulatedannealing import sigmoid
from algorithms.simulatedannealing import acceptation
from algorithms.simulatedannealing import curTempLinear
import random
import math

def hillClimberBatteries(env, iterations, beginTemp, endTemp):

    # keep list with scores and upperbound
    costs = []
    upperbound = 0

    # create the array of batteries for model
    hillClimberEnv = env

    # initial hillclimber score after randomizing batteries
    randomizeBatteries(hillClimberEnv.batteries)        
    costs.append(hillClimber(hillClimberEnv, 1000))
    upperbound = costs[0].cost

    iteration = 1

    while iteration <= iterations:
        currentTemp = sigmoid(a, beginTemp, endTemp, iteration, iterations)
        print(iteration)
        print(currentTemp)

        neighbourEnv = pickRandomNeighbour(hillClimberEnv)
        neighbourModel = hillClimber(neighbourEnv, 1000)
        deltaNodes = neighbourModel.cost - costs[-1].cost
        if  deltaNodes < 0 or checkNode(iteration, iterations, deltaNodes, currentTemp):
            costs.append(neighbourModel)
            hillClimberEnv = neighbourEnv          
            if costs[-1].cost < upperbound:
                upperbound = neighbourModel.cost
        else:
            costs.append(costs[-1])
        iteration += 1

    costsList = []
    for node in costs:
        costsList.append(node.cost)
   
    return makeHillClimberPakackage(hillClimberEnv, costs[-1], costsList)

def makeHillClimberPakackage(env, model, costs):

    model.listOfCosts = costs
    model.setName("batteryHillClimber", 1)
    model.printResult()
    hillClimberArray = [env, model, costs]
    return hillClimberArray

def pickRandomNeighbour(inputBatteries):

    nodeBatteries = inputBatteries
    randomBatInt = random.randint(0, len(nodeBatteries.batteries) - 1)
    randomBat = nodeBatteries.batteries[randomBatInt]
    randomYorX = random.randint(1, 2)
    randomPosOrNeg = random.choice([-1, 1])

    if randomYorX == 1:
        nodeBatteries.batteries[randomBatInt].x += randomPosOrNeg
    elif randomYorX == 2:
        nodeBatteries.batteries[randomBatInt].y += randomPosOrNeg 

    return nodeBatteries

def randomizeBatteries(batteries):
    neighbourhoodLength = 50

    for battery in batteries:
        battery.x = random.randint(0, neighbourhoodLength)
        battery.y = random.randint(0, neighbourhoodLength)

def checkNode(iteration, iterations, delta, temp):
    randomInt = random.random()
    probality = math.exp(-delta / temp)
    if probality > randomInt:
        return True
    else:
        return False