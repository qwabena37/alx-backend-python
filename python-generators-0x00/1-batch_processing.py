#!/usr/bin/python3
"""
Batch processing module for fetching and processing data in batches
"""

import seed


def stream_users_in_batches(batch_size):
    """
    Generator function that fetches rows in batches from user_data table
    Args: batch_size - number of rows to fetch in each batch
    Yields: list of dictionaries containing user data for each batch
    """
    connection = seed.connect_to_prodev()
    if connection is None:
        return
    try:
        cursor = connection.cursor(dictionary=True)
        offset = 0
        while True:
            # Fetch batch with LIMIT and OFFSET
            cursor.execute(
                f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}"
            )
            batch = cursor.fetchall()
            if not batch:  # No more data
                break
            yield batch
            offset += batch_size

    except Exception as e:
        print(f"Error streaming batches: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25
    Args: batch_size - size of each batch to process
    """
    # Process each batch and filter users over 25
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)


if __name__ == "__main__":
    # Test batch processing
    batch_processing(50)
