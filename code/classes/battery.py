class Battery:
    def __init__(self, id, xCoor, yCoor, batCap):
        self.idbattery = id
        self.x = xCoor
        self.y = yCoor
        self.maxcapacity = batCap
        self.curcapacity = 0.0
        self.house = list()

        
