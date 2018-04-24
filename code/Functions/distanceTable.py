import csv
import numpy as np 

def makeDistanceTable(batteries, houses):
    distanceTable = np.array(range(len(batteries) + 1))
    for house in houses:
        row = [house.idHouse]
        for bat in batteries:
            row.append(abs(house.x-bat.x)+abs(house.y-bat.y))
        np.asarray(row)
        distanceTable = np.vstack([distanceTable, row])
    return distanceTable
