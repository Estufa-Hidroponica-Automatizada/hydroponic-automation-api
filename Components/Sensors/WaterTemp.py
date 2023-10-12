from Components.Sensors.ArduinoSensor import arduinoSensor

class WaterTemp():
    def read_value(self):
        print("Reading Water Temperature sensor")
        waterTemperature = arduinoSensor.get_data_from_arduino()[1]
        print(f"Water Temperature: {waterTemperature}")
        return round(float(waterTemperature), 2)
    
waterTemp = WaterTemp()