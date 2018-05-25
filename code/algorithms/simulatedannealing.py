from classes.model import Model
from algorithms.runrandom import runRandom
from algorithms.hillclimber import chooseClimbModel
from algorithms.evolution import writeProgress
import random
import math
import time
import datetime

def simAnneal(env, model, iterations, chooseConstraint, mutation, moves, coolingSchedule):

    # create a list with all the lowest costs per iteration for plotting purposes
    costs = []

    # run a random as a starting state
    boundModel = model
    
    # initialize temperatures and constant for cooling schemes
    beginTemp = 1000
    endTemp = 1
    iteration = 1

    # run the algorithm for the amount of iterations given
    for i in range(iteration, iterations):

        # copy old Model
        climberModel = boundModel

        # keep climbing until legit solution is found
        modelClimber = chooseClimbModel(chooseConstraint, climberModel, mutation, moves)

        # calculate the costs of the returned model
        modelClimber.calculateCosts(env.distanceTable)

        # get the current temp
        temp = chooseCoolingSchedule(beginTemp, endTemp, iteration, iterations, coolingSchedule)

        # get a random number between 0 and 1
        randomNum = random.random()

        # compare the result and anneal
        if (acceptation(boundModel, modelClimber, temp) > randomNum):
            boundModel = modelClimber

        # append lowest costs to the list for comparison    
        costs.append(boundModel.cost)

        iteration += 1

    # return the list of costs for plotting
    boundModel.listOfCosts = costs
    return boundModel

def chooseCoolingSchedule(beginTemp, endTemp, iteration, iterations, coolingSchedule):

    # choose the chosen cooling schedule
    if coolingSchedule == 1:
        return curTempLinear(beginTemp, endTemp, iteration, iterations)
    if coolingSchedule == 2:
        return curTempExp(beginTemp, endTemp, iteration, iterations)
    if coolingSchedule == 3:
        return curTempSigmoid(beginTemp, endTemp, iteration, iterations)

def curTempLinear(beginTemp, endTemp, iteration, iterations):
    return (beginTemp - (iteration*((beginTemp - endTemp)/iterations)))

def curTempExp(beginTemp, endTemp, iteration, iterations):
    if endTemp == 0:
        endTemp = 0.001
    return (beginTemp*(endTemp/beginTemp)**(iteration/iterations))
    
def curTempSigmoid(beginTemp, endTemp, iteration, iterations):
    a = 0.3
    sigmoid = endTemp + (beginTemp - endTemp) / (1 + math.exp(a*(iteration - (iterations/2))))
    return sigmoid

def acceptation(boundModel, modelClimbed, temp):

    if (modelClimbed.cost < boundModel.cost):

        # if the new costs are lower, return 1
        return 1.0
    
    # else return the calculation for the acceptation
    return math.exp((boundModel.cost - modelClimbed.cost) / temp)