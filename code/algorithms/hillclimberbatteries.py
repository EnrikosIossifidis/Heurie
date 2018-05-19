from classes.model import Model
from classes.environment import Environment
from algorithms.depthfirst import createModelBatteries
from algorithms.runrandom import runRandom
from algorithms.hillclimber import hillClimber
from algorithms.simulatedannealing import acceptation
from algorithms.simulatedannealing import curTemp
from functions.visualisation import visVillage
import random
import math

def hillClimberBatteries(env, iterations, beginTemp):

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
    endTemp = 0

    while iteration <= iterations:
        currentTemp = curTemp(iteration, beginTemp, iterations)
        neighbourEnv = pickRandomNeighbour(hillClimberEnv)
        neighbourModel = hillClimber(neighbourNode, 1000)
        nodeDifference = neighbourModel.cost - costs[-1].cost

        if checkNode(costs[-1].cost, neighbourModel.cost, currentTemp):
            costs.append(neighbourModel)
            hillClimberEnv = neighbourEnv
            if costs[-1].cost < upperbound:
                upperbound = neighbourModel.cost
                print(upperbound)        
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
    hillClimberArray = [env, model]
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

def checkNode(currentCost, neighbourCost, temp):
    randomInt = random.random()
    probality = math.exp((currentCost - neighbourCost) / temp)
    if neighbourCost < currentCost:
        return True
    elif probality > randomInt:
        return True
    else:
        return False