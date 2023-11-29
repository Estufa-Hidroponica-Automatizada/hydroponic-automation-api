from Components.Sensors.ArduinoSensor import arduinoSensor

class DHT22():
    def read_value(self):
        try:
            print("Reading DHT sensor")
            values = arduinoSensor.get_data_from_arduino()
            temperature, humidity = values[4], values[5]
            print(f"Temp: {temperature}ºC| Humidity: {humidity}%")
            return float(temperature), float(humidity)
        except Exception as e:
            print(f"Failed to read DHT: {e}")
            return -1, -1

    
dht22 = DHT22()
