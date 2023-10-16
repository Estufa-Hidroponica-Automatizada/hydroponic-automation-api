import io
from flask import Flask, jsonify, make_response, request, send_file
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from Components.Sensors.DHT22 import dht22
from Components.Sensors.EC import ec
from Components.Sensors.Light import light
from Components.Sensors.PH import ph
from Components.Sensors.WaterLevel import waterLevel
from Components.Sensors.WaterTemp import waterTemp
from Components.Actuators.Relay import relays

from Services.LightService import lightService
from Services.NutrientService import nutrientService
from Services.LimitService import limitService
from Services.GreenhouseService import greenhouseService
from Services.WebcamService import webcamService
from Services.ProfileService import profileService
from Services.DatabaseService import databaseService

from flask_apscheduler import APScheduler
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, unset_jwt_cookies

app = Flask(__name__)
CORS(app,supports_credentials=True)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

app.config['JWT_SECRET_KEY'] = 'seu_segredo_super_secreto'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False 

@app.route('/actuator', methods=['GET']) # Retorna todos os estados dos atuadores
#@jwt_required()
def get_actuators():
    return jsonify({
        "light": relays["light"].get_state(),
        "fan": relays["fan"].get_state(),
        "exhaustor": relays["exhaustor"].get_state(),
        "pumpPhPlus": relays["pumpPhPlus"].get_state(),
        "pumpPhMinus": relays["pumpPhMinus"].get_state(),
        "pumpNutrientA": relays["pumpNutrientA"].get_state(),
        "pumpNutrientB": relays["pumpNutrientB"].get_state()
    }), 200

@app.route('/actuator/<value>/<action>', methods=['POST']) # Retorna todos os estados dos atuadores
#@jwt_required()
def set_actuators(value, action):
    if value not in relays.keys():
        return jsonify({ "result": False, "message": "Atuador fornecido não é válido." }), 400
    if action == "on":
        relays[value].turn_on()
    elif action == "off":
        relays[value].turn_off()
    else:
        return jsonify({ "result": False, "message": "Ação fornecida é inválida. Ações disponíveis: on/off" }), 400
    return jsonify({ "result": True }), 200

@app.route('/actuator/<value>/on_for/<seconds>', methods=['POST']) # Retorna todos os estados dos atuadores
#@jwt_required()
def set_actuators_for(value, seconds):
    if not seconds.isnumeric():
        return jsonify({ "result": False, "message": "Segundos fornecidos não é um valor válido" }), 400
    if value not in relays.keys():
        return jsonify({ "result": False, "message": "Atuador fornecido não é válido." }), 400
    relays[value].turn_on_for(int(seconds))
    return jsonify({ "result": True }), 200


@app.route('/sensor', methods=['GET']) # Retorna todos os valores medidos nos sensores
#@jwt_required()
def read_sensors():
    temp, humidity = dht22.read_value()
    return jsonify({
        "airTemperature": temp,
        "humidity": humidity,
        "waterTemperature": waterTemp.read_value(),
        "pH": ph.read_value(),
        "condutivity": ec.read_value(),
        "waterLevel": waterLevel.read_value(),
        "light": light.read_value()
    }), 200

@app.route('/sensor/<sensor>', methods=['GET']) # Retorna o valor medido no sensor passado
#@jwt_required()
def read_sensor(sensor):
    if sensor == "air-temperature":
        return jsonify({"value": dht22.read_value()[0]}), 200
    elif sensor == "humidity":
        return jsonify({"value": dht22.read_value()[1]}), 200
    elif sensor == "condutivity":
        return jsonify({"value": ec.read_value()}), 200
    elif sensor == "ph":
        return jsonify({"value": ph.read_value()}), 200
    elif sensor == "light":
        return jsonify({"value": light.read_value()}), 200
    elif sensor == "water-level":
        return jsonify({"value": waterLevel.read_value()}), 200
    elif sensor == "water-temperature":
        return jsonify({"value": waterTemp.read_value()}), 200
    return jsonify({'success': False, 'message': 'Invalid sensor'}), 400

