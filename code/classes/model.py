class Model:
    
    class Battery:
        def __init__(self, id):
            self.idBattery = id
            self.curCapacity = 0.0
            self.houses = list()

    def __init__(self, cost, mBatteries):
        self.cost = cost
        self.modelBatteries = mBatteries
        self.name = ""

    def setName(self, algorithm, id):
        self.name = "model " + algorithm + " " + str(id+1)

    def printResult(self):
        print("cost of " + self.name + " = " + str(self.cost))