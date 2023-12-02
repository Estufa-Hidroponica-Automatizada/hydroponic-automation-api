# hydroponic-automation-api
Repositório da API feita com Flask para monitoramento e controle do sistema de cultivo hidropônico automatizado utilizando Raspberry Pi.\
Este projeto foi desenvolvido como Trabalho de Conclusão de Curso do curso de Engenharia de Computação na Escola Politécnica da Universidade de São Paulo pelos alunos:

- Brian Andrade Nunes
- Marco Aurélio Condé Oliveira Prado
- Silas Lima e Silva

## Configuração do sistema

1. Conecte os pinos conforme tabelas abaixo:

| Sensor                              | Conexão           |
|-------------------------------------|-------------------|
| pH (PH4502C)                        | Arduino Analog 0  |
| Luminosidade (LDR)                  | Arduino Analog 2  |
| Condutividade (TDS)                 | Arduino Analog 3  |
| Temperatura d'água (DS18B20)        | Arduino Digital 2 |
| Temperatura do ar e umidade (DHT22) | Arduino Digital 3 |
| Nível d'água                        | Raspberry GPIO 24 |


| Actuator          | Connection        |
|-------------------|-------------------|
| Bomba pH+         | Raspberry GPIO 5  |
| Bomba pH-         | Raspberry GPIO 6  |
| Bomba Nutriente B | Raspberry GPIO 16 |
| Painel de Luz     | Raspberry GPIO 17 |
| Exaustor          | Raspberry GPIO 22 |
| Bomba Nutriente A | Raspberry GPIO 26 |
| Ventilador        | Raspberry GPIO 27 |

2. Carregue e execute o arquivo ```arduino_estufa.ino``` no seu Arduino.
3. Conecte o Arduino e a Webcam nas portas USB do Raspberry.

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
