from db_utils import create_connection, create_table
from file_utils import load_csv_to_dataframe

def main():
    
    data = load_csv_to_dataframe("data.csv")

    conn = create_connection("my_database.db")

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS employees (
        ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Age INTEGER,
        Salary REAL
    );
    """
    create_table(conn, create_table_sql)

    data.to_sql("employees", conn, if_exists="append", index=False)

    conn.close()

if __name__ == "__main__":
    main()
