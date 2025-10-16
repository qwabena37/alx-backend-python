#!/usr/bin/python3
"""
4-stream_ages.py
Memory-efficient aggregation using generators
"""

import seed


def stream_user_ages():
    """
    Generator that yields user ages one by one
    from the user_data table.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data;")

    for row in cursor:  # loop 1
        yield row["age"]

    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Calculate average age of users without loading all data into memory.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():  # loop 2
        total_age += age
        count += 1

    average_age = total_age / count if count > 0 else 0
    print(f"Average age of users: {average_age:.2f}")


if __name__ == "__main__":
    calculate_average_age()
