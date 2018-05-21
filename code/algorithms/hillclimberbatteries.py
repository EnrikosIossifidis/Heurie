from classes.model import Model
from classes.environment import Environment
from algorithms.runrandom import runRandom
from algorithms.hillclimber import hillClimber
from algorithms.depthfirst import createModelBatteries
from algorithms.simulatedannealing import sigmoid
from algorithms.simulatedannealing import acceptation
from algorithms.simulatedannealing import curTempLinear
from algorithms.simulatedannealing import curTempLog
from operator import itemgetter
import random
import math

def hillClimberBatteries(env, iterations, beginTemp, endTemp):

    # keep list with scores and upperbound
    costs = []

    # create the array of batteries for model
    hillClimberEnv = env

    # initial hillclimber score after randomizing batteries
    randomizeBatteries(hillClimberEnv.batteries)  
    costs.append(hillClimber(hillClimberEnv, 10, 1))

    iteration = 1

    # keep searching unit stopcriterium is reached
    while iteration <= iterations:

        # calculate current temp (linear, exponential, sigmoidal)
        currentTemp = curTempLog(beginTemp, iteration)

        # make random move for a new state and calculate costs with help from hillclimber
        neighbourEnv = pickRandomNeighbour(hillClimberEnv)
        neighbourModel = hillClimber(neighbourEnv, 10, 1)

        # calculate difference between new state and previous state 
        deltaNodes = neighbourModel.cost - costs[-1].cost

        # accept new state if lower costs or if loss is accepted by chance
        if  deltaNodes < 0 or checkNode(iteration, iterations, deltaNodes, currentTemp):
            costs.append(neighbourModel)
            hillClimberEnv = neighbourEnv
        
        # append previous state if new state is rejected
        else:
            costs.append(costs[-1])
        iteration += 1

    # make list of costs for plotting purposes
    costsList = []
    for node in costs:
        costsList.append(node.cost)
   
    return makeHillClimberPakackage(hillClimberEnv, costs[-1], costsList)

def makeHillClimberPakackage(env, model, costs):

    # adjust model for plotting purposes
    model.listOfCosts = costs
    model.setName("batteryHillClimber", 1)
    model.printResult()

    # make list of required items for returning to main
    hillClimberBatteryList = [env, model, costs]
    return hillClimberBatteryList

def pickRandomNeighbour(inputBatteries):

    # select random battery
    nodeBatteries = inputBatteries
    randomBatInt = random.randint(0, len(nodeBatteries.batteries) - 1)
    randomBat = nodeBatteries.batteries[randomBatInt]

    # select random move
    randomYorX = random.randint(1, 2)
    randomPosOrNeg = random.choice([-1, 1])

    # adjust random battery with random move
    if randomYorX == 1:
        nodeBatteries.batteries[randomBatInt].x += randomPosOrNeg
    elif randomYorX == 2:
        nodeBatteries.batteries[randomBatInt].y += randomPosOrNeg 

    return nodeBatteries

def randomizeBatteries(batteries):
    
    # grid length
    neighbourhoodLength = 50

    # randomize position of all batteries
    for battery in batteries:
        battery.x = random.randint(0, neighbourhoodLength)
        battery.y = random.randint(0, neighbourhoodLength)

def checkNode(iteration, iterations, delta, temp):

    # check if new state is accepted
    randomInt = random.random()
    probality = math.exp(-delta / temp)

    if probality > randomInt:
        return True
    else:
        return False