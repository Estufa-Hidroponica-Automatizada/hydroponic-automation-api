import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)

class Relay():
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = True

    def turn_on_for(self, seconds):
        self.turn_on()
        time.sleep(seconds)
        self.turn_off()

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False

    def get_state(self):
        return self.state

relays = {
    "light": Relay(17),
    "fan": Relay(27),
    "exhaustor": Relay(22),
    "pumpPhPlus": Relay(5),
    "pumpPhMinus": Relay(6),
    "pumpNutrientA": Relay(26),
    "pumpNutrientB": Relay(16),
}
