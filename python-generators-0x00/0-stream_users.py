#!/usr/bin/python3
"""
Generator function to stream rows from SQL database one by one
"""

import seed


def stream_users():
    """
    Generator function that streams rows from user_data table one by one
    Yields: dictionary containing user data for each row
    """
    connection = seed.connect_to_prodev()
    if connection is None:
        return
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        # Fetch all results first to avoid unread result error
        results = cursor.fetchall()
        # Use generator to yield one row at a time
        for row in results:
            yield row
    except Exception as e:
        print(f"Error streaming users: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    # Test the generator
    for user in stream_users():
        print(user)
        break  # Just print first user for testing
