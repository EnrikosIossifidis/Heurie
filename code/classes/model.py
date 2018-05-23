import csv

class Model:
    
    class Battery:
        def __init__(self, id):
            self.idBattery = id
            self.curCapacity = 0.0
            self.maxCapacity = 0
            self.houses = list()
            self.batteryDistanceList = []

        def setMaxCapacity(self, env):
            self.maxCapacity = env.batteries[self.idBattery -1].maxCapacity

        def checkCapacity(self, EnvBatteries, newHouse):
            self.curCapacity = 0
            for house in self.houses:
                self.curCapacity += house.cap 
            if self.curCapacity + newHouse.cap <= EnvBatteries[self.idBattery - 1].maxCapacity:
                return True
        
        def setCurCapacity(self):
            totalHouseCap = 0
            for house in self.houses:
                totalHouseCap += house.cap 
            self.curCapacity = totalHouseCap

        def checkOverload(self):
            totalHouseCap = 0
            for house in self.houses:
                totalHouseCap += house.cap 
            if totalHouseCap >= self.maxCapacity:
                return True
            else:
                return False

    def __init__(self, mBatteries):
        self.cost = 0
        self.modelBatteries = mBatteries
        self.name = ""
        self.listOfCosts = []

    def setName(self, algorithm, id):
        self.name = "model " + algorithm + " " + str(id+1)

    def printResult(self):
        print("cost of cables in " + self.name + " = " + str(self.cost))
    
    def write(self):
        listOfhouses = []*150
        for bat in self.modelBatteries:
            for house in bat.houses:
                listOfhouses.append([house.idHouse, bat.idBattery])
        
        # sort the list of houses on houseId
        listOfhouses = sorted(listOfhouses, key=lambda tup: tup[0])
        connections = []
        connections.append(self.cost)

        # assign battery value to connection list in order of house number
        for house in listOfhouses:
            connections.append(house[1])

        with open(r'output_queue.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(connections)

        return connections
    

    def calculateCosts(self, dt):
                    
        # make sure the cost and length are starting with 0
        cost = 0
        length = 0

        # calculate the length of the cables
        for battery in self.modelBatteries:
            for house in battery.houses:
                length += dt[house.idHouse][battery.idBattery]
        
        # calculate cost of the cables
        cost = length * 9
        self.cost = cost

    def checkValidity(self):
        # print("houses per battery:")
        # for battery in self.modelBatteries:
        #     print(len(battery.houses))
    
        for i in range(0, len(self.modelBatteries)):
            totCapHouses = 0
            for house in self.modelBatteries[i].houses:
                totCapHouses += house.cap
            # print("cap Battery")
            # print(env.batteries[i].maxCapacity)
            
            # print("cap Houses")
            # print(totCapHouses)

            # break out of loop and return False if capacity of battery is exceeded
            if totCapHouses > self.modelBatteries[i].maxCapacity:
                return False
                
        # if capacity is not exceeded in any battery, return True
        return True
    
    def printDistributionHouses(self):
        print("profile per battery:")
        for battery in self.modelBatteries:
            print("amount of houses: ", end="")  
            print(len(battery.houses), end=", ")  
            print("maximum capacity: ", end="")           
            print(battery.maxCapacity, end=", ")
            print("current capacity: ", end="")   
            battery.setCurCapacity()
            print(battery.curCapacity)
        print("total houses = {}".format(sum([len(x.houses) for x in self.modelBatteries])))



