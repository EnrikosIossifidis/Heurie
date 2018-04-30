import matplotlib.pyplot as plt

def visVillage(batteries, houses):
    arrayHouseX = list()
    arrayHouseY = list()
    arrayHouseZ = list()
    arrayZ = list()

    
    arrayBatteryZ = ['b','c','y','m','r']

    for house in houses:
        arrayHouseX.append(house.x)
        arrayHouseY.append(house.y)
        if house.battery==1:
            arrayHouseZ.append(arrayBatteryZ[0])
        elif house.battery==2:
            arrayHouseZ.append(arrayBatteryZ[1])
        elif house.battery==3:
            arrayHouseZ.append(arrayBatteryZ[2])
        elif house.battery==4:
            arrayHouseZ.append(arrayBatteryZ[3])
        elif house.battery==5:
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