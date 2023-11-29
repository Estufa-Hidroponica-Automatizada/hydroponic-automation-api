from Components.Sensors.ArduinoSensor import arduinoSensor

class PH():
    def read_value(self):
        print("Reading PH sensor")
        ph = arduinoSensor.get_data_from_arduino()[3]
        print(f"PH: {ph}")
        return float(ph)
    
ph = PH()