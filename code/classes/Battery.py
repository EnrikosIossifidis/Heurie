class Battery:
    def __init__(self, id, xCoor, yCoor, maxCap):
        self.idBattery = id
        self.x = xCoor
        self.y = yCoor
        self.maxCapacity = maxCap
        self.curCapacity = 0.0
        self.House = list()

        