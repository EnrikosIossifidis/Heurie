import matplotlib.pyplot as plt

def visVillage(env, model):
     # These are the "Tableau 20" colors as RGB.    
    tableau20 = [(31, 119, 180), (255, 127, 14), (255, 187, 120),    
              (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (44, 160, 44), (188, 189, 34),(174, 199, 232), (0, 179, 226), (255,255,255), (24,24,24)]  
    
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
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
    
    # Create color range for batteries
    arrayBatteryZ = list()
    for i in range(0,len(env.batteries)):
        arrayBatteryZ.append(tableau20[i])

    # Create a square plot, since that corresponds to the neighbourhood.   
    fig = plt.figure(figsize=(6, 6))  
  
    # get the x and y coordinates for the houses
    for battery in model.modelBatteries:
        for item in battery.houses:
            arrayHouseX.append(item.x)
            arrayHouseY.append(item.y)
            arrayZ.append(battery.idBattery)
            
            # if battery.idBattery==1:
            #     plt.plot([item.x, env.batteries[0].x], [item.y, env.batteries[0].y], linewidth = 0.7, c=arrayBatteryZ[0], alpha=0.5)
            # elif battery.idBattery==2:
            #     plt.plot([item.x, env.batteries[1].x], [item.y, env.batteries[1].y], linewidth = 0.7, c=arrayBatteryZ[1], alpha=0.5)
            # elif battery.idBattery==3:
            #     plt.plot([item.x, env.batteries[2].x], [item.y, env.batteries[2].y], linewidth = 0.7, c=arrayBatteryZ[2], alpha=0.5)
            # elif battery.idBattery==4:
            #     plt.plot([item.x, env.batteries[3].x], [item.y, env.batteries[3].y], linewidth = 0.7, c=arrayBatteryZ[3], alpha=0.5)
            # elif battery.idBattery==5:
            #     plt.plot([item.x, env.batteries[4].x], [item.y, env.batteries[4].y], linewidth = 0.7, c=arrayBatteryZ[4], alpha=0.5)

            
            # # Actual cables over grid
            # if battery.idBattery==1:
            #     plt.plot([item.x, item.x, env.batteries[0].x], [item.y, env.batteries[0].y, env.batteries[0].y], linewidth = 0.5, c=arrayBatteryZ[0], alpha=0.5)
            # elif battery.idBattery==2:
            #     plt.plot([item.x, item.x, env.batteries[1].x], [item.y, env.batteries[1].y, env.batteries[1].y], linewidth = 0.5, c=arrayBatteryZ[1], alpha=0.5)
            # elif battery.idBattery==3:
            #     plt.plot([item.x, item.x, env.batteries[2].x], [item.y, env.batteries[2].y, env.batteries[2].y], linewidth = 0.5, c=arrayBatteryZ[2], alpha=0.5)
            # elif battery.idBattery==4:
            #     plt.plot([item.x, item.x, env.batteries[3].x], [item.y, env.batteries[3].y, env.batteries[3].y], linewidth = 0.5, c=arrayBatteryZ[3], alpha=0.5)
            # elif battery.idBattery==5:
            #     plt.plot([item.x, item.x, env.batteries[4].x], [item.y, env.batteries[4].y, env.batteries[4].y], linewidth = 0.5, c=arrayBatteryZ[4], alpha=0.5)

    # put the houses in the right battery
    for idBattery in arrayZ:
            arrayHouseZ.append(tableau20[12])

    # get the x and y coordinates for the batteries
    for battery in env.batteries:
        arrayBatteryX.append(battery.x)
        arrayBatteryY.append(battery.y)  

    # Remove the plot frame lines. They are ugly.    
    ax = plt.subplot(111)    
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(True)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(True)   

    # # # Set background color
    # fig.patch.set_facecolor(tableau20[19]) 
    # ax.set_facecolor(tableau20[19])

    # Make sure your axis ticks are large enough to be easily read.  
    # You don't want your viewers squinting to read your plot.  
    plt.xticks(fontsize=8, color=tableau20[19])  
    plt.yticks(fontsize=8, color=tableau20[19])   


    # Make the title 
    plt.title("Village 1 - Distribution of houses and batteries", fontsize=14, color=tableau20[19])  
            
    # plot the visualisation    
    plt.scatter(arrayBatteryX, arrayBatteryY, marker='8', c=arrayBatteryZ)
    plt.scatter(arrayHouseX, arrayHouseY, marker='2', c=arrayHouseZ)
    plt.axis()
    plt.show()
