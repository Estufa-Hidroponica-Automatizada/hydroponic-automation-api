from Services.DatabaseService import databaseService
from Services.LimitService import limitService
from Services.NutrientService import nutrientService
from Services.LightService import lightService
from Services.NtfyService import ntfyService
import ast


class ProfileService():
    def __init__(self):
        self.profiles = databaseService.get_profiles()
        self.profile_actual = databaseService.get_profile_actual()
    
    def update_profile(self, id, name, temperature_min, temperature_max, humidity_min, humidity_max, ph_min, ph_max, ec_min, ec_max, water_temperature_min, water_temperature_max, light_schedule, nutrient_proportion):
        databaseService.put_profile(id, name, str(temperature_min), str(temperature_max), str(humidity_min), str(humidity_max), str(ph_min), str(ph_max), str(ec_min), str(ec_max), str(water_temperature_min), str(water_temperature_max), str(light_schedule), str(nutrient_proportion))
        self.profiles = databaseService.get_profiles()
        return True
    
    def insert_profile(self, name, temperature_min, temperature_max, humidity_min, humidity_max, ph_min, ph_max, ec_min, ec_max, water_temperature_min, water_temperature_max, light_schedule, nutrient_proportion):
        databaseService.post_profile(name, str(temperature_min), str(temperature_max), str(humidity_min), str(humidity_max), str(ph_min), str(ph_max), str(ec_min), str(ec_max), str(water_temperature_min), str(water_temperature_max), str(light_schedule), str(nutrient_proportion))
        self.profiles = databaseService.get_profiles()
        return True
    
    def delete_profile(self, id):
        databaseService.delete_profile(id)
        self.profiles = databaseService.get_profiles()
        return True
    
    def get_profiles(self):
        return self.profiles
    
    def get_profile(self, id):
        return databaseService.get_profile(id)

    def set_profile_actual(self, id, dias):
        if databaseService.get_profile(id):
            databaseService.post_profile_actual(id, dias)
            self.profile_actual = databaseService.get_profile_actual()
            return True
        else:
            return False

    def get_profile_actual(self):
        return self.profile_actual
    
    def add_day(self):
        databaseService.add_day_profile_actual()

    def update_limits_for_days_by_profile(self):
        profile_actual = self.get_profile(self.profile_actual[0])
        week = profileService.profile_actual[1] // 7
        print("--------------- actualizando limites ---------------")
        print(f"Semana: {week}")
        print(f"Profile actual: {self.build_profile_object(profile_actual)}")
        if week >= len(ast.literal_eval(profile_actual[2])):
            print("Plantio finalizado")
            ntfyService.send_notification("Plantio foi finalizado!", "Boas notícias!", "default", "partying_face,tada")
            return
        #setar limites
        limitService.set_limit('temperature_min', ast.literal_eval(profile_actual[2])[week])
        limitService.set_limit('temperature_max', ast.literal_eval(profile_actual[3])[week])
        limitService.set_limit('humidity_min', ast.literal_eval(profile_actual[4])[week])
        limitService.set_limit('humidity_max', ast.literal_eval(profile_actual[5])[week])
        limitService.set_limit('ph_min', ast.literal_eval(profile_actual[6])[week])
        limitService.set_limit('ph_max', ast.literal_eval(profile_actual[7])[week])
        limitService.set_limit('ec_min', ast.literal_eval(profile_actual[8])[week])
        limitService.set_limit('ec_max', ast.literal_eval(profile_actual[9])[week])
        limitService.set_limit('water_temperature_min', ast.literal_eval(profile_actual[10])[week])
        limitService.set_limit('water_temperature_max', ast.literal_eval(profile_actual[11])[week])
        #setar lightschedule
        lightService.delete_all_schedule()
        schedule_list = ast.literal_eval(profile_actual[12])
        for alarm in schedule_list[week]:
            lightService.insert_schedule(alarm[0], alarm[1], alarm[2])
        #setar nutrient proportion
        nutrient_proportion = ast.literal_eval(profile_actual[13])[week]
        nutrientService.set_proportion(nutrient_proportion[0],nutrient_proportion[1])
        print("--------------- Fim atualização de limites ---------------")

    def build_profile_object(self, profile_list):
        return {
            "id": profile_list[0],
            "name": profile_list[1],
            "temperature_min":  ast.literal_eval(profile_list[2]),
            "temperature_max":  ast.literal_eval(profile_list[3]),
            "humidity_min":  ast.literal_eval(profile_list[4]),
            "humidity_max":  ast.literal_eval(profile_list[5]),
            "ph_min":  ast.literal_eval(profile_list[6]),
            "ph_max":  ast.literal_eval(profile_list[7]),
            "ec_min":  ast.literal_eval(profile_list[8]),
            "ec_max":  ast.literal_eval(profile_list[9]),
            "water_temperature_min":  ast.literal_eval(profile_list[10]),
            "water_temperature_max":  ast.literal_eval(profile_list[11]),
            "light_schedule":  ast.literal_eval(profile_list[12]),
            "nutrient_proportion":  ast.literal_eval(profile_list[13])
        }

    def build_profile_actual_object(self, profile_actual_list):
        return {
            "id": profile_actual_list[0],
            "days": profile_actual_list[1]
        }

profileService = ProfileService()
