import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    
    def __enter__(self):
        # Open the connection and create a cursor
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, traceback):
        # Commit changes if no exception, otherwise rollback
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        # Close connection
        self.cursor.close()
        self.conn.close() 

if __name__ == '__main__':
    with DatabaseConnection("user.db") as cursor:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            print(row)                    