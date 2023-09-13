from Services.DatabaseService import databaseService


class LightService():
    def __init__(self):
        self.schedule = databaseService.fetch_light_schedule()
    
    def update_schedule(self, id, hour, minute, state):
        databaseService.update_schedule(id, hour, minute, state)
        self.schedule = databaseService.fetch_light_schedule()
        return True
    
    def insert_schedule(self, hour, minute, state):
        databaseService.insert_schedule(hour, minute, state)
        self.schedule = databaseService.fetch_light_schedule()
        return True
    
    def delete_schedule(self, id):
        databaseService.delete_schedule(id)
        self.schedule = databaseService.fetch_light_schedule()
        return True
    
    def isSupposedToBeOn(self):
        return True # TODO

lightService = LightService()