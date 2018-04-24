import csv
import numpy as np 

def makedistancetable(batteries, houses):
    distancetable = np.array(range(len(batteries) + 1))
    for house in houses:
        row = [house.idhouse]
        for bat in batteries:
            print(type(house.x))
            print(bat.x)
            row.append(abs((int(house.x)-int(bat.x)))+abs((int(house.y)-int(bat.y))))
        np.asarray(row)
        distancetable = np.vstack([distancetable, row])
    return(distancetable)
    
