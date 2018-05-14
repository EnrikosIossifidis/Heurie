class Model:
    
    class Battery:
        def __init__(self, id):
            self.idBattery = id
            self.curCapacity = 0.0
            self.houses = list()

    def __init__(self, mBatteries):
        self.cost = 0
        self.modelBatteries = mBatteries
        self.name = ""
        self.listOfCosts = []

    def setName(self, algorithm, id):
        self.name = "model " + algorithm + " " + str(id+1)

    def printResult(self):
        print("cost of " + self.name + " = " + str(self.cost))

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
