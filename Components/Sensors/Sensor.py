class Sensor(): # Abstract - DO NOT instantiate
    def __init__(self, pin):
        self.pin = pin

    def read_value(self):
        print("Not defined!")
        return -1