@app.route('/limit', methods=['GET']) # Retorna a lista de limites
#@jwt_required()
def get_limits():
    data = {
        "airTemperature": {'max': limitService.get_limit("temperature_max")[2], 'min': limitService.get_limit("temperature_min")[2]},
        "waterTemperature": {'max': limitService.get_limit("water_temperature_max")[2], 'min': limitService.get_limit("water_temperature_min")[2]},
        "humidity": {'max': limitService.get_limit("humidity_max")[2], 'min': limitService.get_limit("humidity_min")[2]},
        "pH": {'max': limitService.get_limit("ph_max")[2], 'min': limitService.get_limit("ph_min")[2]},
        "condutivity": {'max': limitService.get_limit("ec_max")[2], 'min': limitService.get_limit("ec_min")[2]}
    }
    return jsonify(data), 200

@app.route('/limit/<value>', methods=['GET', 'PUT']) # Retorna o valor do limite passado | Seta valor do limite passado
#@jwt_required()
def get_limit(value):
    if request.method == 'GET':
        if value == "air-temperature":
            return jsonify({'max': limitService.get_limit("temperature_max")[2], 'min': limitService.get_limit("temperature_min")[2]}), 200
        elif value == "humidity":
            return jsonify({'max': limitService.get_limit("humidity_max")[2], 'min': limitService.get_limit("humidity_min")[2]}), 200
        elif value == "condutivity":
            return jsonify({'max': limitService.get_limit("ec_max")[2], 'min': limitService.get_limit("ec_min")[2]}), 200
        elif value == "ph":
            return jsonify({'max': limitService.get_limit("ph_max")[2], 'min': limitService.get_limit("ph_min")[2]}), 200
        elif value == "water-temperature":
            return jsonify({'max': limitService.get_limit("water_temperature_max")[2], 'min': limitService.get_limit("water_temperature_min")[2]}), 200
        return jsonify({'success': False, 'message': "Invalid sensor"}), 400
    elif request.method == 'PUT':
        data = request.get_json()
        try:
            limitService.set_limit(value+"_min", data["min"])
            limitService.set_limit(value+"_max", data["max"])
            return jsonify({'success': True}), 200
        except:
            return jsonify({'success': False, 'message': 'Invalid data'}), 400
    

@app.route('/light/schedule', methods=['GET', 'POST']) # Altera horario existente | Adiciona horario novo
#@jwt_required()
def light_schedule():
    if request.method == 'GET':
        return jsonify(lightService.schedule)
    elif request.method == 'POST':
        data = request.get_json()
        lightService.insert_schedule(data['hour'], data['minute'], data['state'])
        return jsonify({"result": True}), 200
    
@app.route('/light/schedule/<id>', methods=['PUT', 'DELETE']) # pega horario existente | deleta horario existente
#@jwt_required()
def light_schedule_id(id):
    if request.method == 'PUT':
        data = request.get_json()
        lightService.update_schedule(id, data['hour'], data['minute'], data['state'])
        return jsonify({"result": True}), 200
    elif request.method == 'DELETE':
        lightService.delete_schedule(id)
        return jsonify({"result": True}), 200
    
@app.route('/nutrient/proportion', methods=['GET', 'PUT']) # Pega e actualiza porporção de nutrientes
#@jwt_required()
def func_nutrients():
    if request.method == 'GET':
        return jsonify(nutrientService.nutrients)
    elif request.method == 'PUT':
        data = request.get_json()
        nutrientService.set_proportion(data['nutrientA'], data['nutrientB'])
        return jsonify({"result": True}), 200

