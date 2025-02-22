import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self):
        try:
            print("Trying to make connection")
            self.connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="mansi_116",
                database="school",
                port=3306
            )
            self.cursor = self.connection.cursor()
            print("Connection Successful")
        except Error as err:
            print(f"Database Error: {err}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
            

    def add_student(self,regis_num, name, gender,dob, age, address, phone, email, standard):
        try:
            query = ("INSERT INTO student(registration_number, full_name, gender, date_of_birth, age, address, phone, email, standard) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
            self.cursor.execute(query, (regis_num, name, gender, dob, age, address, phone, email, standard))
        except mysql.connector.Error as e:
            print("Error: ", e)
            return False


    def close_connection(self):
        self.cursor.close()
        self.connection.close()