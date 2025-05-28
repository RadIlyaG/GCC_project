import sqlite3
import os
import datetime
import collections


class SqliteDB:
    def __init__(self):
        work_dir = os.path.dirname(os.path.abspath(__file__))
        self.db = os.path.join('c:/ate-controlcenter', 'jerAteStats.db')
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
        #print(f'read table type(rows):{type(rows)}')
        return rows

    def start_of_week(self, date):
        """returns start of week for date."""
        weekday = date.weekday()  # 0 = monday
        sunday = date - datetime.timedelta(days=(weekday + 1) % 7)
        return sunday.replace(hour=0, minute=0, second=0, microsecond=0)


    def retrive_min_max_dates(self, df):
        all_dates = sorted({row['open_date'] for row in df})
        date_from = min(all_dates).split(' ')[0]
        date_to = max(all_dates).split(' ')[0]
        return date_from, date_to



    def read_period_counts(self, tbl_name, start_date, end_date, period='month'):
        print(f'\nread_period_counts {start_date}, {end_date}, {period}')
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        if period == 'month':
            date_expr = "strftime('%Y-%m', open_date)"
        elif period == 'week':
            # set sunday as first week day
            date_expr = "strftime('%Y-%m-%d', date(open_date, '-' || ((strftime('%w', open_date) + 0) % 7) || ' days'))"
        else:
            raise ValueError("period must be 'month' or 'week'")

        query = f"""
            SELECT {date_expr} AS period, COUNT(*) as count
            FROM {tbl_name}
            WHERE open_date BETWEEN ? AND ?
            GROUP BY period
            ORDER BY period;
        """

        params = [start_date, end_date]

        cursor.execute(query, params)
        result = [{'period': row[0], 'count': row[1]} for row in cursor.fetchall()]

        conn.close()

        print(f'read_period_counts type(result):{type(result)}')
        return result

if __name__ == '__main__':
    db = SqliteDB()
    df = db.read_table('RMA', '2024-04-05', '2025-04-12')
    print(df)


