class AirControlService():
    def __init__(self, dht22, relays, database):
        self.dht22 = dht22
        self.relays = relays
        self.low_temp_limit = database.get_low_temp_limit()
        self.high_temp_limit = database.get_high_temp_limit()
        self.low_humidity_limit = database.get_low_humidity_limit()
        self.high_humidity_limit = database.get_high_humidity_limit()
