import sqlite3


class SqliteDB:
    def __init__(self):
        self.db = 'db.db'

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

    def read_table(self, tbl_name, start_date, end_date):
        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {tbl_name} "
                       f"WHERE open_date BETWEEN '{start_date}' AND '{end_date}' "
                       f"ORDER BY open_date ;")
        #rows = cursor.fetchall()
        df = [dict(row) for row in cursor.fetchall()]


        with open('c:/temp/123.csv', 'w') as f:
            pass
            f.write("Headers" + '\n')
            for row in df:
                #print(row)
                f.write(str(row)+'\n')

        # Commit changes and close the connection
        conn.commit()
        conn.close()
        return df

    def retrive_min_max_dates(self, df):
        all_dates = sorted({row['open_date'] for row in df})
        date_from = min(all_dates).split(' ')[0]
        date_to = max(all_dates).split(' ')[0]
        return date_from, date_to

if __name__ == '__main__':
    db = SqliteDB()
    df = db.read_table('RMA', '2024-04-05', '2025-04-12')
    print(df)


