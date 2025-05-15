import sqlite3
import os


class SqliteDB:
    def __init__(self):
        qsfc_dir = os.path.dirname(os.path.abspath(__file__))
        self.db = os.path.join(qsfc_dir, 'db.db')
        print(f"[DEBUG] Using DB file: {self.db}")

        # self.db = 'db.db'
        #self.db = os.path.join(os.path.dirname(__file__), '..', 'db.db')
        #self.db = os.path.abspath(self.db)
        print(f"[DEBUG] Using DB file: {os.path.abspath(self.db)}", self.list_tables())

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

    def ne_read_table(self, tbl_name, start_date, end_date, ret_cat='*', cat=None, cat2=None, cat_val=None, cat2_val=None):
        print('read_table' , tbl_name, start_date, end_date, cat, cat_val)
        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if cat:
            cursor.execute(f"SELECT {ret_cat} FROM {tbl_name} "
                           f"WHERE (open_date BETWEEN '{start_date}' AND '{end_date}') AND {cat}={cat_val})"
                           f"ORDER BY open_date desc;")
        else:
            cursor.execute(f"SELECT * FROM {tbl_name} "
                       f"WHERE open_date BETWEEN '{start_date}' AND '{end_date}' "
                       f"ORDER BY open_date desc;")
        #rows = cursor.fetchall()
        rows = [dict(row) for row in cursor.fetchall()]


        with open(f'c:/temp/{tbl_name}.json', 'w') as f:
            f.write("Headers" + '\n')
            for row in rows:
                #print(row)
                f.write(str(row)+'\n')

        # Commit changes and close the connection
        conn.commit()
        conn.close()
        return rows

    def read_table(self, tbl_name, start_date, end_date, ret_cat=None, cat=None, cat2=None, cat_val=None, cat2_val=None):
        print('read_table' , tbl_name, start_date, end_date, ret_cat, cat, cat_val)
        if ret_cat is None:
            ret_cat_str = '*'
        elif isinstance(ret_cat, list):
            if 'open_date' not in ret_cat:
                ret_cat.append('open_date')
            ret_cat_str = ', '.join(ret_cat)
        else:
            # Если по ошибке передали строку — просто используем её
            ret_cat_str = ret_cat

        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = f"SELECT {ret_cat_str} FROM {tbl_name} WHERE (open_date BETWEEN ? AND ?)"
        params = [start_date, end_date]

        if cat:
            query += f" AND {cat} = ?"
            params.append(cat_val)

        if cat2:
            query += f" AND {cat2} = ?"
            params.append(cat2_val)

        query += " ORDER BY open_date DESC;"

        print('qry: ',query, 'params: ', params, '\n')
        cursor.execute(query, params)

        rows = [dict(row) for row in cursor.fetchall()]
        #print('rows: ', rows, '\n')
        # Commit changes and close the connection
        conn.commit()
        conn.close()


        with open(f'c:/temp/{tbl_name}.json', 'w') as f:
            f.write("Headers" + '\n')
            for row in rows:
                #print(row)
                f.write(str(row)+'\n')

        return rows

    def retrive_min_max_dates(self, df):
        all_dates = sorted({row['open_date'] for row in df})
        date_from = min(all_dates).split(' ')[0]
        date_to = max(all_dates).split(' ')[0]
        return date_from, date_to

if __name__ == '__main__':
    db = SqliteDB()
    df = db.read_table('RMA', '2024-04-05', '2025-04-12')
    print(df)


