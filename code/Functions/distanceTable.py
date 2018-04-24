import csv
import numpy as np 

def makeDistanceTable(batteries, houses):
    distanceTable = np.array(range(0,6))
    for house in houses:
        row = []
        row.append(house.idHouse)
        for bat in batteries:
            row.append((house.x-bat.x)+(house.y-bat.y))
        np.asarray(row)
        distanceTable = np.vstack([distanceTable, row])
    print(distanceTable)