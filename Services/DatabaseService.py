import sqlite3
import os

class DatabaseService():

    def __init__(self, database_name='database.db', schema_script='schema.sql'):
        self.database_name = database_name

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
            self.conn.commit()

    def fetch_limits(self):
        self.cursor.execute('SELECT * FROM limit_value')
        limit = self.cursor.fetchall()
        return limit

    def fetch_limit_value(self, name):
        self.cursor.execute('SELECT value FROM limit_value WHERE name = ?', (name))
        limit = self.cursor.fetchone()
        return limit
    
    def update_limit_value(self, name, value):
        self.cursor.execute('UPDATE limit_value SET value = ? WHERE name = ?', (value, name))
        self.conn.commit()
    
    def fetch_light_schedule(self):
        self.cursor.execute('SELECT * FROM light_schedule')
        schedule = self.cursor.fetchall()
        return schedule
    
    def update_schedule(self, id, hour, minute, state):
        self.cursor.execute('UPDATE light_schedule SET hour = ?, minute = ?, state, = ? WHERE id = ?', (hour, minute, state, id))
        self.conn.commit()

    def insert_schedule(self, hour, minute, state):
        self.cursor.execute('INSERT INTO light_schedule (hour, minute, state) VALUES (?, ?, ?)', (hour, minute, state))
        self.conn.commit()

    def delete_schedule(self, id):
        self.cursor.execute('DELETE FROM light_schedule WHERE id = ?', (id))
        self.conn.commit()

    def close(self):
        self.conn.close()

databaseService = DatabaseService()