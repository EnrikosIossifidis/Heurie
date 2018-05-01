class Environment:
    class Battery:
        def __init__(self, id, xCoor, yCoor, batCap):
            self.idBattery = id
            self.x = xCoor
            self.y = yCoor
            self.maxCapacity = batCap

    class House:
        def __init__(self, id, xCoor, yCoor, houseCap):
            self.idHouse = id
            self.x = xCoor
            self.y = yCoor
            self.cap = houseCap
