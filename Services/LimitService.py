from Services.DatabaseService import databaseService

class LimitService():
    def __init__(self):
        self.limits = databaseService.fetch_limits()

    def get_limit(self, name):
        for limit in self.limits:
            if limit[1] == name:
                return limit
    
    def set_limit(self, name, value):
        databaseService.update_limit_value(name, value)
        self.limits = databaseService.fetch_limits()
        return True

limitService = LimitService()
        
