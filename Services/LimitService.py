from Services.DatabaseService import DatabaseService


class LimitService():
    def __init__(self, database: DatabaseService):
        self.limits = database.fetch_limits()

    def get_limit(self, name):
        for limit in self.limits:
            if limit[1] == name:
                return limit
    
    def set_limit(self, name, value):
        self.database.update_limit_value(name, value)
        self.limits = self.database.fetch_limits()
        return True
        
