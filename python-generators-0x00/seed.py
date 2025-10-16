"""
seed.py
Setup MySQL database ALX_prodev with table user_data,
and populate from user_data.csv
"""
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import csv
import uuid

# Load environment variables
load_dotenv()

def connect_db():
    """Connects to MySQL server (without specifying database)."""
    try:
        connection = mysql.connector.connect(
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            host = os.getenv("DB_HOST")
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    return None 

def create_database(connection):
    """Creates database ALX_prodev if not exists."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;") 
        cursor.close()
        print("Database created successful.")
    except Error as e:
        print(f"Error creating database: {e}")
        
def connect_to_prodev():
    """Connects directly to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            database="ALX_prodev",
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            host = os.getenv("DB_HOST")
        )                  
        if connection.is_connected():
            print(f"Connection successful: {connection.database}")
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
    return None 


def create_table(connection):
    """Creates user_data table if it does not exist.""" 
    try:
        cursor = connection.cursor()
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data(
                    user_id CHAR(36) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    age DECIMAL NOT NULL,
                    INDEX (user_id)
                );                           
        """)     
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}") 

def insert_data(connection, csv_file): 
    """Insert data into user_data table from CSV if not already present."""
    try:
        cursor = connection.cursor()
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # generate UUID for each user if not provided
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = int(row["age"])
                
                # check if email already exists
                cursor.execute("SELECT user_id FROM user_data WHERE email = %s", (email,))
                result = cursor.fetchone()
                if not result:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (user_id, name, email, age)
                    ) 
        connection.commit()
        cursor.close()
        print("Data inserted successful.")
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"CSV file {csv_file} not found.")
                              


if __name__ == "__main__":
    # Connect to MySQL server
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()

    # Connect to the ALX_prodev database
    prodev_conn = connect_to_prodev()
    if prodev_conn:
        create_table(prodev_conn)
        insert_data(prodev_conn, "user_data.csv")
        prodev_conn.close()
           