# hydroponic-automation-api
Respository for the Flask API behind an autonomous hydroponic plantantion made with Raspberry Pi

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

# How to connect each sensor

> **IMPORTANT**: Make sure every pin in Raspberry and code are defined correctly! Wrong setup may cause damage to your sensors or even to the Raspberry

### DHT22

### EC

### pH

### Light

### Water Level

### Water Temperature