import matplotlib.pyplot as plt  

def plotHistMultiple(data, iterations, village, number):
    

    ## data[i] = {'results': [4098, 5000, 3800], 'maxGen': 10, 'popSize': 200, 'type': "two children per parent"}  

    # unpack data
    arrays = []
    legendDescription = []
    for sim in data:
        arrays.append(sim['results'])
        legendDescription.append(str(sim['maxGen']) + ", " + str(sim['popSize']) + ", " + str(sim['birthsPerCouple']) + ", " + str(sim['matingPartners']) + ", " + str(sim['pDom']) + ", " + str(sim['type']))
 
    # These are the "Tableau 20" colors as RGB.    
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
                (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
                (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
                (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
                (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
    
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
    for i in range(len(tableau20)):    
        r, g, b = tableau20[i]    
        tableau20[i] = (r / 255., g / 255., b / 255.)    
    
    # # You typically want your plot to be ~1.33x wider than tall. This plot is a rare    
    # # exception because of the number of lines being plotted on it.    
    # # Common sizes: (10, 7.5) and (12, 9)    
    # plt.figure(figsize=(12, 6))    
    
    # Remove the plot frame lines. They are unnecessary chartjunk.    
    ax = plt.subplot(111)    
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)    
    
    # Ensure that the axis ticks only show up on the bottom and left of the plot.    
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.    
    ax.get_xaxis().tick_bottom()    
    ax.get_yaxis().tick_left()    

    # pick colors
    colors = []
    for i in range(0, len(arrays)):
        colors.append(tableau20[i+3])

    # make actual plot
    plt.hist(arrays, bins = 15, color = colors, histtype='stepfilled', alpha = 0.5, fill=False, label = legendDescription) 

    # add legend
    handles, labels = ax.get_legend_handles_labels()
    lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1), title="maxGen, popSize, birthsPerCouple, matPartners, parentDom")
    # ax.grid('on')

    
    # construct title and filename from input parameters
    title = "Figure " + str(number) + ". Histogram of performance, evolution, n = " + str(iterations) + "\n\n (village: " + str(village) + ")"
    name = "fig" + str(number) + "_evolution_i" + str(iterations) + "_v" + str(village) + ".png"
    
    # show titles and axes labels
    plt.title(title)
    plt.xlabel("cost")
    plt.ylabel("frequency")

    # save plot
    plt.savefig('../results/personalresults/' + name, bbox_extra_artists=(lgd,), bbox_inches='tight')


