import datetime
import pytz
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
    
    def delete_all_schedule(self):
        databaseService.delete_all_schedule()
        self.schedule = databaseService.fetch_light_schedule()
        return True
    
    def isSupposedToBeOn(self):
        now = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
        current_hour, current_minute = now.hour, now.minute

        latest_state = None
        latest_time_diff = None

        for row in self.schedule:
            id, hour, minute, state = row

            time_diff = (current_hour - hour) * 60 + (current_minute - minute)

            if latest_time_diff is None or (time_diff < latest_time_diff and (latest_time_diff >= 0 and time_diff >= 0) or (latest_time_diff < 0 and time_diff < 0)):
                latest_state = state
                latest_time_diff = time_diff

        return latest_state == 1
    
    def _from_list_to_light_schedule(self, input_data):
        light_schedule = []
        for entry in input_data:
            light_schedule.append({"hour": entry[1], "minute": entry[2], "state": entry[3]})
        return light_schedule

lightService = LightService()