import time
from serial import Serial

class ArduinoSensor():
    def __init__(self, sensor_folder):
        self.ser = Serial(sensor_folder, 9600)

    def get_data_from_arduino(self):
        try:
            self.ser.write('R'.encode())

            data = None
            tries = 0
            data_return = -1, -1, -1, -1, -1, -1
            while tries < 5:
                time.sleep(1)
                tries += 1
                data = self.ser.readline().decode().strip()  # Lê uma linha da porta serial
                print(f"Data received: {data}")
                if data:
                    data_return = data.split(',')
                    if len(data_return) == 6:
                        return data_return
            print("Falha ao ler Arduino após 5 tentativas.")
            return data_return
        except:
            print("Erro ao ler/escrever na porta serial do Arduino")
            return -1, -1, -1, -1, -1, -1
    
arduinoSensor = ArduinoSensor('/dev/ttyACM0')