import sqlite3
import os
from flask_bcrypt import Bcrypt

class DatabaseService():

    def __init__(self, database_name='database.db', schema_script='schema.sql'):
        self.database_name = database_name
        self.bcrypt = Bcrypt()

        if not os.path.exists(database_name):
            self._initialize_database(schema_script)
        
        self.conn = sqlite3.connect(database_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def _initialize_database(self, schema_script):
        open(self.database_name, 'w').close()

        with open(schema_script, 'r') as schema_file:
            schema_sql = schema_file.read()
            self.conn = sqlite3.connect(self.database_name)
            self.cursor = self.conn.cursor()
            self.cursor.executescript(schema_sql)
            hashed_password = self.bcrypt.generate_password_hash("1234").decode("utf-8")
            self.cursor.execute('INSERT INTO user (username, password) VALUES (?, ?)', ("user", hashed_password))
            self.conn.commit()

    def fetch_limits(self):
        self.cursor.execute('SELECT * FROM limit_value')
        limit = self.cursor.fetchall()
        return limit
    
    def fetch_nutrient_proportion(self):
        self.cursor.execute('SELECT * FROM nutrient_proportion')
        nutrientProportion = self.cursor.fetchone()
        return nutrientProportion

    def fetch_limit_value(self, name):
        self.cursor.execute('SELECT value FROM limit_value WHERE name = ?', (name))
        limit = self.cursor.fetchone()
        return limit
    
    def update_nutrient_proportion(self, nutrientAPorportion, nutrientBPorportion):
        self.cursor.execute('UPDATE nutrient_proportion SET nutrientA = ?, nutrientB = ?', (nutrientAPorportion, nutrientBPorportion))
        self.conn.commit()
    
    def update_limit_value(self, name, value):
        self.cursor.execute('UPDATE limit_value SET value = ? WHERE name = ?', (value, name))
        self.conn.commit()
    
    def fetch_light_schedule(self):
        self.cursor.execute('SELECT * FROM light_schedule')
        schedule = self.cursor.fetchall()
        return schedule
    
    def update_schedule(self, id, hour, minute, state):
        self.cursor.execute('UPDATE light_schedule SET hour = ?, minute = ?, state = ? WHERE id = ?', (hour, minute, state, id))
        self.conn.commit()

    def insert_schedule(self, hour, minute, state):
        self.cursor.execute('INSERT INTO light_schedule (hour, minute, state) VALUES (?, ?, ?)', (hour, minute, state))
        self.conn.commit()

    def delete_schedule(self, id):
        self.cursor.execute('DELETE FROM light_schedule WHERE id = ?', (id))
        self.conn.commit()

    def delete_all_schedule(self):
        self.cursor.execute('DELETE FROM light_schedule')
        self.conn.commit()
    
    def get_profiles(self):
        self.cursor.execute('SELECT * FROM profile')
        profiles = self.cursor.fetchall()
        return profiles

    def get_profile(self, id):
        self.cursor.execute('SELECT * FROM profile WHERE id = ?', (id,))
        profile = self.cursor.fetchone()
        return profile
    
    def get_user_info(self):
        self.cursor.execute('SELECT * FROM user')
        profile = self.cursor.fetchone()
        return {'username': profile[0], "password": profile[1]}
    
    def set_new_password(self, new_password):
        hashed_password = self.bcrypt.generate_password_hash(new_password).decode('utf-8')
        self.cursor.execute('UPDATE user SET password = ?', (hashed_password,))
        self.conn.commit()

    def post_profile(self, name, temperature_min, temperature_max, humidity_min, humidity_max, ph_min, ph_max, ec_min, ec_max, water_temperature_min, water_temperature_max, light_schedule, nutrient_proportion):
        self.cursor.execute('INSERT INTO profile (name, temperature_min, temperature_max, humidity_min, humidity_max, ph_min, ph_max, ec_min, ec_max, water_temperature_min, water_temperature_max, light_schedule, nutrient_proportion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (name, temperature_min, temperature_max, humidity_min, humidity_max, ph_min, ph_max, ec_min, ec_max, water_temperature_min, water_temperature_max, light_schedule, nutrient_proportion))
        self.conn.commit()

    def put_profile(self, id, name, temperature_min, temperature_max, humidity_min, humidity_max, ph_min, ph_max, ec_min, ec_max, water_temperature_min, water_temperature_max, light_schedule, nutrient_proportion):
        self.cursor.execute('UPDATE profile SET name = ?, temperature_min = ?, temperature_max = ?, humidity_min = ?, humidity_max = ?, ph_min = ?, ph_max = ?, ec_min = ?, ec_max = ?, water_temperature_min = ?, water_temperature_max = ?, light_schedule = ?, nutrient_proportion =? WHERE id = ?', (name, temperature_min, temperature_max, humidity_min, humidity_max, ph_min, ph_max, ec_min, ec_max, water_temperature_min, water_temperature_max, light_schedule, nutrient_proportion, id))
        self.conn.commit()

    def delete_profile(self, id):
        self.cursor.execute('DELETE FROM profile WHERE id = ?', (id,))
        self.conn.commit()

    def get_profile_actual(self):
        self.cursor.execute('SELECT * FROM profile_actual')
        profile = self.cursor.fetchone()
        return profile

    def post_profile_actual(self, id, dias=0):
        self.cursor.execute('UPDATE profile_actual SET id_selected = ?, days_passed = ?', (id, dias))
        self.conn.commit()

    def add_day_profile_actual(self):
        self.cursor.execute('UPDATE profile_actual SET days_passed = ((SELECT days_passed FROM profile_actual) + 1)')
        self.conn.commit()

    def close(self):
        self.conn.close()


databaseService = DatabaseService()