from Components.Sensors.Sensor import Sensor

class WaterTemp(Sensor):
    def read_value(self):
        print("Lendo sensor Water Temperature")
        return 22
    
waterTemp = WaterTemp(6)