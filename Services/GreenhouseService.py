from Components.Sensors.DHT22 import dht22
from Components.Sensors.EC import ec
from Components.Sensors.Light import light
from Components.Sensors.PH import ph
from Components.Sensors.WaterLevel import waterLevel
from Components.Actuators.Relay import relays

from Services.LightService import lightService
from Services.LimitService import limitService
from Services.NutrientService import nutrientService
from Services.NtfyService import ntfyService

class GreenhouseService():
    def maintaince(self):
        print("----------------INICIANDO MANUTENCAO------------------")
        print("-----------------------LENDO--------------------------")
        temperatureMeasure, humidityMeasure = dht22.read_value()
        lightMeasure = light.read_value()
        waterLevelMeasure = waterLevel.read_value()


        print("----------------------ATUANDO-------------------------")
        ecMeasure = ec.read_value()
        if ecMeasure > -1:
            ec_min, ec_max = limitService.get_limit("ec_min")[2], limitService.get_limit("ec_max")[2]
            print(f"Limites de EC - mín: {ec_min}ppm | máx: {ec_max}ppm")
            if ecMeasure < ec_min:
                time_multiplier = ((ec_min - ecMeasure) / 65) # 1 seg para cada 65ppm a menos
                time_nutrient_A = nutrientService.nutrients[0] * time_multiplier
                time_nutrient_B = nutrientService.nutrients[1] * time_multiplier
                print(f"EC abaixo do mínimo por {(ec_min - ecMeasure)}ppm")
                print(f"Fator de multiplicação: {time_multiplier}")
                print(f"Ativando bomba A por {time_nutrient_A} segundos")
                relays["pumpNutrientA"].turn_on_for(time_nutrient_A)
                print(f"Ativando bomba B por {time_nutrient_B} segundos")
                relays["pumpNutrientB"].turn_on_for(time_nutrient_B)
            elif ecMeasure > ec_max:
                print(f"EC acima do máximo por {(ecMeasure - ec_max)}ppm")
                ntfyService.send_notification(f"A condutividade da água está acima do limite, considere trocar a água! - Limite: {ec_max}ppm | Medido: {ecMeasure}ppm", "Alerta - Limites excedidos!", "high", "warning")
        else:
            ntfyService.send_notification("Ocorreu um erro ao ler a EC da água!", "Alerta - Sensor com defeito!", "max", "rotating_light")

        phMeasure = ph.read_value()
        if phMeasure > -1:
            ph_min, ph_max = limitService.get_limit("ph_min")[2], limitService.get_limit("ph_max")[2]
            print(f"Limites de pH - mín: {ph_min} | máx: {ph_max}")
            if phMeasure < ph_min:
                time_to_apply = ((ph_min - phMeasure) / 0.25) # 1 seg para cada 0.25 a menos
                print(f"Ph abaixo do mínimo por {(ph_min - phMeasure)}")
                print(f"Ativando bomba de pH+ por {time_to_apply} segundos")
                relays["pumpPhPlus"].turn_on_for(time_to_apply)
            elif phMeasure > ph_max:
                time_to_apply = ((phMeasure - ph_max) / 0.25) # 1 seg para cada 0.25 a mais
                print(f"Ph acima do máximo por {(phMeasure - ph_max) }")
                print(f"Ativando bomba de pH- por {time_to_apply} segundos")
                relays["pumpPhMinus"].turn_on_for(time_to_apply)
        else:
            ntfyService.send_notification("Ocorreu um erro ao ler o pH da água!", "Alerta - Sensor com defeito!", "max", "rotating_light")

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
            ntfyService.send_notification("Ocorreu um erro ao ler a temperatura/humidade do ambiente!", "Alerta - Sensor com defeito!", "max", "rotating_light")

        isSupposedToBeOn = lightService.isSupposedToBeOn()

        if isSupposedToBeOn:
            print("Luzes ligadas!")
            relays["light"].turn_on()
        else:
            print("Luzes desligadas!")
            relays["light"].turn_off()

        if lightMeasure < 100 and isSupposedToBeOn:
            print("Alerta - Luz está desligada indevidamente")
            ntfyService.send_notification("A luz está apagada e deveria estar acesa!", "Alerta - Luz com defeito!", "max", "rotating_light")

        if not waterLevelMeasure:
            print("Alerta - Nível de água baixo")
            ntfyService.send_notification("O nível da água esta baixo!", "Alerta - Nível de água", "high", "warning")

        print("----------------FIM MANUTENCAO------------------")
            
greenhouseService = GreenhouseService()

