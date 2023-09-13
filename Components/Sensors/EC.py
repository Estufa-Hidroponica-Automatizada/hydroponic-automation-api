from Components.Sensors.Sensor import Sensor

class EC(Sensor):
    def read_value(self):
        print("Lendo sensor EC")
        return 400
    
ec = EC(2)