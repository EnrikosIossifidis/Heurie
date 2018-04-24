import csv
#from classes import House

def ImportHouses(housesCsv):
    # load data and connect
    houseCsvPath = 'data/wijk2_huizen.csv'
    with open(houseCsvPath, 'r') as f:
        reader = csv.reader(f)
        items = list(reader)
        print(items)
#        houses = []

        # for item in items:
            
            # houses.append()    
        
    
def ImportBatteries():
    with open('data/wijk2_batterijen.csv', 'rb') as f:
        reader = csv.reader(f)
        # batteries = list(reader)