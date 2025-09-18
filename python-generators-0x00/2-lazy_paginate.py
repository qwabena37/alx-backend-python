#!/usr/bin/python3
"""
Lazy pagination module for fetching paginated data using generators
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetches a specific page of users from the database
    Args:
        page_size - number of users per page
        offset - starting position for the page
    Returns: list of user dictionaries for the requested page
    """
    connection = seed.connect_to_prodev()
    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"Error paginating users: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def lazy_pagination(page_size):
    """
    Generator function that implements lazy loading of paginated data
    Args: page_size - number of records per page
    Yields: list of user dictionaries for each page
    """
    offset = 0

    while True:
        # Fetch the next page
        page = paginate_users(page_size, offset)

        if not page:  # No more data
            break

        yield page
        offset += page_size


if __name__ == "__main__":
    # Test lazy pagination
    for page_num, page in enumerate(lazy_pagination(100), 1):
        print(f"Page {page_num}:")
        for user in page[:3]:  # Show first 3 users of each page
            print(user)
        if page_num >= 2:  # Just show first 2 pages for testing
            break
