import matplotlib.pyplot as plt


def visVillage(env, model):
    
     # these are the "Tableau 20" colors as RGB    
    tableau20 = [(31, 119, 180), (255, 127, 14),    
              (152, 223, 138), (214, 39, 40),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (44, 160, 44), (188, 189, 34),(174, 199, 232), (0, 179, 226), (255,255,255), (24,24,24)]  
    
    # scale the RGB values to the [0, 1] range, which is the format matplotlib accepts   
    for i in range(len(tableau20)):    
        r, g, b = tableau20[i]    
        tableau20[i] = (r / 255., g / 255., b / 255.) 
    
    # create lists to fill the visualisation
    arrayHouseX = list()
    arrayHouseY = list()
    arrayHouseZ = list()
    arrayBatteryX = list()
    arrayBatteryY = list()
    arrayZ = list()
    
    # create color range for batteries
    arrayBatteryZ = list()
    for i in range(0,len(env.batteries)):
        arrayBatteryZ.append(tableau20[i])

    # create a square plot, since that corresponds to the neighbourhood   
    fig = plt.figure(figsize=(6, 6))  
  
    # get the x and y coordinates for the houses
    for battery in model.modelBatteries:
        for item in battery.houses:
            arrayHouseX.append(item.x)
            arrayHouseY.append(item.y)
            arrayZ.append(battery.idBattery)
            
            if battery.idBattery==1:
                plt.plot([item.x, env.batteries[0].x], [item.y, env.batteries[0].y], linewidth = 0.7, c=arrayBatteryZ[0], alpha=0.5)
            elif battery.idBattery==2:
                plt.plot([item.x, env.batteries[1].x], [item.y, env.batteries[1].y], linewidth = 0.7, c=arrayBatteryZ[1], alpha=0.5)
            elif battery.idBattery==3:
                plt.plot([item.x, env.batteries[2].x], [item.y, env.batteries[2].y], linewidth = 0.7, c=arrayBatteryZ[2], alpha=0.5)
            elif battery.idBattery==4:
                plt.plot([item.x, env.batteries[3].x], [item.y, env.batteries[3].y], linewidth = 0.7, c=arrayBatteryZ[3], alpha=0.5)
            elif battery.idBattery==5:
                plt.plot([item.x, env.batteries[4].x], [item.y, env.batteries[4].y], linewidth = 0.7, c=arrayBatteryZ[4], alpha=0.5)         

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

    # set axes 
    plt.xticks(fontsize=8, color=tableau20[17])  
    plt.yticks(fontsize=8, color=tableau20[17])   

    # set the title 
    plt.title("Village " + str(env.village) + " - " + model.name + "\n Connections between houses and batteries" , fontsize=10, color=tableau20[17])  
            
    # plot the visualisation    
    plt.scatter(arrayBatteryX, arrayBatteryY, marker='8', c=arrayBatteryZ)
    plt.scatter(arrayHouseX, arrayHouseY, marker='2', c=arrayHouseZ)

    # save the model into a png file in the results map
    name = str(model.cost) + "_v" + str(env.village) + ".png"
    plt.savefig('../results/personalresults/' + name)

