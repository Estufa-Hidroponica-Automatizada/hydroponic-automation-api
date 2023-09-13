from flask import Flask, jsonify, request
from Components.Sensors.DHT22 import dht22
from Components.Sensors.EC import ec
from Components.Sensors.Light import light
from Components.Sensors.PH import ph
from Components.Sensors.WaterLevel import waterLevel
from Components.Sensors.WaterTemp import waterTemp

from Services.DatabaseService import databaseService
from Services.LightService import lightService
from Services.NutrientService import nutrientService
from Services.LimitService import limitService
from Services.GreenhouseService import greenhouseService

from flask_apscheduler import APScheduler


app = Flask(__name__)
scheduler = APScheduler()

@app.route('/sensor', methods=['GET']) # Retorna todos os valores medidos nos sensores
def read_sensors():
    temp, humidity = dht22.read_value()
    return jsonify({
        "airTemperature": temp,
        "humidity": humidity,
        "waterTemperature": waterTemp.read_value(),
        "pH": ph.read_value(),
        "EC": ec.read_value(),
        "waterLevel": waterLevel.read_value(),
        "light": light.read_value()
    }), 200

@app.route('/sensor/<sensor>', methods=['GET']) # Retorna o valor medido no sensor passado
def read_sensor(sensor):
    if sensor == "air-temperature":
        return jsonify({"value": dht22.read_value()[0]}), 200
    elif sensor == "humidity":
        return jsonify({"value": dht22.read_value()[1]}), 200
    elif sensor == "ec":
        return jsonify({"value": ec.read_value()}), 200
    elif sensor == "ph":
        return jsonify({"value": ph.read_value()}), 200
    elif sensor == "light":
        return jsonify({"value": light.read_value()}), 200
    elif sensor == "water-level":
        return jsonify({"value": waterLevel.read_value()}), 200
    elif sensor == "water-temperature":
        return jsonify({"value": waterTemp.read_value()}), 200
    return jsonify({'error': 'Invalid sensor'}), 400

@app.route('/limit', methods=['GET']) # Retorna a lista de limites
def get_limits():
    return jsonify(limitService.limits), 200

@app.route('/limit/<value>', methods=['GET', 'PUT']) # Retorna o valor do limite passado | Seta valor do limite passado
def get_limit(value):
    if request.method == 'GET':
        return jsonify({'value': limitService.get_limit(value)})
    elif request.method == 'PUT':
        data = request.get_json()
        if data:
            limitService.set_limit(value, data["value"])
            return jsonify({"result": True}), 200
        else:
            return jsonify({'error': 'Invalid JSON data'}), 400

@app.route('/light/schedule', methods=['GET', 'POST']) # Altera horario existente | Adiciona horario novo
def light_schedule():
    if request.method == 'GET':
        return jsonify(lightService.schedule)
    elif request.method == 'POST':
        data = request.get_json()
        lightService.insert_schedule(data['hour'], data['minute'], data['state'])
        return jsonify({"result": True}), 200
    
@app.route('/light/schedule/<id>', methods=['PUT', 'DELETE']) # pega horario existente | deleta horario existente
def light_schedule_id(id):
    if request.method == 'PUT':
        data = request.get_json()
        lightService.update_schedule(id, data['hour'], data['minute'], data['state'])
        return jsonify({"result": True}), 200
    elif request.method == 'DELETE':
        lightService.delete_schedule(id)
        return jsonify({"result": True}), 200
    
@app.route('/nutrient/proportion', methods=['GET', 'PUT']) # Pega e atualiza porporção de nutrientes
def func_nutrients():
    if request.method == 'GET':
        return jsonify(nutrientService.nutrients)
    elif request.method == 'PUT':
        data = request.get_json()
        nutrientService.set_proportion(data['nutrientA'], data['nutrientB'])
        return jsonify({"result": True}), 200

@app.route('/cam/<action>', methods=['GET']) # retorna foto/stream/timelapse da estufa
def cam_endpoint(action):
    data = {'message': 'This is sample data from the API.'}
    return jsonify(data)

@app.route('/change-password', methods=['POST']) # muda senha
def changePassword():
    data = {'message': 'This is sample data from the API.'}
    return jsonify(data)

@app.route('/login', methods=['POST']) # faz login
def login():
    data = {'message': 'This is sample data from the API.'}
    return jsonify(data)

@app.route('/logout', methods=['POST']) # faz logout
def logout():
    data = {'message': 'This is sample data from the API.'}
    return jsonify(data)

@scheduler.task('interval', id='monitoring', seconds=120)
def maintain_greenhouse():
    greenhouseService.maintaince()

if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=True, host='0.0.0.0', port='5000')