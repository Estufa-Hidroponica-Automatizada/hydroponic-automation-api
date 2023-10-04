import RPi.GPIO as GPIO
import time

class Relay():
    def __init__(self, pin):
        self.pin = pin
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(self.pin, GPIO.OUT)
        self.state = GPIO.LOW

    def turn_on(self):
        #GPIO.output(self.pin, GPIO.HIGH)
        self.state = GPIO.HIGH

    def turn_on_for(self, seconds):
        self.turn_on()
        time.sleep(seconds)
        self.turn_off()

    def turn_off(self):
        #GPIO.output(self.pin, GPIO.LOW)
        self.state = GPIO.LOW

    def get_state(self):
        return "ON" if self.state == GPIO.HIGH else "OFF"

relays = {
    "light": Relay(7),
    "fan": Relay(8),
    "exhaustor": Relay(9),
    "pumpPhPlus": Relay(10),
    "pumpPhMinus": Relay(11),
    "pumpNutrientA": Relay(12),
    "pumpNutrientB": Relay(13),
}