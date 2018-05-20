class Model:
    
    class Battery:
        def __init__(self, id):
            self.idBattery = id
            self.curCapacity = 0.0
            self.houses = list()
        
        def checkCapacity(self, id, EnvBatteries, houses, newHouse):
            totalHouseCap = 0
            for house in houses:
                totalHouseCap += house.cap 
                
            if totalHouseCap + newHouse.cap <= EnvBatteries[id - 1].maxCapacity:
                return True
    

    def __init__(self, mBatteries):
        self.cost = 0
        self.modelBatteries = mBatteries
        self.name = ""
        self.listOfCosts = []

    def setName(self, algorithm, id):
        self.name = "model " + algorithm + " " + str(id+1)

    def printResult(self):
        print("cost of cables in " + self.name + " = " + str(self.cost))

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

    def checkValidity(self, env):
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
            if totCapHouses > env.batteries[i].maxCapacity:
                return False
        # if capacity is not exceeded in any battery, return True
        return True
    


