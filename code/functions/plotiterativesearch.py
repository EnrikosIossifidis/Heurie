import matplotlib.pyplot as plt


def plotIterativeSearch(arrays, number, nameAlgorithm, village):
    
     # these are the "Tableau 20" colors as RGB    
    tableau20 = [(31, 119, 180), (255, 127, 14), (255, 187, 120),    
              (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (44, 160, 44), (188, 189, 34),(174, 199, 232), (0, 179, 226), (255,255,255), (24,24,24)]  
    
    # scale the RGB values to the [0, 1] range, which is the format matplotlib accepts    
    for i in range(len(tableau20)):    
        r, g, b = tableau20[i]    
        tableau20[i] = (r / 255., g / 255., b / 255.) 
    
    plt.figure(figsize=(8, 6))    

    # Remove the plot frame lines 
    ax = plt.subplot(111)    
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(True)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(True)   
  .  
    # construct title and filename from input parameters
    title = "Figure " + str(number) + ". Progress over iterations of " + nameAlgorithm + "\n\n (village: " + str(village) + ")"
    name = "fig" + str(number) + "_progress_iterations_" + nameAlgorithm + "_v" + str(village)

    # add axis labels
    plt.xlabel("iterations")
    plt.ylabel("cost")
    plt.xticks(fontsize=8, color=tableau20[19])  
    plt.yticks(fontsize=8, color=tableau20[19])   

    # show title 
    plt.title(title)

    # plot the visualisation   
    for array in arrays:          
        plt.plot(array)

    plt.axis()

    # save the model into a png file in the results map
    name = name + ".png"
    plt.savefig('../results/personalresults/' + name)


    

    


