from app import db

class LimitValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __init__(self, name, value):
        self.name = name
        self.value = value