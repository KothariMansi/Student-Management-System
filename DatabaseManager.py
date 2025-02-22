from distutils.util import execute

import mysql.connector
from mysql.connector import Error, connect


class DatabaseManager:
    def __init__(self, host, user, password, database, port=3306):
        self.db_config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
            "port": port
        }

    def execute_query(self, query, params=None):
        try:
            with mysql.connector.connect(**self.db_config) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    connection.commit()
                    print("✅ Query executed successfully.")
        except Error as e:
            print(f"❌ Error executing query: {e}")

    def fetch_query(self, query, params=None):
        try:
            with mysql.connector.connect(**self.db_config) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    return cursor.fetchall()
        except Error as e:
            print(f"Error fetching query: {e}")
            return []

    def add_student(self,regis_num, name, gender,dob, age, address, phone, email, standard):
        query = """
            INSERT INTO student(registration_number, full_name, gender, date_of_birth, age, address, phone, email, standard)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (regis_num, name, gender,dob, age, address, phone, email, standard)
        self.execute_query(query, params)