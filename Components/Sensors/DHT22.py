import Adafruit_DHT

from Components.Sensors.Sensor import Sensor

class DHT22(Sensor):
    def __init__(self, pin):
        super().__init__(pin)
        self.sensor = Adafruit_DHT.DHT22

    def read_value(self):
        humidity, temperature = Adafruit_DHT.read(self.sensor, self.pin) # TODO - Read_retry
        if humidity is not None and temperature is not None:
            return temperature, humidity
        else:
            print("Failed to read DHT22 sensor")
            return -1, -1

    
dht22 = DHT22(1)