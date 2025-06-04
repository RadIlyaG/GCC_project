import sqlite3
import os
import datetime
import collections


class SqliteDB:
    def __init__(self):
        #qsfc_dir = os.path.dirname(os.path.abspath(__file__))
        #self.db = os.path.join(db_path, db_name)
        #print(f"[DEBUG] Using DB file: {self.db}")

        # self.db = 'db.db'
        #self.db = os.path.join(os.path.dirname(__file__), '..', 'db.db')
        #self.db = os.path.abspath(self.db)
        #print(f"[DEBUG] Using DB file: {os.path.abspath(self.db)}", self.list_tables())
        pass

    def db_name(self, db_path, db_name):
        #db = str(os.path.join(db_path, db_name))
        db = os.path.abspath(str(os.path.join(db_path, db_name)))
        self.db = db
        print(f"[DEBUG] Using DB file:  {db}", self.list_tables())
        return db

    def list_tables(self):
        import sqlite3
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        print(f"[DEBUG] Tables in DB: {tables}")
        return tables

    def fill_table(self, tbl_name, data):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        columns = list(data[0].keys())
        columns_def = ", ".join([f"{col} TEXT" for col in columns])
        cursor.execute(f"DROP TABLE IF EXISTS {tbl_name};")
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {tbl_name} ({columns_def})")
        # Dynamically insert data
        placeholders = ", ".join(["?" for _ in columns])
        insert_sql = f"INSERT INTO {tbl_name} ({', '.join(columns)}) VALUES ({placeholders})"
        for row in data:
            values = tuple(row[col] for col in columns)
            cursor.execute(insert_sql, values)

        # Save changes and close connection
        conn.commit()
        conn.close()



if __name__ == '__main__':
    #db = SqliteDB()
    #df = db.read_table('RMA', '2024-04-05', '2025-04-12')
    #print(df)
    pass


