import csv
import numpy as np 

def makeDistanceTable(batteries, houses):
    distanceTable = np.array(range(len(batteries) + 1))
    for house in houses:
        row = [house.idHouse]
        for bat in batteries:
            print(type(house.x))
            print(bat.x)
            row.append(abs((int(house.x)-int(bat.x)))+abs((int(house.y)-int(bat.y))))
        np.asarray(row)
        distanceTable = np.vstack([distanceTable, row])
    return distanceTable
