from Services.DatabaseService import DatabaseService


class LimitService():
    def __init__(self, database: DatabaseService):
        self.limits = database.fetch_limits()

    def get_limit(self, name):
        return self.limits[name]
    
    def set_limit(self, name, value):
        self.database.update_limit_value()
        self.limits[name] = value
        return True
        
