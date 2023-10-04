import Adafruit_DHT

from Components.Sensors.Sensor import Sensor

class DHT22(Sensor):
    def __init__(self, pin):
        super().__init__(pin)
        self.sensor = Adafruit_DHT.DHT22

    def read_value(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if humidity is not None and temperature is not None:
            print (f"Temp = {temperature:2.1f}ºC  Umidade = {humidity:2.1f}%")
            return temperature, humidity
        else:
            print("Failed to read DHT22 sensor")
            return -1, -1

    
dht22 = DHT22(23)
