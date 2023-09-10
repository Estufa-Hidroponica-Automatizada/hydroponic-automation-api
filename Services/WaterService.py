class WaterService():
    def __init__(self, ec, ph, waterLevel, waterTemp, relays, database, limitService):
        self.ec = ec
        self.ph = ph
        self.waterLevel = waterLevel
        self.waterTemp = waterTemp
        self.relays = relays
        self.database = database
        self.limitService = limitService
