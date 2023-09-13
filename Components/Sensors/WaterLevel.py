from Components.Sensors.Sensor import Sensor

class WaterLevel(Sensor):
    def read_value(self):
        print("Lendo sensor Water Level")
        return 1
    
waterLevel = WaterLevel(5)