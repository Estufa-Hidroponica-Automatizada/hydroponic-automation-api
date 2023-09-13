from Components.Sensors.Sensor import Sensor

class DHT22(Sensor):
    def read_value(self):
        print("Lendo sensor DHT22")
        return 27, 64
    
dht22 = DHT22(1)