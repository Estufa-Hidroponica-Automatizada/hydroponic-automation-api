from Components.Sensors.Sensor import Sensor

class PH(Sensor):
    def read_value(self):
        print("Lendo sensor PH")
        return 7.5

ph = PH(4)