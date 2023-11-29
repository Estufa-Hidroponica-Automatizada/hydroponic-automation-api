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

# How to deploy on local server

All is configured in ```gunicorn_config.py```: ip, port and number of workers, you can change the default configuration there, then you can run:

```
gunicorn -c gunicorn_config.py app:app
```

And everything should be up and running.

> **Remember**: this only runs the server locally, you may access it from local network, if you need to access it remotely make sure to make the adequate port-forwarding in your router, and fixing the working machine ip.
