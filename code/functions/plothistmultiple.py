import matplotlib.pyplot as plt  

def plotHistMultiple(arrays, namesOfAlgorithms, number, iterations, village):
 
    # these are the "Tableau 20" colors as RGB    
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
                (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
                (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
                (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
                (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
    
    # scale the RGB values to the [0, 1] range, which is the format matplotlib accepts    
    for i in range(len(tableau20)):    
        r, g, b = tableau20[i]    
        tableau20[i] = (r / 255., g / 255., b / 255.)    
    
    # set plot size
    plt.figure(figsize=(7, 6))    
    
    # remove the plot frame lines   
    ax = plt.subplot(111)    
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)    
    
    # ensure that the axis ticks only show up on the bottom and left of the plot       
    ax.get_xaxis().tick_bottom()    
    ax.get_yaxis().tick_left()    

    # pick colors
    colors = []
    for i in range(0, len(arrays)):
        colors.append(tableau20[i+3])

    # make actual plot
    plt.hist(arrays, bins = 15, histtype='stepfilled', alpha = 0.5, label = namesOfAlgorithms) 

    # add legend
    plt.legend(prop={'size': 10})

    # construct title and filename from input parameters
    title = "Figure " + str(number) + ". Histogram of performance, n = " + str(iterations) + "\n\n (village: " + str(village) + ")"
    name = "fig" + str(number) + "_performance_histogram_" + str(iterations) + "_v" + str(village) + ".png"
    
    # show titles and axes labels
    plt.title(title)
    plt.xlabel("cost")
    plt.ylabel("frequency")

    # save plot
    plt.savefig('../results/' + name)


