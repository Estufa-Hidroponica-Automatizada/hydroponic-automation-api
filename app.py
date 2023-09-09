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

@app.route('/sensor', methods=['GET'])
def read_sensors():
    return 'Hello, World!'

@app.route('/sensor/<sensor>', methods=['GET'])
def read_sensor(sensor):
    return 'Hello, World!'

@app.route('/sensor/<sensor>/history', methods=['GET'])
def read_sensor_history(sensor):
    data = {'message': 'This is sample data from the API.'}
    return jsonify(data)

@app.route('/limit', methods=['GET'])
def get_limits():
    data = {'message': 'This is sample data from the API.'}
    return jsonify(data)

@app.route('/limit/<value>', methods=['GET'])
def get_limit(value):
    data = {'message': 'This is sample data from the API.'}
    return jsonify(data)

@app.route('/limit/<value>', methods=['POST'])
def set_limit(value):
    data = {'message': 'This is sample data from the API.'}
    return jsonify(data)

@app.route('/light/schedule', methods=['GET'])
def get_limit():
    data = {'message': 'This is sample data from the API.'}
    return jsonify(data)

@app.route('/light/schedule', methods=['POST'])
def set_limit():
    data = {'message': 'This is sample data from the API.'}
    return jsonify(data)

@app.teardown_appcontext
def cleanup_app_context(exception=None):
    databaseService.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')