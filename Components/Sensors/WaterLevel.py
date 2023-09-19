from gpiozero import DigitalInputDevice
from Components.Sensors.Sensor import Sensor

class WaterLevel(Sensor):
    def __init__(self, pin):
        super().__init__(pin)
        # Create an instance of DigitalInputDevice to read the binary signal
        self.sensor = DigitalInputDevice(self.pin)

    def read_value(self):
        print("Reading Water Level sensor")
        # Read the binary signal (1 for good level, 0 for low level)
        value = self.sensor.value
        return value
    
waterLevel = WaterLevel(5)