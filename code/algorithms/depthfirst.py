from classes.model import Model
from algorithms.runrandom import runRandom
import copy
from operator import itemgetter
import numpy as np

def depthFirstBnB(model, env):

    # create the array of batteries for model
    modelBatteries = env.createModelBatteries(env.batteries)

    # initialize algorithm model
    depthFirstModel = Model(modelBatteries)
    
    # initiliaze upperbound at random cost
    model = model
    upperBound = model.cost
    levels = len(env.houses)
    solution = []

    # create stack with root houseNode
    depthFirstStack = []
    depthFirstStack.append(np.array([0]))

    while len(depthFirstStack) > 0:

        # select last item and pop it
        node = depthFirstStack.pop()
        tempCostNodes = []

        # create all children
        lenModelBatteries = len(modelBatteries)
        for i in range(0, lenModelBatteries):
 
            # create new houseNode
            newNode = np.append(node, modelBatteries[i].idBattery)
            if (len(newNode) - 1) == levels:
                if checkCapacity(newNode, env.batteries, modelBatteries, env.houses):
                    costs = model.calculateCosts(env.distanceTable)
                    if costs < upperBound:

                        upperBound = costs 
                        print(upperBound)
                        solution = newNode.tolist()

            else:
                if checkCapacity(newNode, env.batteries, modelBatteries, env.houses) and model.calculateCosts(env.distanceTable) < upperBound:
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