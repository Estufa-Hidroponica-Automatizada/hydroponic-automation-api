from Services.DatabaseService import databaseService
from Services.LimitService import limitService
from Services.NutrientService import nutrientService
from Services.LightService import lightService
from Services.NtfyService import ntfyService
import ast


class ProfileService():
    def __init__(self):
        self.profiles = databaseService.get_profiles()
        self.current_profile = databaseService.get_current_profile()
    
    def update_profile(self, id, name, temperature_min, temperature_max, humidity_min, humidity_max, ph_min, ph_max, ec_min, ec_max, water_temperature_min, water_temperature_max, light_schedule, nutrient_proportion):
        light_schedule_list = [[[entry["hour"], entry["minute"], entry["state"]] for entry in week] for week in light_schedule]
        nutrient_proportion_list = [[entry["nutrientA"], entry["nutrientB"]] for entry in nutrient_proportion]
        databaseService.put_profile(id, name, str(temperature_min), str(temperature_max), str(humidity_min), str(humidity_max), str(ph_min), str(ph_max), str(ec_min), str(ec_max), str(water_temperature_min), str(water_temperature_max), str(light_schedule_list), str(nutrient_proportion_list))
        self.profiles = databaseService.get_profiles()
        return True
    
    def insert_profile(self, name, temperature_min, temperature_max, humidity_min, humidity_max, ph_min, ph_max, ec_min, ec_max, water_temperature_min, water_temperature_max, light_schedule, nutrient_proportion):
        light_schedule_list = [[[entry["hour"], entry["minute"], entry["state"]] for entry in week] for week in light_schedule]
        nutrient_proportion_list = [[entry["nutrientA"], entry["nutrientB"]] for entry in nutrient_proportion]
        databaseService.post_profile(name, str(temperature_min), str(temperature_max), str(humidity_min), str(humidity_max), str(ph_min), str(ph_max), str(ec_min), str(ec_max), str(water_temperature_min), str(water_temperature_max), str(light_schedule_list), str(nutrient_proportion_list))
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

    def set_current_profile(self, id, dias):
        if databaseService.get_profile(id):
            databaseService.post_current_profile(id, dias)
            self.current_profile = databaseService.get_current_profile()
            return True
        else:
            return False

    def get_current_profile(self):
        return self.current_profile
    
    def add_day(self):
        databaseService.add_day_current_profile()

    def update_limits_for_days_by_profile(self):
        current_profile = self.get_profile(self.current_profile[0])
        week = profileService.current_profile[1] // 7
        print("--------------- Atualizando limites ---------------")
        print(f"Semana: {week}")
        print(f"Perfil atual: {self.build_profile_object(current_profile)}")
        if week >= len(ast.literal_eval(current_profile[2])) and not profileService.current_profile[2]:
            print("Plantio finalizado")
            databaseService.set_current_profile_finished()
            ntfyService.send_notification("Plantio foi finalizado!", "Boas notícias!", "default", "partying_face,tada")
            return
        #setar limites
        limitService.set_limit('temperature_min', ast.literal_eval(current_profile[2])[week])
        limitService.set_limit('temperature_max', ast.literal_eval(current_profile[3])[week])
        limitService.set_limit('humidity_min', ast.literal_eval(current_profile[4])[week])
        limitService.set_limit('humidity_max', ast.literal_eval(current_profile[5])[week])
        limitService.set_limit('ph_min', ast.literal_eval(current_profile[6])[week])
        limitService.set_limit('ph_max', ast.literal_eval(current_profile[7])[week])
        limitService.set_limit('ec_min', ast.literal_eval(current_profile[8])[week])
        limitService.set_limit('ec_max', ast.literal_eval(current_profile[9])[week])
        limitService.set_limit('water_temperature_min', ast.literal_eval(current_profile[10])[week])
        limitService.set_limit('water_temperature_max', ast.literal_eval(current_profile[11])[week])
        #setar lightschedule
        lightService.delete_all_schedule()
        schedule_list = ast.literal_eval(current_profile[12])
        for alarm in schedule_list[week]:
            lightService.insert_schedule(alarm[0], alarm[1], alarm[2])
        #setar nutrient proportion
        nutrient_proportion = ast.literal_eval(current_profile[13])[week]
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
            "light_schedule":  self._from_list_to_light_schedule(ast.literal_eval(profile_list[12])),
            "nutrient_proportion":  self._from_list_to_nutrient_proportion(ast.literal_eval(profile_list[13]))
        }

    def build_current_profile_object(self, current_profile_list):
        return {
            "id": current_profile_list[0],
            "days": current_profile_list[1],
            "isFinished": current_profile_list[2]
        }
    
    def _from_list_to_light_schedule(self, input_data):
        light_schedule = []
        for week in input_data:
            week_data = [{"hour": entry[0], "minute": entry[1], "state": entry[2]} for entry in week]
            light_schedule.append(week_data)
        return light_schedule
    
    def _from_list_to_nutrient_proportion(self, input_data):
        nutrient_proportion = [{"nutrientA": entry[0], "nutrientB": entry[1]} for entry in input_data]
        return nutrient_proportion

profileService = ProfileService()
