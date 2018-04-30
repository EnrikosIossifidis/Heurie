class Battery:
    def __init__(self, id, xCoor, yCoor, batCap):
        self.idBattery = id
        self.x = xCoor
        self.y = yCoor
        self.maxCapacity = batCap
        self.curCapacity = 0.0
        self.house = list()

        
