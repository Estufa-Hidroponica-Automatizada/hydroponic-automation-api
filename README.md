# hydroponic-automation-api
Respository for the Flask API behind an autonomous hydroponic plantantion made with Raspberry Pi

# First steps

1. Set all pins correctly:

| Sensor            | Connection             |
|-------------------|------------------------|
| DHT22             | Arduino Digital 3      |
| TDS               | Arduino Analog 3       |
| Light             | Arduino Analog 2       |
| pH                | Arduino Analog 0       |
| Water Level       | Raspberry GPIO 24      |
| Water Temperature | Arduino Digital 2      |


| Actuator          | Connection             |
|-------------------|------------------------|
| Nutrient Pump A   | Raspberry GPIO 26      |
| Nutrient Pump B   | Raspberry GPIO 16      |
| Pump pH-          | Raspberry GPIO 6       |
| Pump pH+          | Raspberry GPIO 5       |
| Fan               | Raspberry GPIO 27      |
| Exhaustor         | Raspberry GPIO 22      |
| Light             | Raspberry GPIO 17      |

2. Run ```arduino_estufa.ino``` into your Arduino.
3. Connect Arduino and your Webcam into Raspberry's USB ports.


# How to run for development

First, install all dependecies using:

```
pip install -r requirements.txt
```

then you can use:

```
python app.py
```

Alternatively, you can define the Flask's enviroment variable using:

```
export FLASK_APP=app.py
```

And finally:

```
flask run
```

## Local Testing

Import ```ApiEstufa.postman_collection.json``` into Postman all endpoints on your service can be tested directly.

# How to deploy on local server

You need a ```server.crt``` and a ```server.key``` files in root to host a valid HTTPS server, if that's what you want you need to remove the commenting following code from ```gunicorn_config.py```:

```
keyfile = '/home/rasp/hydroponic-automation-api/server.key'
certfile = '/home/rasp/hydroponic-automation-api/server.crt' 
```


Everything else is configured in ```gunicorn_config.py```: ip, port and number of workers, you can change the default configuration there, then you can run:

```
gunicorn -c gunicorn_config.py app:app
```

And everything should be up and running.

> **Remember**: this only runs the server locally, you may access it from local network, if you need to access it remotely make sure to make the adequate port-forwarding in your router, and fixing the working machine ip.
