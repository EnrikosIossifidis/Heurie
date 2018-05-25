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

print("What algorithm do you want to use? Type the number corresponding with the algorithm.")
print("For getting the distribution of house to batteries - 1: Random, 2: Depth first with branch & Bound 3: Hill climber, 4: Simulated Annealing, 5:Evolution")
print("For getting new locaties of the batteries - 6: K-means, 7: Hill climber on the batteries")
choice = int(input())

menu(choice, env)