import sqlite3
import os
import datetime
from datetime import datetime
import collections
import logging
import json

import utils.lib_gen as gen

# from utils.mdl_logger import setup_logger
# setup_logger('read_dbs_log.html')
# logger = logging.getLogger(__name__)


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

    def build_count_query(self, table, conditions: dict):
        where_clause = " AND ".join(f"{k}=?" for k in conditions.keys())
        sql = f"SELECT COUNT(*) FROM {table} WHERE {where_clause}"
        values = tuple(conditions.values())
        return sql, values

    def build_check_exists_query(self, table, key_columns):
        where_clause = " AND ".join(f"{col}=?" for col in key_columns)
        sql = f"SELECT COUNT(*) FROM {table} WHERE {where_clause}"
        return sql

    def log_duplicate(self, cursor, table_name, columns, values):
        timestamp = datetime.now().isoformat(timespec='seconds')
        columns_str = json.dumps(columns)
        values_str = json.dumps(values)
        cursor.execute(
            "INSERT INTO duplicate_log (table_name, timestamp, column_names, row_values) VALUES (?, ?, ?, ?)",
            (table_name, timestamp, columns_str, values_str)
        )

    def fill_table(self, tbl_name, data, chk_exist="no"):
        if chk_exist == 'yes':
            conn_dpl = sqlite3.connect("db_dpl.db")
            cursor_dpl = conn_dpl.cursor()
            cursor_dpl.execute("""
                CREATE TABLE IF NOT EXISTS duplicate_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_name TEXT,
                    timestamp TEXT,
                    column_names  TEXT,
                    row_values  TEXT
                );
            """)

        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        columns = list(data[0].keys())
        columns_def = ", ".join([f"{col} TEXT" for col in columns])
        #cursor.execute(f"DROP TABLE IF EXISTS {tbl_name};")
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {tbl_name} ({columns_def})")
        # Dynamically insert data
        placeholders = ", ".join(["?" for _ in columns])

        insert_sql = f"INSERT INTO {tbl_name} ({', '.join(columns)}) VALUES ({placeholders})"
        duplicate_check_fields = ["aoi_name", "aoi_test_time", "aoi_mkt", "po_number"]
        check_sql = self.build_check_exists_query(tbl_name, duplicate_check_fields)

        for row in data:
            values = tuple(row[col] for col in columns)

            key_values = ()
            if chk_exist=='yes':
                key_values = tuple(row[col] for col in duplicate_check_fields)
                cursor.execute(check_sql, key_values)
                count = cursor.fetchone()[0]
            else:
                count = 0

            if count == 0:
                cursor.execute(insert_sql, values)
            else:
                self.log_duplicate(cursor_dpl, tbl_name, duplicate_check_fields, key_values)

        # Save changes and close connection
        conn.commit()
        conn.close()

        if chk_exist=='yes':
            conn_dpl.commit()
            conn_dpl.close()


    def get_last_date(self, tbl_name, tst_field):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        query = f"SELECT MAX({tst_field}) from {tbl_name}"
        cursor.execute(query)
        last_date =  cursor.fetchall()[0][0].split(" ")[0]

        conn.commit()
        conn.close()

        return last_date




if __name__ == '__main__':
    #db = SqliteDB()
    #df = db.read_table('RMA', '2024-04-05', '2025-04-12')
    #print(df)
    pass



