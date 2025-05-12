from datetime import date, timedelta, datetime
from sql_db_rw import SqliteDB
from Graphs import DrawPlot
from utils import lib_gen

# def format_date_to_uso(date): #rom '15/06/2024' → '2024-06-15 2024-06-15 00:00:00.000000'
#     date_from_obj = datetime.strptime(date, '%d/%m/%Y')
#     return date_from_obj.strftime('%Y-%m-%d %H:%M:%S.%f')
#
# def format_date_from_iso(date):  #from '2024-06-15' → '15/06/2024'
#     date_obj = datetime.strptime(date, '%Y-%m-%d')
#     return  date_obj.strftime('%d/%m/%Y')


gen = lib_gen.FormatDates()
date_from = gen.format_date_to_uso('15/03/2025')
date_upto = gen.format_date_to_uso('12/04/2025')
sql = SqliteDB()
df = sql.read_table('RMA', date_from, date_upto)
#print(df)
# df = sql.read_table('Prod', '2024-06-05', '2025-04-12')
# print(len(df))
# for dicti in df:
#     print(dicti)

dp = DrawPlot()
dp.by_string(df, 'customers_name', 'RMAs by customer', 'Quantity', 'Customer')