class WaterControlService():
    def __init__(self, ec, ph, waterLevel, waterTemp, relays, database):
        self.ec = ec
        self.ph = ph
        self.waterLevel = waterLevel
        self.waterTemp = waterTemp
        self.relays = relays
        self.low_ec_limit = database.fetch_limit_value('ec_min')
        self.high_ec_limit = database.fetch_limit_value('ec_max')
        self.low_ph_limit = database.fetch_limit_value('ph_min')
        self.high_ph_limit = database.fetch_limit_value('ph_max')
        self.low_temp_limit = database.fetch_limit_value('water_temperature_min')
        self.high_temp_limit = database.fetch_limit_value('water_temperature_max')
