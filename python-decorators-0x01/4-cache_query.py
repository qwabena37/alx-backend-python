#!/usr/bin/python3
import time
import sqlite3
import functools

# Simple cache dictionary with timestamp
query_cache = {}

# Decorator to handle opening and closing DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # open connection
        try:
            result = func(conn, *args, **kwargs)  # pass conn to wrapped function
        finally:
            conn.close()  # ensure connection is always closed
        return result
    return wrapper

# Decorator to cache query results with timestamp
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            cached_result, timestamp = query_cache[query]
            print(f"[CACHE HIT] Query: {query} (cached at {time.strftime('%H:%M:%S', time.localtime(timestamp))})")
            return cached_result
        print(f"[CACHE MISS] Executing and caching query: {query}")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = (result, time.time())  # store result with timestamp
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Demonstration
if __name__ == "__main__":
    # First call will execute and cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
