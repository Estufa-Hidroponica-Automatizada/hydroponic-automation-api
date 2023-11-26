import datetime
import time
import Adafruit_DHT

from Components.Sensors.Sensor import Sensor

class DHT22(Sensor):
    def __init__(self, pin):
        super().__init__(pin)
        self.sensor = Adafruit_DHT.DHT22
        time.sleep(2)
        self.last_read = datetime.datetime.now()
        self.humidity, self.temperature = Adafruit_DHT.read(self.sensor, self.pin)

    def read_value(self):
        try:
            print(datetime.datetime.now() - self.last_read)
            if datetime.datetime.now() - self.last_read < datetime.timedelta(seconds=90):
                print(f"Returnig last DHT22's data read: Temperature: {self.temperature:2.1f}ºC | Humidity: {self.humidity:2.1f}%")
                return round(self.temperature, 2), round(self.humidity, 2)
            print("Reading DHT22 sensor")
            self.last_read = datetime.datetime.now()
            self.humidity, self.temperature = Adafruit_DHT.read(self.sensor, self.pin)
            if self.humidity is not None and self.temperature is not None:
                print (f"Temperature: {self.temperature:2.1f}ºC | Humidity: {self.humidity:2.1f}%")
                return round(self.temperature, 2), round(self.humidity, 2)
            else:
                print("Failed to read DHT22 sensor")
                return -1, -1
        except:
            print("Failed to read DHT22 sensor")
            self.humidity, self.temperature = -1, -1
            return -1, -1

    
dht22 = DHT22(23)
