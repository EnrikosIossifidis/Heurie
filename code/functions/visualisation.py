import matplotlib.pyplot as plt

def visvillage(batteries, houses):
    arrayHouseX = list()
    arrayHouseY = list()
    for house in houses:
        arrayHouseX.append(house.x)
        arrayHouseY.append(house.y)

    arrayBatteryX = list()
    arrayBatteryY = list()
    for battery in batteries:
        arrayBatteryX.append(battery.x)
        arrayBatteryY.append(battery.y)     
        
    arrayHouseZ = ['b']*30+['c']*30+['y']*30+['m']*30+['r']*30
    arrayBatteryZ = ['b','c','y','m','r']

    plt.scatter(arrayHouseX, arrayHouseY, marker='*', c=arrayHouseZ)
    plt.scatter(arrayBatteryX, arrayBatteryY, marker='o', c=arrayBatteryZ)
    plt.scatter(arrayHouseX, arrayHouseY, marker='*', c=arrayHouseZ)
    plt.axis()
    plt.show()