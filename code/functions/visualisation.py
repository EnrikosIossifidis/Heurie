import matplotlib.pyplot as plt

def visVillage(env, model):

    # create lists to fill the visualisation
    arrayHouseX = list()
    arrayHouseY = list()
    arrayHouseZ = list()
    arrayBatteryX = list()
    arrayBatteryY = list()
    arrayZ = list()

    # create the array of colours
    arrayBatteryZ = ['b','c','y','m','r']

    # get the x and y coordinates for the houses
    for battery in model.modelBatteries:
        for item in battery.houses:
            arrayHouseX.append(item.x)
            arrayHouseY.append(item.y)
            arrayZ.append(battery.idBattery)

    # put the houses in the right battery
    for idBattery in arrayZ:
        if idBattery==1:
            arrayHouseZ.append(arrayBatteryZ[0])
        elif idBattery==2:
            arrayHouseZ.append(arrayBatteryZ[1])
        elif idBattery==3:
            arrayHouseZ.append(arrayBatteryZ[2])
        elif idBattery==4:
            arrayHouseZ.append(arrayBatteryZ[3])
        elif idBattery==5:
            arrayHouseZ.append(arrayBatteryZ[4])      

    # get the x and y coordinates for the batteries
    for battery in env.batteries:
        arrayBatteryX.append(battery.x)
        arrayBatteryY.append(battery.y)  
        
    # plot the visualisation    
    plt.scatter(arrayHouseX, arrayHouseY, marker='*', c=arrayHouseZ)
    plt.scatter(arrayBatteryX, arrayBatteryY, marker='o', c=arrayBatteryZ)
    plt.scatter(arrayHouseX, arrayHouseY, marker='*', c=arrayHouseZ)
    plt.axis()
    plt.show()