from Components.Sensors.ArduinoSensor import arduinoSensor

class Light():
    def read_value(self):
        print("Reading Light sensor")
        light_value = arduinoSensor.get_data_from_arduino()[0]
        print(f"Light: {light_value}")
        return int(light_value)
    
light = Light()
