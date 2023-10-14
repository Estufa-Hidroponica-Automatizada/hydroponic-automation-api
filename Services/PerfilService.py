from Services.DatabaseService import databaseService
from Services.LimitService import limitService
from Services.NutrientService import nutrientService
from Services.LightService import lightService
import ast


class PerfilService():
    def __init__(self):
        self.perfils = databaseService.get_perfils()
        self.perfil_atual = databaseService.get_perfil_atual()
    
    def update_perfil(self, id, name, temperature_min, temperature_max, humidity_min, humidity_max, ph_min, ph_max, ec_min, ec_max, water_temperature_min, water_temperature_max, light_schedule, nutrient_proportion):
        databaseService.put_perfil(id, name, str(temperature_min), str(temperature_max), str(humidity_min), str(humidity_max), str(ph_min), str(ph_max), str(ec_min), str(ec_max), str(water_temperature_min), str(water_temperature_max), str(light_schedule), str(nutrient_proportion))
        self.perfils = databaseService.get_perfils()
        return True
    
    def insert_perfil(self, name, temperature_min, temperature_max, humidity_min, humidity_max, ph_min, ph_max, ec_min, ec_max, water_temperature_min, water_temperature_max, light_schedule, nutrient_proportion):
        databaseService.post_perfil(name, str(temperature_min), str(temperature_max), str(humidity_min), str(humidity_max), str(ph_min), str(ph_max), str(ec_min), str(ec_max), str(water_temperature_min), str(water_temperature_max), str(light_schedule), str(nutrient_proportion))
        self.perfils = databaseService.get_perfils()
        return True
    
    def delete_perfil(self, id):
        databaseService.delete_perfil(id)
        self.perfils = databaseService.get_perfils()
        return True
    
    def get_perfils(self):
        return self.perfils
    
    def get_perfil(self, id):
        return databaseService.get_perfil(id)

    def set_perfil_atual(self, id, dias):
        if databaseService.get_perfil(id):
            databaseService.post_perfil_atual(id, dias)
            self.perfil_atual = databaseService.get_perfil_atual()
            return True
        else:
            return False

    def get_perfil_atual(self):
        return self.perfil_atual
    
    def add_day(self):
        databaseService.add_day_perfil_atual()

    def update_limits_for_days_by_perfil(self):
        perfil_atual = self.get_perfil(self.perfil_atual[0])
        week = perfilService.perfil_atual[1] // 7
        print("--------------- Atualizando limites ---------------")
        print(f"Semana: {week}")
        print(f"Perfil atual: {self.build_perfil_object(perfil_atual)}")
        if week >= len(ast.literal_eval(perfil_atual[2])):
            print("Plantio finalizado - Alerta!")
            return
        #setar limites
        limitService.set_limit('temperature_min', ast.literal_eval(perfil_atual[2])[week])
        limitService.set_limit('temperature_max', ast.literal_eval(perfil_atual[3])[week])
        limitService.set_limit('humidity_min', ast.literal_eval(perfil_atual[4])[week])
        limitService.set_limit('humidity_max', ast.literal_eval(perfil_atual[5])[week])
        limitService.set_limit('ph_min', ast.literal_eval(perfil_atual[6])[week])
        limitService.set_limit('ph_max', ast.literal_eval(perfil_atual[7])[week])
        limitService.set_limit('ec_min', ast.literal_eval(perfil_atual[8])[week])
        limitService.set_limit('ec_max', ast.literal_eval(perfil_atual[9])[week])
        limitService.set_limit('water_temperature_min', ast.literal_eval(perfil_atual[10])[week])
        limitService.set_limit('water_temperature_max', ast.literal_eval(perfil_atual[11])[week])
        #setar lightschedule
        lightService.delete_all_schedule()
        schedule_list = ast.literal_eval(perfil_atual[12])
        for alarm in schedule_list[week]:
            lightService.insert_schedule(alarm[0], alarm[1], alarm[2])
        #setar nutrient proportion
        nutrient_proportion = ast.literal_eval(perfil_atual[13])[week]
        nutrientService.set_proportion(nutrient_proportion[0],nutrient_proportion[1])
        print("--------------- Fim atualização de limites ---------------")

    def build_perfil_object(self, perfil_list):
        return {
            "id": perfil_list[0],
            "name": perfil_list[1],
            "temperature_min":  ast.literal_eval(perfil_list[2]),
            "temperature_max":  ast.literal_eval(perfil_list[3]),
            "humidity_min":  ast.literal_eval(perfil_list[4]),
            "humidity_max":  ast.literal_eval(perfil_list[5]),
            "ph_min":  ast.literal_eval(perfil_list[6]),
            "ph_max":  ast.literal_eval(perfil_list[7]),
            "ec_min":  ast.literal_eval(perfil_list[8]),
            "ec_max":  ast.literal_eval(perfil_list[9]),
            "water_temperature_min":  ast.literal_eval(perfil_list[10]),
            "water_temperature_max":  ast.literal_eval(perfil_list[11]),
            "light_schedule":  ast.literal_eval(perfil_list[12]),
            "nutrient_proportion":  ast.literal_eval(perfil_list[13])
        }

    def build_perfil_atual_object(self, perfil_atual_list):
        return {
            "id": perfil_atual_list[0],
            "days": perfil_atual_list[1]
        }

perfilService = PerfilService()
