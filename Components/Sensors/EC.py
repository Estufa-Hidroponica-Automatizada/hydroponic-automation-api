from Components.Sensors.ArduinoSensor import arduinoSensor

class EC():
    def read_value(self):
        print("Reading EC sensor")
        ec = arduinoSensor.get_data_from_arduino()[3]
        print(f"EC: {ec}")
        return int(ec)
    
ec = EC()