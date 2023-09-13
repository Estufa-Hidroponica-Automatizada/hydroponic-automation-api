import datetime
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
        now = datetime.datetime.now()
        current_hour, current_minute = now.hour, now.minute

        latest_time = None
        latest_state = None

        for row in self.schedule:
            id, hour, minute, state = row

            time_diff = (current_hour - hour) * 60 + (current_minute - minute)

            if time_diff >= 0 and (latest_time is None or time_diff < latest_time):
                latest_time = time_diff
                latest_state = state

        return True if latest_state == 1 else False

lightService = LightService()