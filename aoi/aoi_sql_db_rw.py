import sqlite3
import os
import datetime
import collections


class SqliteDB:
    def __init__(self):
        qsfc_dir = os.path.dirname(os.path.abspath(__file__))
        self.db = os.path.join(qsfc_dir, 'db_aoi.db')
        #print(f"[DEBUG] Using DB file: {self.db}")

        # self.db = 'db.db'
        #self.db = os.path.join(os.path.dirname(__file__), '..', 'db.db')
        #self.db = os.path.abspath(self.db)
        #print(f"[DEBUG] Using DB file: {os.path.abspath(self.db)}", self.list_tables())

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
        # Динамически вставляем данные
        placeholders = ", ".join(["?" for _ in columns])
        insert_sql = f"INSERT INTO {tbl_name} ({', '.join(columns)}) VALUES ({placeholders})"
        for row in data:
            values = tuple(row[col] for col in columns)
            cursor.execute(insert_sql, values)

        # cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS qry_type (
        #         form_number TEXT PRIMARY KEY,
        #         customers_full_name TEXT,
        #         catalog TEXT
        #     )
        # """)
        # for row in data:
        #     cursor.execute("""
        #         INSERT INTO qry_type (form_number, customers_full_name, catalog)
        #         VALUES (?, ?, ?)
        #     """, (row['form_number'], row['customers_full_name'], row['catalog']))

        # Сохраняем изменения и закрываем соединение
        conn.commit()
        conn.close()



if __name__ == '__main__':
    #db = SqliteDB()
    #df = db.read_table('RMA', '2024-04-05', '2025-04-12')
    #print(df)
    pass


