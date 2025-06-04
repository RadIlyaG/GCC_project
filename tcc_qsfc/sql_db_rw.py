import sqlite3
import os
import datetime
import collections
from pathlib import Path

#from qsfc.sql_db_rw import SqliteDB as qdb
from utils.sql_db_rw import SqliteDB as sqldb


class SqliteDB(sqldb):
    def __init__(self):
        super().__init__()
        #work_dir = os.path.dirname(os.path.abspath(__file__))
        #self.db = os.path.join('c:/ate-controlcenter', 'jerAteStats.db')
        #self.db = os.path.join(db_path, db_name)
        #print(f"[DEBUG] Using DB file: {self.db}")

        # self.db = 'db.db'
        #self.db = os.path.join(os.path.dirname(__file__), '..', 'db.db')
        #self.db = os.path.abspath(self.db)
        #print(f"[DEBUG] Using DB file: {os.path.abspath(self.db)}", self.list_tables())
        pass

    def get_qsfc_prod_lines(self,qsfc_path):
        sql_obj = sqldb()
        qsfc_db_file = sql_obj.db_name(qsfc_path, 'db_qsfc.db')
        #qsfc_db = qsfc.db
        conn = sqlite3.connect(qsfc_db_file)
        cursor = conn.cursor()
        query = f"""
                    select product_line   FROM  RMA
                    union
                    select product_line   FROM Prod ;
                """
        cursor.execute(query)
        rows = [row[0] for row in cursor.fetchall()]
        print(f'QSFC product_line:{len(rows)}')
        conn.close()
        return rows

    def get_tcc_catalogs(self, tcc_path):
        sql_obj = sqldb()
        tcc_db_file = sql_obj.db_name(tcc_path, 'jerAteStats.db')
        conn = sqlite3.connect(tcc_db_file)
        cursor = conn.cursor()
        query = f"""
                    select UutName  FROM  tbl where length(UutName)> 2 group by UutName ;
                """
        cursor.execute(query)
        rows = [row[0] for row in cursor.fetchall()]
        print(f'TCC UutNames: {len(rows)}')
        conn.close()
        return rows

    def create_merged_prod_line_with_priority(self, qsfc_db_file, tcc_db_file, output_db_file, date_from, date_upto):
        print(f'create_merged_prod_line_with_priority',qsfc_db_file, tcc_db_file, output_db_file, date_from, date_upto)
        #import sqlite3
        #

        # Remove prev output result file
        try:
            Path(output_db_file).unlink(missing_ok=True)
        except Exception as ee:
            print(ee)
            return -1

        conn_out = sqlite3.connect(output_db_file)
        cur_out = conn_out.cursor()

        # Подключаем основную и внешнюю БД
        cur_out.execute(f"ATTACH DATABASE '{qsfc_db_file}' AS main_db")
        cur_out.execute(f"ATTACH DATABASE '{tcc_db_file}' AS db2")

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

    def ensure_indexes_in_main_db(self, main_db_path):
        print(f'ensure_indexes_in_main_db main_db_path:{main_db_path}')
        conn_main = sqlite3.connect(main_db_path)
        cur_main = conn_main.cursor()

        cur_main.execute("CREATE INDEX IF NOT EXISTS idx_rma_catalog ON RMA(catalog)")
        cur_main.execute("CREATE INDEX IF NOT EXISTS idx_prod_tested_catalog ON Prod(tested_catalog)")

        conn_main.commit()
        conn_main.close()





if __name__ == '__main__':
    # db_path = os.path.dirname(os.path.abspath(__file__))
    # db_name = 'db_aoi.db'

    tcc_path = os.path.abspath('c:/ate-controlcenter') # os.path.join('c:/ate-controlcenter', 'jerAteStats.db')
    sql_obj = SqliteDB()
    #('c:/ate-controlcenter', 'jerAteStats.db')
    qsfc_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'qsfc')
    sql_obj.get_qsfc_prod_lines(qsfc_path)
    sql_obj.get_tcc_catalogs(tcc_path)

    tcc_db_file = os.path.join(tcc_path, "jerAteStats.db")
    qsfc_db_file = os.path.join(qsfc_path, 'db_qsfc.db')
    date_from = "2024-01-01"
    date_upto = "2025-12-31"
    output_db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "merged_prod_line.db")
    sql_obj.ensure_indexes_in_main_db(qsfc_db_file)
    sql_obj.create_merged_prod_line_with_priority(qsfc_db_file, tcc_db_file, output_db_file, date_from, date_upto)


