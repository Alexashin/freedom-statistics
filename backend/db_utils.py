import sqlite3

def create_connection(db_file):
  
    return sqlite3.connect(db_file)

def create_table(conn, create_table_sql):

    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()
