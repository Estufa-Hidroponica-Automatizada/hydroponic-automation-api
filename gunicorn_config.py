# gunicorn_config.py
bind = '0.0.0.0:4000'
workers = 1

keyfile = '/home/rasp/Documents/hydroponic-automation-api/server.key'
certfile = '/home/rasp/Documents/hydroponic-automation-api/server.crt' 