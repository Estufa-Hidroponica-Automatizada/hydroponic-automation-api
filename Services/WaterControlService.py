class WaterControlService():
    def __init__(self, ec, ph, waterLevel, waterTemp, relays, database):
        self.ec = ec
        self.ph = ph
        self.waterLevel = waterLevel
        self.waterTemp = waterTemp
        self.relays = relays
        self.low_ec_limit = database.get_low_ec_limit()
        self.high_ec_limit = database.get_high_ec_limit()
        self.low_ph_limit = database.get_low_ph_limit()
        self.high_ph_limit = database.get_high_ph_limit()
        self.low_temp_limit = database.get_low_temp_limit()
        self.high_temp_limit = database.get_high_temp_limit()
