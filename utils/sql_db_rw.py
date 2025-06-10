import sqlite3
import os
import datetime
import collections
import logging

import utils.lib_gen as gen
from utils.mdl_logger import setup_logger
setup_logger('read_dbs_log.html')
logger = logging.getLogger(__name__)


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

    def build_check_exists_query(self, table, columns):
        where_clause = " AND ".join(f"{col}=?" for col in columns)
        sql = f"SELECT COUNT(*) FROM {table} WHERE {where_clause}"
        return sql

    def fill_table(self, tbl_name, data, chk_exist="no"):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        columns = list(data[0].keys())
        columns_def = ", ".join([f"{col} TEXT" for col in columns])
        #cursor.execute(f"DROP TABLE IF EXISTS {tbl_name};")
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {tbl_name} ({columns_def})")
        # Dynamically insert data
        placeholders = ", ".join(["?" for _ in columns])

        insert_sql = f"INSERT INTO {tbl_name} ({', '.join(columns)}) VALUES ({placeholders})"
        check_sql = self.build_check_exists_query(tbl_name, columns)

        print(f'insert_sql:<{insert_sql}>')
        print(f'check_sql:<{check_sql}>')

        # for row in data:
        #     sql, values = self.build_count_query("AOI_data", row)
        #     print(f'check_sql:<{sql}> values:<{values}> ')
        #     cursor.execute(sql, values)
        #     count = cursor.fetchone()[0]
        #     print(f"Count: {count}")

        for row in data:
            values = tuple(row[col] for col in columns)

            if chk_exist=='yes':
                cursor.execute(check_sql, values)
                count = cursor.fetchone()[0]
            else:
                count = 0
            #print(count, values)

            if count == 0:
                cursor.execute(insert_sql, values)
            elif count == 1:
                print(f"The row already exists: {values}")
            else:
                print(f"Error: there are {count} duplications for {values}!")
            # values = tuple(row[col] for col in columns)
            # cursor.execute(insert_sql, values)

        # Save changes and close connection
        conn.commit()
        conn.close()

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



