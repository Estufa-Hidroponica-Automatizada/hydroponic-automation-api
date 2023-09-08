from flask import Flask, jsonify
from Components.Actuators.Relay import Relay
from Components.Sensors.DHT22 import DHT22
from Components.Sensors.EC import EC
from Components.Sensors.Light import Light
from Components.Sensors.PH import PH
from Components.Sensors.WaterLevel import WaterLevel
from Components.Sensors.WaterTemp import WaterTemp
from Services.AirControlService import AirControlService

from Services.DatabaseService import DatabaseService
from Services.LightControlService import LightControlService
from Services.WaterControlService import WaterControlService

app = Flask(__name__)
dht22 = DHT22(1)
ec = EC(2)
light = Light(3)
ph = PH(4)
waterLevel = WaterLevel(5)
waterTemp = WaterTemp(6)
relays = {
    "light": Relay(7),
    "fan": Relay(8),
    "exaustor": Relay(9),
    "pumpPhPlus": Relay(10),
    "pumpPhMinus": Relay(11),
    "pumpNutrientA": Relay(12),
    "pumpNutrientB": Relay(13),
}
databaseService = DatabaseService()
airControlService = AirControlService(dht22, relays, databaseService)
waterControlService = WaterControlService(ec, ph, waterLevel, waterTemp, relays, databaseService)
lightControlService = LightControlService(light, relays, databaseService)

#ENDPOINTS
# - Get todos os valores
# - Get valores com historico
# - Get limites - (db)
# - Set limites (valores devem ser armazenados em banco para não perde-los)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/data')
def get_data():
    data = {'message': 'This is sample data from the API.'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)