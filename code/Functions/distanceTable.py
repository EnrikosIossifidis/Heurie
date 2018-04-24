import csv
import numpy as np 

def makedistancetable(batteries, houses):
    distancetable = np.array(range(len(batteries) + 1))
    for house in houses:
        row = [house.idHouse]
        for bat in batteries:
            row.append(abs(house.x-bat.x)+abs(house.y-bat.y))
        np.asarray(row)
        distancetable = np.vstack([distancetable, row])
    return(distancetable)
    
