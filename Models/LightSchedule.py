from app import db

class LightSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hour = db.Column(db.Integer, nullable=False)
    minute = db.Column(db.Integer, nullable=False)
    state = db.Column(db.Boolean, nullable=False)

    def __init__(self, hour, minute, state):
        self.hour = hour
        self.minute = minute
        self.state = state