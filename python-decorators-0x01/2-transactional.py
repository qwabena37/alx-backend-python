import sqlite3
import functools

# Decorator to handle opening and closing DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db") # Open connection
        
        try:
            result = func(conn, *args, **kwargs) # Pass conn to the wrapped function
        finally:
            conn.close() # Ensure conn is always closed
        return result
    return wrapper 

# Decorator to handle transactions
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit() # Commit if successful
            return result
        except Exception as e:
            pass 
    return wrapper 

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ?", (new_email, user_id))
    
# Update user's email with automatic transaction handling
if __name__ == '__main__':
   user_email = update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
   print(user_email)                  