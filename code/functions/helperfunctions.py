import os
import csv

def importHouses(housesCsv):
    # load data and connect
    with open(housesCsv, 'r') as f:
        reader = csv.reader(f)
        items = list(reader)
        print(items)
        houses = []
        
        # for item in items:

            # houses.append()    


def importBatteries():
    with open('data/wijk2_batterijen.csv', 'rb') as f:
        reader = csv.reader(f)
        # batteries = list(reader)