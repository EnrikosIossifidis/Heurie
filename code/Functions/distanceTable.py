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
<<<<<<< HEAD
        distancetable = np.vstack([distancetable, row])
    print(distancetable)
    
=======
        distanceTable = np.vstack([distanceTable, row])
    return distanceTable
>>>>>>> 0e6b5cee310735465518c97c2817b4b641b64005
