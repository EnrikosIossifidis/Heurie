import csv
from connect01 import connect01

# load data and connect
with open('data/wijk2_huizen.csv', 'r') as f:
    reader = csv.reader(f)
    print(reader)
    houses = list(reader)

with open('data/wijk2_batterijen.csv', 'r') as f:
    reader = csv.reader(f)
    batteries = list(reader)

# create a table with the distance from every house to every battery
# result: distancetable[n][h] - n=battery, h=house
distancetable = [0]*len(batteries)
for n in range(len(batteries)):
    distancetable[n] = list()
    for i in range(len(houses)):
        distancetable[n].append(abs((int(houses[i][0])-int(batteries[n][0])))+abs((int(houses[i][1])-int(batteries[n][1]))))

# connect and print result
connect01(batteries, houses, distancetable)
