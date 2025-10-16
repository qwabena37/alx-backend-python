import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else []
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # Open DB connection
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Execute query with parameters
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results  # return results to be used in 'with' block

    def __exit__(self, exc_type, exc_value, traceback):
        # Commit if no error, rollback otherwise
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()

        # Close resources
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)

    with ExecuteQuery("users.db", query, param) as results:
        for row in results:
            print(row)