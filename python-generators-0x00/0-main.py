from seed import connect_db, create_database, connect_to_prodev, create_table, insert_data

if __name__ == "__main__":
    # Connect to MySQL server
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()

    # Connect to the ALX_prodev database
    prodev_conn = connect_to_prodev()
    if prodev_conn:
        create_table(prodev_conn)
        insert_data(prodev_conn, "user_data.csv")   # load data from CSV
        prodev_conn.close()
