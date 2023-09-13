class Relay():
    def __init__(self, pin):
        self.pin = pin

    def turn_on(self):
        pass

    def turn_on_for(self, seconds):
        pass

    def turn_off(self):
        pass

    def get_state(self):
        pass

relays = {
    "light": Relay(7),
    "fan": Relay(8),
    "exaustor": Relay(9),
    "pumpPhPlus": Relay(10),
    "pumpPhMinus": Relay(11),
    "pumpNutrientA": Relay(12),
    "pumpNutrientB": Relay(13),
}