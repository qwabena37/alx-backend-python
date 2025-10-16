"""
0-stream_users.py
Generator that streams rows from the user_data table one by one
"""
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load environment variables
load_dotenv()

def stream_users():
    """
    Generator function that connects to the ALX_prodev database
    and yields rows from user_data table one by one.
    """
    try:
        connection = mysql.connector.connect(
            database="ALX_prodev",
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            host = os.getenv("DB_HOST")
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        
        for row in cursor:
            yield row
        
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error: {e}")
        return        