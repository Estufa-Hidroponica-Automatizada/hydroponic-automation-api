# hydroponic-automation-api
Repositório da API feita com Flask para monitoramento e controle do sistema de cultivo hidropônico automatizado utilizando Raspberry Pi.\
Este projeto foi desenvolvido como Trabalho de Conclusão de Curso do curso de Engenharia de Computação na Escola Politécnica da Universidade de São Paulo pelos alunos:

- Brian Andrade Nunes
- Marco Aurélio Condé Oliveira Prado
- Silas Lima e Silva

## Configuração do sistema

1. Conecte os pinos conforme tabelas abaixo:

| Sensor                              | Conexão           |
|:-----------------------------------:|:-----------------:|
| pH (PH4502C)                        | Arduino Analog 0  |
| Luminosidade (LDR)                  | Arduino Analog 2  |
| Condutividade (TDS)                 | Arduino Analog 3  |
| Temperatura d'água (DS18B20)        | Arduino Digital 2 |
| Temperatura do ar e umidade (DHT22) | Arduino Digital 3 |
| Nível d'água                        | Raspberry GPIO 24 |


| Atuador           | Conexão           |
|:-----------------:|:-----------------:|
| Bomba pH+         | Raspberry GPIO 5  |
| Bomba pH-         | Raspberry GPIO 6  |
| Bomba Nutriente B | Raspberry GPIO 16 |
| Painel de Luz     | Raspberry GPIO 17 |
| Exaustor          | Raspberry GPIO 22 |
| Bomba Nutriente A | Raspberry GPIO 26 |
| Ventilador        | Raspberry GPIO 27 |

2. Carregue e execute o arquivo ```arduino_estufa.ino``` no seu Arduino.
3. Conecte o Arduino e a Webcam nas portas USB do Raspberry.

## Scripts
### Dependências do projeto
Antes de seguir para os próximos scripts, você primeiro deve instalar todas as dependências do projeto executando o seguinte comando:
```
pip install -r requirements.txt
```

### Modo desenvolvedor
Para rodar a API no modo desenvolvedor, basta executar o seguinte comando:
```
python app.py
```
Como alternativa, você pode definir a variável de ambiente do Flask da seguinte forma:
```
export FLASK_APP=app.py
```
Ao fazer isso, você poderá rodar (em modo desenvolvedor) com o comando:
```
flask run
```

### Deploy
Você precisará dos arquivos `server.crt` e `server.key` na raiz do seu projeto caso queira hostear um servidor HTTPS válido. Neste caso, basta descomentar as seguintes linhas no arquivo `gunicorn_config.py`:
```
keyfile = '/home/rasp/hydroponic-automation-api/server.key'
certfile = '/home/rasp/hydroponic-automation-api/server.crt' 
```
Neste arquivo, também constam as demais configurações do servidor, que incluem IP, porta e número de workers. Após alterar as configurações (caso necessário), basta executar o seguinte comando para realizar o deploy no servidor local:
```
gunicorn -c gunicorn_config.py app:app
```

> **Lembrete**: Isso só irá rodar o servidor localmente, permitindo o acesso pela rede local. Se você deseja acessar remotamente, configure adequadamente o redirecionamento de portas no seu roteador.

## Testes locais
Para testar todos os endpoints implementados neste projeto pelo _Postman_, basta importar o arquivo `ApiEstufa.postman_collection.json`.
