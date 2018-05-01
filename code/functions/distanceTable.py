import csv
import numpy as np 

def makeDistanceTable(env):
    distancetable = np.array(range(len(env.batteries) + 1))
    for house in env.houses:
        row = [house.idHouse]
        for bat in env.batteries:
            row.append(abs(house.x-bat.x)+abs(house.y-bat.y))
        np.asarray(row)
        distancetable = np.vstack([distancetable, row])
    return(distancetable)