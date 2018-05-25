from classes.model import Model
from algorithms.runrandom import runRandom
import copy
from operator import itemgetter
import numpy as np
import time
import datetime

def depthFirstBnB(env):

    # create the array of batteries for model
    modelBatteries = env.createModelBatteries()

    # initialize algorithm model
    depthFirstModel = Model(modelBatteries)
    
    # initiliaze upperbound at random cost, levels and solution
    model = runRandom(env)
    model.calculateCosts(env.distanceTable)
    upperBound = model.cost
    levels = len(env.houses)
    solution = []

    # create stack with root houseNode
    depthFirstStack = []
    depthFirstStack.append(np.array([0]))

    while len(depthFirstStack) > 0:

        # select last item and pop it
        node = depthFirstStack.pop()

        # create array to put best childnode on top of the stack
        tempCostNodes = []

        # create all children
        lenModelBatteries = len(modelBatteries)
        for i in range(0, lenModelBatteries):
 
            # create new houseNode
            newNode = np.append(node, modelBatteries[i].idBattery)

            # check for legit solution if all houses are connected
            if (len(newNode) - 1) == levels:
                if checkCapacity(newNode, env.batteries, modelBatteries, env.houses):
                    newModel = makeModel(newNode, env)

                    # set new upperbound for Branch-n-Bound and add solution to list
                    if newModel.cost < upperBound:
                        upperBound = newModel.cost 
                        solution = newNode.tolist()
            
            # check if there isn't over capacity
            else:
                if checkCapacity(newNode, env.batteries, modelBatteries, env.houses):
                    newModel = makeModel(newNode, env)

                    # check if current node isn't already higher than upperbound
                    if newModel.cost < upperBound:
                        tempCostNodes.append([env.distanceTable[len(newNode) - 1][newNode[-1]], newNode])
            
                else:
                    continue

        # childnode with lowest cost on top of the stack
        tempCostNodes = sorted(tempCostNodes, key=itemgetter(0), reverse = True)
        tempCostNodes = [node[1] for node in tempCostNodes]
        depthFirstStack.extend(tempCostNodes)

    # make depth first model and update battery capacities
    lenSolution = len(solution)
    for i in range(1, lenSolution):
        depthFirstModel.modelBatteries[solution[i] - 1].houses.append(env.houses[i - 1])
        depthFirstModel.modelBatteries[solution[i] - 1].curCapacity += env.houses[i - 1].cap

    depthFirstModel.calculateCosts(env.distanceTable)
    return depthFirstModel

def checkCapacity(newNode, envBatteries, mBatteries, houses):
    
    capacities = []
    check = False
    lenEnvBatteries = len(envBatteries)
    lenNewNode = len(newNode)
    for i in range(0, lenEnvBatteries):
        capacities.append(0)

    for i in range(1, lenNewNode):
        capacities[newNode[i] - 1] += houses[i - 1].cap 
        if capacities[newNode[i] - 1] < envBatteries[newNode[i] - 1].maxCapacity:
            check = True
        else:
            return False
    
    if check == True:
        return True

def makeModel(node, env):
  
    nodeModelBatteries = env.createModelBatteries()
    
    for i in range (1, len(node)):
        nodeModelBatteries[node[i] - 1].houses.append(env.houses[i - 1])

    nodeModel = Model(nodeModelBatteries)
    nodeModel.calculateCosts(env.distanceTable)
    return nodeModel
    
