import Adafruit_DHT

from Components.Sensors.Sensor import Sensor

class DHT22(Sensor):
    def __init__(self, pin):
        super().__init__(pin)
        self.sensor = Adafruit_DHT.DHT22

    def read_value(self):
        print("Reading DHT22 sensor")
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if humidity is not None and temperature is not None:
            print (f"Temperature: {temperature:2.1f}ºC | Humidity: {humidity:2.1f}%")
            return round(temperature, 2), round(humidity, 2)
        else:
            print("Failed to read DHT22 sensor")
            return -1, -1

    
dht22 = DHT22(23)
