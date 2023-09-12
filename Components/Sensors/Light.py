from Components.Sensors.Sensor import Sensor

class Light(Sensor):
    def read_value(self):
        print("Lendo sensor Light")
        return 1