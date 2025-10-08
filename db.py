import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dima1337",
        database = "banquet_hall",
        charset = 'utf8mb4',
        use_unicode = True
    )