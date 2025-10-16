"""
1-batch_processing.py
Generator functions for batch processing user_data from MySQL
"""
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator that yields users in batches from the user_data table.
    Each yield returns a list (batch) of rows.
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
        
        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []
                
        if batch:
            yield batch
        
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error: {e}")
        return

def batch_processing(batch_size):
    """
    Process batches and filter users over the age of 25.
    Prints each user in that condition.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)                

