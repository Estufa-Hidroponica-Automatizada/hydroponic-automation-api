import sqlite3
import os

class DatabaseService():

    def __init__(self, database_name='database.db', schema_script='schema.sql'):
        self.database_name = database_name

        if not os.path.exists(database_name):
            self._initialize_database(schema_script)
        
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def _initialize_database(self, schema_script):
        open(self.database_name, 'w').close()

        with open(schema_script, 'r') as schema_file:
            schema_sql = schema_file.read()
            self.conn = sqlite3.connect(self.database_name)
            self.cursor = self.conn.cursor()
            self.cursor.executescript(schema_sql)
            self.conn.commit()

    def fetch_limit_value(self, name):
        self.cursor.execute('SELECT value FROM limit_value WHERE name = ?', (name))
        limit = self.cursor.fetchone()
        return limit
    
    def fetch_light_schedule(self):
        self.cursor.execute('SELECT hour, minute, state FROM light_schedule')
        schedule = self.cursor.fetchall()
        return schedule

    # def add_user(self, username, email):
    #     self.cursor.execute('INSERT INTO users (username, email) VALUES (?, ?)', (username, email))
    #     self.conn.commit()

    # def update_user(self, user_id, username, email):
    #     self.cursor.execute('UPDATE users SET username = ?, email = ? WHERE id = ?', (username, email, user_id))
    #     self.conn.commit()

    # def delete_user(self, user_id):
    #     self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    #     self.conn.commit()

    def close(self):
        self.conn.close()
