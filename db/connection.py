import mysql.connector
from mysql.connector import Error

class DBConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connected to the database")
        except Error as e:
            print(f"Error: {e}")
            self.connection = None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            print(f"Error executing query: {e}")
            raise

    def execute_update(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
        except Error as e:
            print(f"Error executing update: {e}")
            raise
    
    def execute_procedure(self, procedure_name, params):
        cursor = self.connection.cursor()
        try:
            cursor.callproc(procedure_name, params)
            self.connection.commit()
            results = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())
            return results if results else None
        except mysql.connector.Error as e:
            print(f"Error executing procedure {procedure_name}: {e}")
            raise
        finally:
            cursor.close()
