from serial import Serial

class ArduinoSensor():
    def __init__(self, sensor_folder):
        self.ser = Serial(sensor_folder, 9600)

    def get_data_from_arduino(self):
        data = None
        tries = 0
        data_return = -1, -1, -1
        while tries < 5:
            tries += 1
            data = self.ser.readline().decode().strip()  # Lê uma linha da porta serial
            if data:
                data_return = data.split(',')
                if len(data_return) == 4:
                    return data_return
        return data_return
    
arduinoSensor = ArduinoSensor('/dev/ttyACM0')
