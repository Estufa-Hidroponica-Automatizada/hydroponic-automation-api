from Services.DatabaseService import DatabaseService


class LightService():
    def __init__(self, light, relays, database: DatabaseService):
        self.dht22 = light
        self.relays = relays
        self.database = database
        self.schedule = self.database.fetch_light_schedule()
    
    def update_schedule(self, id, hour, minute, state):
        self.database.update_schedule(id, hour, minute, state)
        self.schedule = self.database.fetch_light_schedule()
        return True
    
    def insert_schedule(self, hour, minute, state):
        self.database.insert_schedule(hour, minute, state)
        self.schedule = self.database.fetch_light_schedule()
        return True
    
    def delete_schedule(self, id):
        self.database.delete_schedule(id)
        self.schedule = self.database.fetch_light_schedule()
        return True

