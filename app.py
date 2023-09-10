from flask import Flask, jsonify, request
from Components.Actuators.Relay import Relay
from Components.Sensors.DHT22 import DHT22
from Components.Sensors.EC import EC
from Components.Sensors.Light import Light
from Components.Sensors.PH import PH
from Components.Sensors.WaterLevel import WaterLevel
from Components.Sensors.WaterTemp import WaterTemp
from Services.AirControlService import AirControlService

from Services.DatabaseService import DatabaseService
from Services.LightService import LightService
from Services.LimitService import LimitService
from Services.WaterService import WaterService

from flask_apscheduler import APScheduler


app = Flask(__name__)
scheduler = APScheduler()

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
limitService = LimitService(databaseService)
airControlService = AirControlService(dht22, relays, databaseService, limitService)
waterService = WaterService(ec, ph, waterLevel, waterTemp, relays, databaseService, limitService)
lightService = LightService(light, relays, databaseService)

@app.route('/sensor', methods=['GET']) # Retorna todos os valores medidos nos sensores
def read_sensors():
    return 'Hello, World!'

@app.route('/sensor/<sensor>', methods=['GET']) # Retorna o valor medido no sensor passado
def read_sensor(sensor):
    return 'Hello, World!'

@app.route('/sensor/<sensor>/history', methods=['GET']) # Retorna o histórico dos valores do sensor passado
def read_sensor_history(sensor):
    data = {'message': 'This is sample data from the API.'}
    return jsonify(data)

@app.route('/limit', methods=['GET']) # Retorna a lista de limites
def get_limits():
    return jsonify(limitService.limits), 200

@app.route('/limit/<value>', methods=['GET', 'POST']) # Retorna o valor do limite passado | Seta valor do limite passado, como receber body?
def get_limit(value):
    if request.method == 'GET':
        return jsonify({'value': limitService.get_limit(value)})
    elif request.method == 'POST':
        data = request.get_json()
        if data:
            limitService.set_limit(data["name"], data["value"])
            return jsonify({"result": True}), 200
        else:
            return jsonify({'error': 'Invalid JSON data'}), 400

@app.route('/light/schedule', methods=['GET', 'PUT', 'POST', 'DELETE']) # Altera horario existente | Adiciona horario novo
def light_schedule():
    if request.method == 'GET':
        return jsonify(lightService.schedule)
    elif request.method == 'PUT':
        data = request.get_json()
        lightService.update_schedule(data['id'], data['hour'], data['minute'], data['state'])
        return jsonify({True}), 200
    elif request.method == 'POST':
        data = request.get_json()
        lightService.insert_schedule(data['hour'], data['minute'], data['state'])
        return jsonify({True}), 200
    
@app.route('/light/schedule/<id>', methods=['GET', 'DELETE']) # pega horario existente | deleta horario existente
def light_schedule_id(id):
    if request.method == 'GET':
        return jsonify(lightService.schedule), 200 # como pega pelo id
    elif request.method == 'DELETE':
        lightService.delete_schedule(id)
        return jsonify({True}), 200

@app.route('/actuator/relay/<name>', methods=['POST']) # Liga ou desliga relay passado
def set_limit(name):
    data = {'message': 'This is sample data from the API.'}
    return jsonify(data)

@app.route('/cam/<action>', methods=['GET']) # retorna foto/stream/timelapse da estufa
def cam_endpoint(action):
    data = {'message': 'This is sample data from the API.'}
    return jsonify(data)

@app.route('/login', methods=['POST']) # faz login
def login():
    data = {'message': 'This is sample data from the API.'}
    return jsonify(data)

@scheduler.task('interval', id='monitoring', seconds=10)
def maintain_greenhouse():
    # Ler todos os sensores
    # Aplicar todos os atuadores necessários
    print('This job is executed every 10 seconds.')

@app.teardown_appcontext
def cleanup_app_context(exception=None):
    databaseService.close()

if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=True, host='0.0.0.0')