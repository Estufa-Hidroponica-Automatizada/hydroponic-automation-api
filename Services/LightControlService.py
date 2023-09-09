class LightControlService():
    def __init__(self, light, relays, database):
        self.dht22 = light
        self.relays = relays
        self.schedule = database.fetch_light_schedule()
