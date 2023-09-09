class AirControlService():
    def __init__(self, dht22, relays, database):
        self.dht22 = dht22
        self.relays = relays
        self.low_temp_limit = database.fetch_limit_value('temperature_min')
        self.high_temp_limit = database.fetch_limit_value('temperature_max')
        self.low_humidity_limit = database.fetch_limit_value('humidity_min')
        self.high_humidity_limit = database.fetch_limit_value('humidity_max')
