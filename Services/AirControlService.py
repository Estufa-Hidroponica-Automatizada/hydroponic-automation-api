class AirControlService():
    def __init__(self, dht22, relays, database, limitService):
        self.dht22 = dht22
        self.relays = relays
        self.database = database
        self.limitService = limitService
