"""
2-lazy_paginate.py
Implements lazy pagination using a generator
"""
import seed

def paginate_users(page_size, offset):
    """
    Fetch one page of users starting from offset
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily loads pages of users.
    Yields one page (list of users) at a time.
    """
    offset = 0
    while True:  # single loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size