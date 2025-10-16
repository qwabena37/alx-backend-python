import time
import sqlite3
import functools


# Decorator to handle opening and closing DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db") # Open connection
        
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper  

# Decorator to retry function on failure
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e 
                    print(f"[Retry {attempt}/{retries}] Failed with error: {e}")
                    if attempt < retries:
                        time.sleep(delay)
                # raise the last exception if all retries failed
            raise last_exception
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Attempt to fetch users with automatic retry on failure
if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)                