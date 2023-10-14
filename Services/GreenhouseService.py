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


        print("----------------------ATUANDO-------------------------")
        isSupposedToBeOn = lightService.isSupposedToBeOn()

        if isSupposedToBeOn:
            print("Luzes ligadas!")
            relays["light"].turn_on()
        else:
            print("Luzes desligadas!")
            relays["light"].turn_off()

        if phMeasure > -1:
            ph_min, ph_max = limitService.get_limit("ph_min")[2], limitService.get_limit("ph_max")[2]
            print(f"Limites de pH - mín: {ph_min} | máx: {ph_max}")
            if phMeasure < ph_min:
                print(f"Ph abaixo do mínimo - {phMeasure}")
                relays["pumpPhPlus"].turn_on_for(2)
            elif phMeasure > ph_max:
                print(f"Ph acima do máximo - {phMeasure}")
                relays["pumpPhMinus"].turn_on_for(2)
        else:
            print("Erro ao ler PH - Alerta!")

        if ecMeasure > -1:
            ec_min, ec_max = limitService.get_limit("ec_min")[2], limitService.get_limit("ec_max")[2]
            print(f"Limites de EC - mín: {ec_min}ppm | máx: {ec_max}ppm")
            if ecMeasure < ec_min:
                print(f"EC abaixo do mínimo - {ecMeasure}ppm")
                print(f"Ativando bomba A por {nutrientService.nutrients[0]} segundos")
                relays["pumpNutrientA"].turn_on_for(nutrientService.nutrients[0])
                print(f"Ativando bomba B por {nutrientService.nutrients[1]} segundos")
                relays["pumpNutrientB"].turn_on_for(nutrientService.nutrients[1])
            elif ecMeasure > ec_max:
                print(f"EC acima do máximo - {ecMeasure}ppm")
                pass # TODO - Alerta de troca de agua??
        else:
            print("Erro ao ler EC - Alerta!")

        if temperatureMeasure > -1:
            humidity_max, temperature_max = limitService.get_limit("humidity_max")[2], limitService.get_limit("temperature_max")[2]
            print(f"Limites máximo de temperatura e humidade - Temperatura: {temperature_max}ºC | Himidade: {humidity_max}%")
            if temperatureMeasure > temperature_max or humidityMeasure > humidity_max:
                print(f"Temperatura e/ou humidade fora da faixa - {temperatureMeasure}ºC | {humidityMeasure}%")
                relays["exhaustor"].turn_on()
                relays["fan"].turn_on()
            else:
                print(f"Desligando exaustor e ventilador - {temperatureMeasure}ºC | {humidityMeasure}%")
                relays["exhaustor"].turn_off()
                relays["fan"].turn_off()
        else:
            print("Erro ao ler temperatura - Alerta!")

        if lightMeasure < 100 and isSupposedToBeOn:
            print("Alerta - Luz está desligada indevidamente")
            pass # TODO - Lançar alerta de luz falha

        if waterLevelMeasure == 0:
            print("Alerta - Nível de água baixo")
            pass # TODO - Lançar alerta de baixo nível de agua

        print("----------------FIM MANUTENCAO------------------")
            
greenhouseService = GreenhouseService()

