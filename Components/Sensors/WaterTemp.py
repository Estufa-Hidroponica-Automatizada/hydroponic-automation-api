
from Components.Sensors.Sensor import Sensor
from ds18b20 import DS18B20

class WaterTemp(Sensor):
    def __init__(self, sensor_id):
        super().__init__(sensor_id)
        # Create an instance of W1ThermSensor for DS18B20 sensor
        # self.sensor = DS18B20(sensor_id)

    def read_value(self):
        print("Reading DS18B20 Water Temperature sensor")
        # Read the temperature value in Celsius
        temperature = 22 #self.sensor.get_temperature()
        return temperature
    
waterTemp = WaterTemp("sensor_id_tem_q_achar")