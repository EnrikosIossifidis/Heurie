class Model:
    
    class Battery:
        def __init__(self, id):
            self.idBattery = id
            self.curCapacity = 0.0
            self.houses = list()

    def __init__(self, cost, mBatteries):
        self.cost = cost
        self.modelBatteries = mBatteries