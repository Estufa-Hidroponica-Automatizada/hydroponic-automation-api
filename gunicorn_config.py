# gunicorn_config.py
bind = '0.0.0.0:4000'
workers = 1

keyfile = '/home/rasp/hydroponic-automation-api/server.key'
certfile = '/home/rasp/hydroponic-automation-api/server.crt' 
