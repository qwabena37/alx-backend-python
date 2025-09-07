#!/usr/bin/python3
"""
Database seeding module for ALX_prodev MySQL database
"""

import mysql.connector
import csv
import uuid
import os
from mysql.connector import Error

DEFAULT_DB_USER = "root"
DEFAULT_DB_PASSWORD = ""


def connect_db():
    """
    Connects to the MySQL database server
    Returns: database connection object or None
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=DEFAULT_DB_USER,
            password=DEFAULT_DB_PASSWORD
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist
    Args: connection - MySQL connection object
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
        print("Database ALX_prodev created or already exists")
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL
    Returns: database connection object or None
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=DEFAULT_DB_USER,
            password=DEFAULT_DB_PASSWORD,
            database="ALX_prodev"
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None


def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields
    Args: connection - MySQL connection object to ALX_prodev
    """
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age INT NOT NULL
        ) ENGINE=InnoDB
        """
        cursor.execute(create_table_query)
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """
    Inserts data from CSV file into the database if it does not exist
    Args: 
        connection - MySQL connection object
        csv_file - path to CSV file containing user data
    """
    cursor = None
    try:
        cursor = connection.cursor()

        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]

        if count > 0:
            print("Data already exists in user_data table")
            return

        # Resolve CSV path relative to this script if needed
        if not os.path.isabs(csv_file):
            base_dir = os.path.dirname(__file__)
            csv_file = os.path.join(base_dir, csv_file)

        # Read CSV and insert data
        with open(csv_file, "r", newline="", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            insert_query = """
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            """

            for row in csv_reader:
                # Generate UUID for user_id
                user_id = str(uuid.uuid4())
                name = (row.get("name") or "").strip()
                email = (row.get("email") or "").strip()

                age_val = row.get("age", "") or ""
                try:
                    # handle numeric values that may be floats in CSV
                    age = int(float(age_val)) if age_val != "" else 0
                except (ValueError, TypeError):
                    age = 0

                cursor.execute(insert_query, (user_id, name, email, age))

        connection.commit()
        print(f"Data inserted successfully from {csv_file}")

    except FileNotFoundError:
        print(f"CSV file {csv_file} not found")
    except Error as e:
        print(f"Error inserting data: {e}")
        if connection:
            connection.rollback()
    except Exception as e:
        print(f"Unexpected error: {e}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()


if __name__ == "__main__":
    # Test the functions
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

        prodev_conn = connect_to_prodev()
        if prodev_conn:
            create_table(prodev_conn)
            insert_data(prodev_conn, "user_data.csv")
            prodev_conn.close()