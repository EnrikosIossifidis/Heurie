import csv
import numpy as np 

def makeDistanceTable(env):

    # create column for each battery
    distancetable = np.array(range(len(env.batteries) + 1))

    # append idHouse to left column
    for house in env.houses:
        row = [house.idHouse]

        # append distance to each battery for every house
        for bat in env.batteries:
            row.append(abs(house.x-bat.x)+abs(house.y-bat.y))

        # convert list into numpy array and add each house
        np.asarray(row)
        distancetable = np.vstack([distancetable, row])

    return(distancetable)