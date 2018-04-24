import csv
import os
from Functions.distanceTable import makeDistanceTable
from classes.Battery import Battery
from classes.House import House

# load data and connect
house_list = []
house_file = House()
house_file.idHouse = 5
house_file.x = 22
house_file.y = 11
house_list.append(house_file)

bat_list = []
for i in range(5):
    battery_file = Battery()
    battery_file.x = i
    battery_file.y = i
    bat_list.append(battery_file)

makeDistanceTable(bat_list, house_list)

