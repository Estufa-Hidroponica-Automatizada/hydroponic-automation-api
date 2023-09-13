from Services.DatabaseService import databaseService

class NutrientService():
    def __init__(self):
        self.nutrients = databaseService.fetch_nutrient_proportion()

    def get_proportion(self):
        return self.nutrients[0], self.nutrients[1]
    
    def set_proportion(self, nutrientAProportion, nutrientBProportion):
        databaseService.update_nutrient_proportion(nutrientAProportion, nutrientBProportion)
        self.nutrients = databaseService.fetch_nutrient_proportion()
        return True

nutrientService = NutrientService()
        
