import RPi.GPIO as GPIO
from Components.Sensors.Sensor import Sensor

class WaterLevel(Sensor):
    def __init__(self, pin):
        super().__init__(pin)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read_value(self):
        print("Reading Water Level sensor")
        value = GPIO.input(self.pin)
        print(f"Water Level: {'Good' if value == GPIO.LOW else 'Bad'}")
        if value is not None:
            return 0 if value == GPIO.HIGH else 1
        else:
            return -1
    
waterLevel = WaterLevel(24)





