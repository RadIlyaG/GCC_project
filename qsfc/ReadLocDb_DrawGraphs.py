from datetime import date, timedelta, datetime
from sql_db_rw import SqliteDB
from Graphs import DrawPlot
from utils import lib_gen

gen = lib_gen.FormatDates()
date_from = gen.format_date_to_uso('15/03/2024')
date_upto = gen.format_date_to_uso('12/04/2025')
sql = SqliteDB()
df = sql.read_table('RMA', date_from, date_upto)
#print(df)
# df = sql.read_table('Prod', '2024-06-05', '2025-04-12')
# print(len(df))
# for dicti in df:
#     print(dicti)

dp = DrawPlot()
#dp.by_string(df, 'customers_name', 'RMAs by customer', 'Quantity', 'Customer')

#dp.by_subcat_day(df, 'customers_name', 'RAD INC.')
#dp.by_string(df, 'product_line', 'RMAs by product_line', 'Quantity', 'product_line')
#dp.by_cat_day(df, 'product_line')
#dp.by_subcat_day(df, 'product_line', 'ETX-203AX')
#dp.by_string(df, 'rad_part', 'RMAs by rad_part', 'Quantity', 'rad_part')

options = {
    'cat' : 'customers_name',
    'subcat' : None,
    'subcat2' : None,
    'tit': 'RMA by CUstomer',
    'xaxis_tit' : 'Customer',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
#dp.by_str_cat_subcat(df, **options)

options = {
    'cat' : 'customers_name',
    'subcat' : None,
    'subcat2' : 'nff',
    'tit': 'NFF by Customer',
    'xaxis_tit' : 'NFFbyCustomer',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
#dp.by_str_cat_subcat(df, **options)

options = {
    'cat' : 'rad_part',
    'subcat' : 'IC-74LCX16245MEA',
    'subcat2' : 'date_code',
    'tit': 'RMAs by Date Code of IC-74LCX16245MEA',
    'xaxis_tit' : 'Date Code',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
#dp.by_str_cat_subcat(df, **options)

options = {
    'cat' : 'product_line',
    'subcat' : 'ETX-203AX',
    'subcat2' : 'location',
    'tit': 'RMAs by Reference of ETX-203AX',
    'xaxis_tit' : 'Reference',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
dp.by_str_cat_subcat(df, **options)

options = {
    'cat' : 'product_line',
    'subcat' : 'ETX-203AX',
    'subcat2' : 'rma_kind_desc',
    'tit': 'RMAs by rma_kind_desc of ETX-203AX',
    'xaxis_tit' : 'rma_kind_desc',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
dp.by_str_cat_subcat(df, **options)

#dp.by_subcat_day(df, 'doa', '1')

options = {
    'cat' : 'customers_name',
    'subcat' : 'BYNET',
    'subcat2' : 'doa',
    'tit': 'RMAs by DOA of BYNET',
    'xaxis_tit' : 'DOA',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
#dp.by_str_cat_subcat(df, **options)

options = {
    'cat' : 'customers_name',
    'subcat' : 'BYNET',
    'subcat2' : 'nff',
    'tit': 'RMAs by NFF of BYNET',
    'xaxis_tit' : 'NFF',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
#dp.by_str_cat_subcat(df, **options)

options = {
    'cat' : 'product_line',
    'subcat' : 'ETX-203AX',
    'subcat2' : 'failure_desc',
    'tit': 'RMAs by failure_desc of ETX-203AX',
    'xaxis_tit' : 'failure_desc',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
#dp.by_str_cat_subcat(df, **options)

options = {
    'cat' : 'product_line',
    'subcat' : 'ETX-203AX',
    'subcat2' : 'repair_types',
    'tit': 'RMAs by repair_types of ETX-203AX',
    'xaxis_tit' : 'repair_types',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
#dp.by_str_cat_subcat(df, **options)
