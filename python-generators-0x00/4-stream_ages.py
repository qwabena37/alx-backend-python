#!/usr/bin/python3
"""
Memory-efficient aggregation module for calculating average age using generators
"""

import seed


def stream_user_ages():
    """
    Generator function that yields user ages one by one
    Yields: integer age of each user
    """
    connection = seed.connect_to_prodev()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        
        # Use generator to yield one age at a time
        for row in cursor:
            yield row[0]  # row[0] contains the age value
            
    except Exception as e:
        print(f"Error streaming ages: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def calculate_average_age():
    """
    Calculates the average age using the generator without loading 
    the entire dataset into memory
    Returns: average age as float
    """
    total_age = 0
    count = 0
    
    # Use the generator to process ages one by one
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        return 0
    
    return total_age / count


if __name__ == "__main__":
    # Calculate and print average age
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age:.2f}")
    