@app.route('/cam/<action>', methods=['GET']) # retorna foto/stream/timelapse da estufa
#@jwt_required()
def cam_endpoint(action):
    if action == 'photo':
        photo_bytes = webcamService.get_save_photo()
        if not photo_bytes: return jsonify({"result": False}), 500
        return send_file(io.BytesIO(photo_bytes),
                         mimetype='image/jpeg',
                         as_attachment=True,
                         download_name='photo.jpg')

    elif action == 'timelapse':
        video_bytes = webcamService.get_timelapse()
        return send_file(io.BytesIO(video_bytes),
                         mimetype='video/mp4',
                         as_attachment=True,
                         download_name='timelapse.mp4')

    else:
        return jsonify({"result": False, 'message': "Invalid action. Use 'photo' or 'timelapse'"}), 400

@app.route('/change-password', methods=['POST']) # muda senha
#@jwt_required()
def changePassword():
    data = request.get_json()
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')
    user_data = databaseService.get_user_info()
    if bcrypt.check_password_hash(user_data['password'], old_password):
        databaseService.set_new_password(new_password)
        return jsonify({"result": True}), 200
    else:
        return jsonify({"result": False, 'message': 'Invalid wrong password'}), 401


@app.route('/login', methods=['POST']) # faz login
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user_data = databaseService.get_user_info()

    if username == user_data['username'] and bcrypt.check_password_hash(user_data['password'], password):
        access_token = create_access_token(user_data['username'])
        resp = make_response(jsonify({'success': True}))
        unset_jwt_cookies(resp)
        resp.set_cookie('access_token_cookie', access_token, httponly=True, secure=True, samesite='None')
        return resp, 200
    else:
        return jsonify({'success': False, "message": "Incorret data"}), 401

@app.route('/logout', methods=['POST']) # faz logout
#@jwt_required()
def logout():
    resp = make_response(jsonify({'success': True}))
    unset_jwt_cookies(resp)
    return resp, 200

@app.route('/profile', methods=['GET', 'POST'])
#@jwt_required()
def get_profiles():
    if request.method == 'GET':
        profiles = []
        for profile in profileService.profiles:
            profiles.append(profileService.build_profile_object(profile))
        return jsonify(profiles), 200
    elif request.method == 'POST':
        data = request.get_json()
        profileService.insert_profile(data['name'], data['temperature_min'], data['temperature_max'], data['humidity_min'], data['humidity_max'], data['ph_min'], data['ph_max'], data['ec_min'], data['ec_max'], data['water_temperature_min'], data['water_temperature_max'], data['light_schedule'], data['nutrient_proportion'])
        return jsonify({"result": True}), 200

@app.route('/profile/<id>', methods=['GET', 'DELETE', 'PUT'])
#@jwt_required()
def action_profile(id):
    if request.method == 'PUT':
        data = request.get_json()
        profileService.update_profile(id, data['name'], data['temperature_min'], data['temperature_max'], data['humidity_min'], data['humidity_max'], data['ph_min'], data['ph_max'], data['ec_min'], data['ec_max'], data['water_temperature_min'], data['water_temperature_max'], data['light_schedule'], data['nutrient_proportion'])
        profileService.update_limits_for_days_by_profile()
        return jsonify({"result": True}), 200
    elif request.method == 'DELETE':
        profileService.delete_profile(id)
        return jsonify({"result": True}), 200
    elif request.method == 'GET':
        return jsonify(profileService.build_profile_object(profileService.get_profile(id))), 200

@app.route('/profile/actual', methods=['GET', 'POST'])
#@jwt_required()
def ongoing_profile():
    if request.method == 'POST':
        data = request.get_json()
        profileService.set_profile_actual(data['id'], data['days'])
        if data.get('erase', False):
            webcamService.delete_photos()
        profileService.update_limits_for_days_by_profile()
        return jsonify({"result": True}), 200
    elif request.method == 'GET':
        return jsonify(profileService.build_profile_actual_object(profileService.profile_actual)), 200

@scheduler.task('interval', id='monitoring', seconds=600)
def maintain_greenhouse():
    greenhouseService.maintaince()

@scheduler.task('interval', id='updating', seconds=3600) # 86400 1 vez ao dia
def daily_update():
    webcamService.get_save_photo()
    profileService.add_day()
    profileService.update_limits_for_days_by_profile()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='3000')
