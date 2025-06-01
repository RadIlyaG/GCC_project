import sqlite3
import os
import datetime
import collections

from qsfc.sql_db_rw import SqliteDB as qdb


class SqliteDB:
    def __init__(self):
        work_dir = os.path.dirname(os.path.abspath(__file__))
        self.db = os.path.join('c:/ate-controlcenter', 'jerAteStats.db')
        #print(f"[DEBUG] Using DB file: {self.db}")

        # self.db = 'db.db'
        #self.db = os.path.join(os.path.dirname(__file__), '..', 'db.db')
        #self.db = os.path.abspath(self.db)
        #print(f"[DEBUG] Using DB file: {os.path.abspath(self.db)}", self.list_tables())

    def get_qsfc_prod_lines(self):
        qsfc = qdb()
        qsfc_db = qsfc.db
        conn = sqlite3.connect(qsfc_db)
        cursor = conn.cursor()
        query = f"""
                    select product_line   FROM  RMA
                    union
                    select product_line   FROM Prod ;
                """
        cursor.execute(query)
        rows = [row[0] for row in cursor.fetchall()]
        print(len(rows))
        conn.close()
        return rows

    def get_tcc_catalogs(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        query = f"""
                    select UutName  FROM  tbl where length(UutName)> 2 group by UutName ;
                """
        cursor.execute(query)
        rows = [row[0] for row in cursor.fetchall()]
        print(len(rows))
        conn.close()
        return rows

    def create_merged_prod_line_with_priority(main_db_path, external_db_path, output_db_path, date_from, date_upto):
        import sqlite3
        from pathlib import Path

        # Удалим предыдущий результат
        Path(output_db_path).unlink(missing_ok=True)

        conn_out = sqlite3.connect(output_db_path)
        cur_out = conn_out.cursor()

        # Подключаем основную и внешнюю БД
        cur_out.execute(f"ATTACH DATABASE '{main_db_path}' AS main_db")
        cur_out.execute(f"ATTACH DATABASE '{external_db_path}' AS db2")

        # Основная таблица с приоритетом RMA > Prod
        cur_out.execute("DROP TABLE IF EXISTS merged_prod_line")
        cur_out.execute("""
            CREATE TABLE merged_prod_line AS
            WITH product_lines AS (
                SELECT t.UutName AS product, r.product_line, 1 AS priority
                FROM db2.tbl t
                LEFT JOIN main_db.RMA r ON r.catalog = t.UutName
                WHERE date(REPLACE(t.Date, '.', '-')) BETWEEN date(?) AND date(?)

                UNION ALL

                SELECT t.UutName AS product, p.product_line, 2 AS priority
                FROM db2.tbl t
                LEFT JOIN main_db.Prod p ON p.tested_catalog = t.UutName
                WHERE date(REPLACE(t.Date, '.', '-')) BETWEEN date(?) AND date(?)
            )
            SELECT product, product_line
            FROM product_lines
            WHERE product_line IS NOT NULL
            GROUP BY product
            HAVING MIN(priority)
        """, (date_from, date_upto, date_from, date_upto))

        # Таблица продуктов, для которых не найден product_line
        cur_out.execute("DROP TABLE IF EXISTS missing_product_line")
        cur_out.execute("""
            CREATE TABLE missing_product_line AS
            SELECT DISTINCT t.UutName AS product
            FROM db2.tbl t
            LEFT JOIN main_db.RMA r ON r.catalog = t.UutName
            LEFT JOIN main_db.Prod p ON p.tested_catalog = t.UutName
            WHERE r.product_line IS NULL AND p.product_line IS NULL
              AND date(REPLACE(t.Date, '.', '-')) BETWEEN date(?) AND date(?)
        """, (date_from, date_upto))

        conn_out.commit()
        conn_out.close()

    def ensure_indexes_in_main_db(main_db_path):
        conn_main = sqlite3.connect(main_db_path)
        cur_main = conn_main.cursor()

        cur_main.execute("CREATE INDEX IF NOT EXISTS idx_rma_catalog ON RMA(catalog)")
        cur_main.execute("CREATE INDEX IF NOT EXISTS idx_prod_tested_catalog ON Prod(tested_catalog)")

        conn_main.commit()
        conn_main.close()

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
    db.get_qsfc_prod_lines()
    db.get_tcc_catalogs()


