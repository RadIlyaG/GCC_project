import sqlite3
import os
import datetime
import collections


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


    def read_table(self, tbl_name, start_date, end_date,
                   ret_cat=None, cat=None, cat2=None, cat_val=None, cat2_val=None,
                   excludes=None):
        print('read_table' , tbl_name, start_date, end_date, ret_cat, cat, cat_val, excludes)
        orig_ret_cat = []
        if ret_cat is None:
            ret_cat_str = '*'
        elif isinstance(ret_cat, list):
            orig_ret_cat = ret_cat.copy()

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

        if excludes:
            print(f'{type(excludes)}, {type(orig_ret_cat)}')
            for excl in excludes:
                print(f'{type(excl)} , {excl}')
                placeholders = ', '.join(['?'])
                query += f" AND {placeholders} NOT IN ({orig_ret_cat[0]})"
                params.extend([excl]) ## convert string to list


        # if cat:
        #     query += f" AND {cat} = ?"
        #     params.append(cat_val)
        if cat:
            if isinstance(cat_val, list):
                placeholders = ', '.join(['?'] * len(cat_val))
                query += f" AND {cat} IN ({placeholders})"
                params.extend(cat_val)
            else:
                query += f" AND {cat} = ?"
                params.append(cat_val)

        # if cat2:
        #     query += f" AND {cat2} = ?"
        #     params.append(cat2_val)
        if cat2:
            if isinstance(cat2_val, list):
                placeholders = ', '.join(['?'] * len(cat2_val))
                query += f" AND {cat2} IN ({placeholders})"
                params.extend(cat2_val)
            else:
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

    def start_of_week(self, date):
        """returns start of week for date."""
        weekday = date.weekday()  # 0 = monday
        sunday = date - datetime.timedelta(days=(weekday + 1) % 7)
        return sunday.replace(hour=0, minute=0, second=0, microsecond=0)

    def read_table_with_aggrigation(self, tbl_name, start_date, end_date, ret_cat=None, cat=None, cat2=None, cat_val=None, cat2_val=None, group_by=None):
        print('\nread_table' , tbl_name, start_date, end_date, ret_cat, cat, cat_val, cat2, cat2_val, group_by)
        if ret_cat is None:
            # ret_cat_str = '*'
            ret_cat_list = ['*']
        elif isinstance(ret_cat, list):
            # if 'open_date' not in ret_cat:
            #     ret_cat.append('open_date')
            # ret_cat_str = ', '.join(ret_cat)
            ret_cat_list = list(ret_cat)
        else:
            ## use string if it was supplied by mistake
            #ret_cat_str = ret_cat
            ret_cat_list = [ret_cat]

        ## open_date must be
        if 'open_date' not in ret_cat_list:
            ret_cat_list.append('open_date')

        # Если агрегация и фильтрация по cat — временно добавим его
        temp_cat_added = False
        if group_by in ['week', 'day'] and cat and cat not in ret_cat_list:
            ret_cat_list.append(cat)
            temp_cat_added = True

        ret_cat_str = ', '.join(ret_cat_list)

        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = f"SELECT {ret_cat_str} FROM {tbl_name} WHERE (open_date BETWEEN ? AND ?)"
        params = [start_date, end_date]

        if cat:
            if isinstance(cat_val, list):
                placeholders = ', '.join(['?'] * len(cat_val))
                query += f" AND {cat} IN ({placeholders})"
                params.extend(cat_val)
            else:
                query += f" AND {cat} = ?"
                params.append(cat_val)

        if cat2:
            if isinstance(cat2_val, list):
                placeholders = ', '.join(['?'] * len(cat2_val))
                query += f" AND {cat2} IN ({placeholders})"
                params.extend(cat2_val)
            else:
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

        if group_by == 'week':
            # week (sun-sat) aggregation
            # weekly_counts = collections.Counter()
            # for row in rows:
            #     dt = datetime.datetime.strptime(row['open_date'].split('.')[0], "%Y-%m-%d %H:%M:%S")
            #     week_start = self.start_of_week(dt)
            #     weekly_counts[week_start] += 1
            # result = [{'week_start': k.strftime("%Y-%m-%d"), 'count': v} for k, v in sorted(weekly_counts.items())]
            # #return result
            weekly_counts = collections.Counter()
            for row in rows:
                dt = datetime.datetime.strptime(row['open_date'].split('.')[0], "%Y-%m-%d %H:%M:%S")
                week_start = self.start_of_week(dt).strftime("%Y-%m-%d")
                key = (week_start, row[cat]) if cat and cat in row else (week_start,)
                weekly_counts[key] += 1

            result = []
            for key, count in sorted(weekly_counts.items()):
                entry = {'week': key[0], 'count': count}
                if cat and len(key) > 1:
                    entry[cat] = key[1]
                result.append(entry)
            #return result

        elif group_by == 'day':
            # day aggregation
            # daily_counts = collections.Counter()
            #
            # for row in rows:
            #     print('group_by: ', group_by, 'row: ', row)
            #     dt = datetime.datetime.strptime(row['open_date'].split('.')[0], "%Y-%m-%d %H:%M:%S")
            #     day = dt.date().isoformat()
            #     daily_counts[day] += 1
            #
            # #print('group_by: ', group_by, 'daily_counts: ', sorted(daily_counts.items()))
            # result = [{'day': k, 'count': v} for k, v in sorted(daily_counts.items())]
            # #result = [{'open_date': k, 'count': v} for k, v in sorted(daily_counts.items())]
            # return result
            daily_counts = collections.Counter()
            for row in rows:
                dt = datetime.datetime.strptime(row['open_date'].split('.')[0], "%Y-%m-%d %H:%M:%S")
                day = dt.date().isoformat()
                key = (day, row[cat]) if cat and cat in row else (day,)
                daily_counts[key] += 1

            result = []
            for key, count in sorted(daily_counts.items()):
                entry = {'day': key[0], 'count': count}
                if cat and len(key) > 1:
                    entry[cat] = key[1]
                #print('key: ', key, 'count: ', count, entry)
                result.append(entry)
            #return result

        else:
            # no aggregation
            if temp_cat_added:
                for row in rows:
                    row.pop(cat, None)
            result = rows


        with open(f'c:/temp/{tbl_name}.json', 'w') as f:
            f.write("Headers" + '\n')
            for row in result:
                #print(row)
                f.write(str(row)+'\n')

        return result

    def retrive_min_max_dates(self, df):
        all_dates = sorted({row['open_date'] for row in df})
        date_from = min(all_dates).split(' ')[0]
        date_to = max(all_dates).split(' ')[0]
        return date_from, date_to

if __name__ == '__main__':
    db = SqliteDB()
    df = db.read_table('RMA', '2024-04-05', '2025-04-12')
    print(df)


