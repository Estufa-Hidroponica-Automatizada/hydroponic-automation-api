from Components.Sensors.DHT22 import dht22
from Components.Sensors.EC import ec
from Components.Sensors.Light import light
from Components.Sensors.PH import ph
from Components.Sensors.WaterLevel import waterLevel
from Components.Actuators.Relay import relays

from Services.LightService import lightService
from Services.LimitService import limitService
from Services.NutrientService import nutrientService

class GreenhouseService():
    def maintaince(self):
        print("----------------INICIANDO MANUTENCAO------------------")
        print("-----------------------LENDO--------------------------")
        temperatureMeasure, humidityMeasure = dht22.read_value()
        lightMeasure = light.read_value()
        waterLevelMeasure = waterLevel.read_value()
        phMeasure = ph.read_value()
        ecMeasure = ec.read_value()
        print("Valores medidos:")
        print(f"Air temperature: {temperatureMeasure}ºC")
        print(f"Humidity: {humidityMeasure}%")
        print(f"Light: {lightMeasure}")
        print(f"Water Level: {waterLevelMeasure}")
        print(f"pH: {phMeasure}")
        print(f"EC: {ecMeasure}")


        print("----------------------ATUANDO-------------------------")
        isSupposedToBeOn = lightService.isSupposedToBeOn()

        if isSupposedToBeOn:
            print("Ligando a luz")
            relays["light"].turn_on()
        else:
            print("Desligando a luz")
            relays["light"].turn_off()

        if phMeasure > -1:
            if phMeasure < limitService.get_limit("ph_min")[2]:
                print(f"Ph abaixo do mínimo - {phMeasure}")
                relays["pumpPhPlus"].turn_on_for(2)
            elif phMeasure > limitService.get_limit("ph_max")[2]:
                print(f"Ph acima do máximo - {phMeasure}")
                relays["pumpPhMinus"].turn_on_for(2)

        if ecMeasure > -1:
            if ecMeasure < limitService.get_limit("ec_min")[2]:
                print(f"EC abaixo do mínimo - {ecMeasure}ppm")
                print(f"Ativando bomba A por {nutrientService.nutrients[0]} segundos")
                relays["pumpNutrientA"].turn_on_for(nutrientService.nutrients[0])
                print(f"Ativando bomba B por {nutrientService.nutrients[1]} segundos")
                relays["pumpNutrientB"].turn_on_for(nutrientService.nutrients[1])
            elif ecMeasure > limitService.get_limit("ec_max")[2]:
                print(f"EC acima do máximo - {ecMeasure}ppm")
                pass # TODO - Alerta de troca de agua??

        if temperatureMeasure > -1:
            if temperatureMeasure > limitService.get_limit("temperature_max")[2] or humidityMeasure > limitService.get_limit("humidity_max")[2]:
                print(f"Temperatura e/ou humidade fora da faixa - {temperatureMeasure}ºC | {humidityMeasure}%")
                relays["exhaustor"].turn_on()
                relays["fan"].turn_on()
            else:
                print(f"Desligando exaustor e ventilador - {temperatureMeasure}ºC | {humidityMeasure}%")
                relays["exhaustor"].turn_off()
                relays["fan"].turn_off()

        if light.read_value() == 0 and isSupposedToBeOn:
            print("Alerta - Luz está desligada indevidamente")
            pass # TODO - Lançar alerta de luz falha

        if waterLevelMeasure == 0:
            print("Alerta - Nível de água baixo")
            pass # TODO - Lançar alerta de baixo nível de agua

        print("----------------FIM MANUTENCAO------------------")
            
greenhouseService = GreenhouseService()

