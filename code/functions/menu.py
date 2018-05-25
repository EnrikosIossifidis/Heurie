from algorithms.runrandom import runRandom
from algorithms.hillclimber import hillClimber
from algorithms.simulatedannealing import simAnneal
from algorithms.kmeans import kMeans
from algorithms.evolution import evolution
from algorithms.hillclimbermovebatteries import hillClimberMoveBatteries
from functions.visualisation import visVillage
from functions.plothist import plotHist
from functions.plothistmultiple import plotHistMultiple
from classes.model import Model
from classes.environment import Environment

def menu(choice, env):

    if choice == 1:
        doRandom(env, choice)

    elif choice == 2:
        model = runRandom(env)
        doHillClimber(env, model)

    elif choice == 3:
        model = runRandom(env)
        doSimAnneal(env, model)

    elif choice == 4:
        doEvolution(env)

    elif choice == 5:
        doKmeans(env)

    elif choice == 6:
        doHillClimberMoveBatteries(env)

def doRandom(env, choice):

    print("How many times do you want to do a random?")
    iterations = int(input())
    costs = []
    for i in range(0, iterations):
        model = runRandom(env)
        model.setName("Runrandom k-means env", i)
        model.printResult()
        costs.append(model.cost)
        visVillage(env, model)

    plotHistMultiple([costs], ["random"], choice, iterations, env.village)

def doHillClimber(env, model):
    print("You are about to run a hill climber starting with a random starting model.") 
    print("Within the parameters you can choose if you want to run the hill climber with option 1: constraints (checking if the model is valid) or option 2: without constraints (returned model is not valid)")
    print("Another choice to make is what kind of mutation you want. Option 1: Move 1 house to another battery. Option 2: switch two houses between random batteries")
    print("Please fill in the following parameters separated by a space: Amount of iterations, constraint option 1 or 2, mutation option 1 or 2, amount of moves before checking")
    iterations, chooseConstraints, mutation, moves = input().split()

    hcModel = hillClimber(env, model, int(iterations), int(chooseConstraints), int(mutation), int(moves))
    name = str("Hill climber " + str(iterations) + " " + str(chooseConstraints) + " " + str(mutation) + " " + str(moves))
    hcModel.setName(name, 0)
    hcModel.printResult()
    hcModel.write(env)
    visVillage(env, hcModel)

def doSimAnneal(env, model):
    print("You are about to run a hill climber starting with a random starting model.") 
    print("Within the parameters you can choose if you want to run the hill climber with option 1: constraints (checking if the model is valid) or option 2: without constraints (returned model is not valid)")
    print("Another choice to make is what kind of mutation you want. Option 1: Move 1 house to another battery. Option 2: switch two houses between random batteries")
    print("The last choice of this algorithm is the cooling scheme. option 1 for a linear cooling scheme, option 2 for an exponential cooling scheme or option 3 for a sigmoid cooling scheme")
    print("Please fill in the following parameters separated by a space: Amount of iterations, constraint option 1 or 2, mutation option 1 or 2, amount of moves before checking, cooling scheme option 1, 2 or 3")
    iterations, chooseConstraint, mutation, moves, coolingSchedule = input().split()

    model = simAnneal(env, model, int(iterations), int(chooseConstraint), int(mutation), int(moves), int(coolingSchedule))
    name = str("SimAnneal " + str(iterations) + " " + str(chooseConstraint) + " " + str(mutation) + " " + str(moves) + " " + str(coolingSchedule))
    model.setName(name, 0)
    model.printResult()
    model.write(env)
    visVillage(env, model)

def doEvolution(env):
    print("You are about to run an evolution algorithm. Make sure you have read the readme to know exactly what the parameters do.")
    print("Please fill in the following parameters separated by a space: maximum amount of generations, population size, probability of mutation, crossover probability") 
    maximumGenerations, populationSize,  mutationProbability, crossoverProbability = input().split()
    
    evoModel = evolution(env, int(maximumGenerations), int(populationSize), 1, 1, 0.5, int(mutationProbability), int(crossoverProbability), True)
    name = str("Evolution " + str(maximumGenerations) + " " + str(populationSize) + " " + str(mutationProbability) + " " + str(crossoverProbability))
    evoModel.setName(name, 0)
    evoModel.printResult
    evoModel.write(env)
    visVillage(env, evoModel)

def doKmeans(env):
    print("You are about to run a K-means algorithm. Please fill in the following parameter: iteration")
    iteration = int(input())

    kMeansTuple = kMeans(env, iteration)
    kMeansEnv = kMeansTuple[0]
    kMeansModel = kMeansTuple[1]
    kMeansModel.calculateCosts(kMeansEnv.distanceTable)
    name = str("K-means " + str(iteration))
    kMeansModel.setName(name, 0)
    kMeansModel.printResult()
    kMeansModel.write(kMeansEnv)
    visVillage(kMeansEnv, kMeansModel)

def doHillClimberMoveBatteries(env):
    print("You are about to run a hill climber on the batteries") 
    print("Within the parameters you can choose if you want to run the hill climber with option 1: constraints (checking if the model is valid) or option 2: without constraints (returned model is not valid)")
    print("Another choice to make is what kind of mutation you want. Option 1: Move 1 house to another battery. Option 2: switch two houses between random batteries")
    print("The last choice of this algorithm is the cooling scheme. option 1 for a linear cooling scheme, option 2 for an exponential cooling scheme or option 3 for a sigmoid cooling scheme")
    print("Please fill in the following parameters separated by a space: Amount of iterations, constraint option 1 or 2, mutation option 1 or 2, amount of moves before checking, cooling scheme option 1, 2 or 3")
    iterations, chooseConstraint, mutation, moves, coolingSchedule = input().split()

    hcbTuple = hillClimberMoveBatteries(env, int(iterations), int(chooseConstraint), int(mutation), int(moves), int(coolingSchedule))
    hcbEnv = hcbTuple[0]
    hcbModel = hcbTuple[1]
    name = str("Hill Climber Moving batteries " + str(iterations) + " " + str(chooseConstraint) + " " + str(mutation) + " " + str(moves) + " " + str(coolingSchedule))
    hcbModel.setName(name, 0)
    hcbModel.printResult()
    hcbModel.write(hcbEnv)
    visVillage(hcbEnv, hcbModel)