import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host='db',
        port=5432,
        database='mydatabase',
        user='myuser',
        password='mypassword'
    )
