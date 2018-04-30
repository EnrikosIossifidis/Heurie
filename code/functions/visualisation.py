import matplotlib.pyplot as plt

def visvillage(batteries, houses):
    arrayHouseX = list()
    arrayHouseY = list()
    arrayHouseZ = list()
    arrayZ = list()

    
    arrayBatteryZ = ['b','c','y','m','r']

    for house in houses:
        arrayHouseX.append(house.x)
        arrayHouseY.append(house.y)
        if house.batterij==1:
            arrayHouseZ.append(arrayBatteryZ[0])
        elif house.batterij==2:
            arrayHouseZ.append(arrayBatteryZ[1])
        elif house.batterij==3:
            arrayHouseZ.append(arrayBatteryZ[2])
        elif house.batterij==4:
            arrayHouseZ.append(arrayBatteryZ[3])
        elif house.batterij==5:
            arrayHouseZ.append(arrayBatteryZ[4])


    arrayBatteryX = list()
    arrayBatteryY = list()
    for battery in batteries:
        arrayBatteryX.append(battery.x)
        arrayBatteryY.append(battery.y)     

    # print(arrayHouseZ)
    
    plt.scatter(arrayHouseX, arrayHouseY, marker='*', c=arrayHouseZ)
    plt.scatter(arrayBatteryX, arrayBatteryY, marker='o', c=arrayBatteryZ)
    plt.scatter(arrayHouseX, arrayHouseY, marker='*', c=arrayHouseZ)
    plt.axis()
    plt.show()