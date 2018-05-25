import csv
import os
import sys
from functions.menu import menu
from classes.environment import Environment


try:
    village = int(sys.argv[1])
    if village == 1:
        env = Environment(r"..\data\wijk1_huizen.csv", r"..\data\wijk1_batterijen.csv", 1)
    elif village == 2:
        env = Environment(r"..\data\wijk2_huizen.csv", r"..\data\wijk2_batterijen.csv", 2)
    elif village == 3:
        env = Environment(r"..\data\wijk3_huizen.csv", r"..\data\wijk3_batterijen.csv", 3)
except IndexError:
    sys.exit("Please use main.py with a village number. For example: main.py 1")

print("What algorithm would you like to run? Type the number corresponding with the algorithm.\n")
print("To make a model of the connection between houses and batteries: \n1: Random \n2: Depth first with branch & bound \n3: Stochastic hillclimber \n4: Simulated Annealing \n5: Evolution\n")
print("To make a model that determines the locations of the batteries: \n6: K-means \n7: Stochastic hillclimber on the location of batteries")
choice = int(input())

menu(choice, env)