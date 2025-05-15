from datetime import date, timedelta, datetime
from sql_db_rw import SqliteDB
from Graphs import DrawPlot
from utils import lib_gen

gen = lib_gen.FormatDates()
date_from = gen.format_date_to_uso('11/03/2024')
date_upto = gen.format_date_to_uso('12/04/2025', last_sec=True)
sql = SqliteDB()
#df = sql.read_table('RMA', date_from, date_upto)
# for v in df:
#     print(v)
#df = sql.read_table('RMA', date_from, date_upto, cat='nff', cat_val='1')
# print(type(df))
# for v in df:
#     print(v)
#df = sql.read_table('RMA', date_from, date_upto, cat='nff', cat_val='1', ret_cat='customers_name, open_date')
#print(type(df))
# for v in df:
#     print(v)
# df = sql.read_table('RMA', date_from, date_upto, cat='product_line', cat_val="ETX-203AX", ret_cat='failure_desc, open_date')
# #print(type(df))
# for v in df:
#     print(v)
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

# options = {
#     'cat' : 'customers_name',
#     'subcat' : None,
#     'cat2' : None,
#     'tit': 'RMA by CUstomer',
#     'xaxis_tit' : 'Customer',
#     'yaxis_tit' : 'Quantity',
#     'chart_type' : 'bar',
# }
#dp.by_str_cat_subcat(df, **options)

# options = {
#     'cat' : 'customers_name',
#     'subcat' : None,
#     'cat2' : 'nff',
#     'tit': 'NFF by Customer',
#     'xaxis_tit' : 'NFFbyCustomer',
#     'yaxis_tit' : 'Quantity',
#     'chart_type' : 'bar',
# }
#dp.by_str_cat_subcat(df, **options)

# options = {
#     'cat' : 'product_line',
#     'subcat' : None,
#     'cat2' : 'nff',
#     'tit': 'NFF by product_line',
#     'xaxis_tit' : 'NFFbyproduct_line',
#     'yaxis_tit' : 'Quantity',
#     'chart_type' : 'bar',
# }
#df = sql.read_table('RMA', date_from, date_upto, cat='nff', cat_val='1', ret_cat='customers_name, open_date')
#dp.by_str_cat_subcat(df, **options)

#dp.by_string(df, 'rad_part', 'RMAs by rad_parttt', 'Quantity', 'rad_part')
# options = {
#     'cat' : 'rad_part',
#     'subcat' : 'LF-IC-NT5TU32M16CG-3CI/ETX',
#     'cat2' : 'date_code',
#     'tit': 'RMAs by Date Code of LF-IC-NT5TU32M16CG-3CI_ETX',
#     'xaxis_tit' : 'Date Code',
#     'yaxis_tit' : 'Quantity',
#     'chart_type' : 'bar',
# }
#dp.by_str_cat_subcat(df, **options)

# options = {
#     'cat' : 'rad_part',
#     'subcat' : None,
#     'cat2' : 'date_code',
#     'tit': 'RMAs by Date Code',
#     'xaxis_tit' : 'Date Code',
#     'yaxis_tit' : 'Quantity',
#     'chart_type' : 'bar',
# }
#dp.by_str_cat_subcat(df, **options)

# options = {
#     'cat' : None,
#     'subcat' : None,
#     'cat2' : 'date_code',
#     'tit': 'RMAs by Date Codes',
#     'xaxis_tit' : 'Date Code',
#     'yaxis_tit' : 'Quantity',
#     'chart_type' : 'bar',
# }
# #dp.by_str_cat_subcat(df, **options)

# options = {
#     'cat' : 'rad_part',
#     'subcat' : 'PS-250/48-4U',
#     'cat2' : 'date_code',
#     'tit': 'RMAs by Date Code of PS-250_48-4U',
#     'xaxis_tit' : 'Date Code',
#     'yaxis_tit' : 'Quantity',
#     'chart_type' : 'bar',
# }
#dp.by_str_cat_subcat(df, **options)

# options = {
#     'cat' : 'rad_part',
#     'subcat' : None,
#     'cat2' : None,
#     'tit': 'RMA by rad_part',
#     'xaxis_tit' : 'rad_part',
#     'yaxis_tit' : 'Quantity',
#     'chart_type' : 'bar',
# }
#dp.by_str_cat_subcat(df, **options)

# options = {
#     'cat' : 'product_line',
#     'subcat' : 'ETX-203AX',
#     'cat2' : 'location',
#     'tit': 'RMAs by Reference of ETX-203AX',
#     'xaxis_tit' : 'Reference',
#     'yaxis_tit' : 'Quantity',
#     'chart_type' : 'bar',
# }
# dp.by_str_cat_subcat(df, **options)

# options = {
#     'cat' : 'product_line',
#     'subcat' : 'ETX-203AX',
#     'cat2' : 'rma_kind_desc',
#     'tit': 'RMAs by rma_kind_desc of ETX-203AX',
#     'xaxis_tit' : 'rma_kind_desc',
#     'yaxis_tit' : 'Quantity',
#     'chart_type' : 'bar',
# }
#dp.by_str_cat_subcat(df, **options)

#dp.by_subcat_day(df, 'doa', '1')

# options = {
#     'cat' : 'customers_name',
#     'subcat' : 'BYNET',
#     'cat2' : 'doa',
#     'tit': 'RMAs by DOA of BYNET',
#     'xaxis_tit' : 'DOA',
#     'yaxis_tit' : 'Quantity',
#     'chart_type' : 'bar',
# }
# dp.by_str_cat_subcat(df, **options)

# options = {
#     'cat' : 'customers_name',
#     'subcat' : 'BYNET',
#     'cat2' : 'nff',
#     'tit': 'RMAs by NFF of BYNET',
#     'xaxis_tit' : 'NFF',
#     'yaxis_tit' : 'Quantity',
#     'chart_type' : 'bar',
# }
#dp.by_str_cat_subcat(df, **options)

# options = {
#     'cat' : 'product_line',
#     'subcat' : 'ETX-203AX',
#     'cat2' : 'failure_desc',
#     'tit': 'RMAs by failure_desc of ETX-203AX',
#     'xaxis_tit' : 'failure_desc',
#     'yaxis_tit' : 'Quantity',
#     'chart_type' : 'bar',
# }
#dp.by_str_cat_subcat(df, **options)

# options = {
#     'cat' : 'product_line',
#     'subcat' : 'ETX-203AX',
#     'cat2' : 'repair_types',
#     'tit': 'RMAs by repair_types of ETX-203AX',
#     'xaxis_tit' : 'repair_types',
#     'yaxis_tit' : 'Quantity',
#     'chart_type' : 'bar',
# }
#dp.by_str_cat_subcat(df, **options)




## what kinds of failure_desc were shipped product_line ETX-203AX

returned = 'failure_desc'
options = {
    'cat' : returned,
    'tit': 'RMAs by failure_desc of ETX-203AX',
    'xaxis_tit' : 'failure_desc',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=[returned], cat='product_line', cat_val="ETX-203AX")
# dp.by_category(df, **options)

#  NFF or not
returned = 'nff'
options = {
    'cat' : returned,
    'tit': 'NFF or not',
    'xaxis_tit' : 'NFF',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto,  ret_cat=[returned])
# dp.by_category(df, **options)


# which customers send NFF
returned = 'customers_name'
options = {
    'cat' : returned,
    'tit': 'NFF by customer',
    'xaxis_tit' : 'Customer',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=[returned], cat='nff', cat_val='1')
# dp.by_category(df, **options)

# which clients send RMA
returned = 'customers_name'
options = {
    'cat' : returned,
    'tit': 'RMA by customer',
    'xaxis_tit' : 'Customer',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=[returned])
#dp.by_category(df, **options)

## which catalog shipped as NFF
returned = 'catalog'
options = {
    'cat' : returned,
    'tit': 'NFF by catalog',
    'xaxis_tit' : 'NFF by catalog',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, cat='nff', cat_val='1', ret_cat=[returned])
#dp.by_category(df, **options)

## which product_line shipped as NFF
returned = 'product_line'
options = {
    'cat' : returned,
    'tit': 'NFF by product_line',
    'xaxis_tit' : 'NFF by product_line',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, cat='nff', cat_val='1', ret_cat=[returned])
#dp.by_category(df, **options)


## Data codes for LF-IC-NT5TU32M16CG-3CI/ETX
# returned = 'rad_part'
options = {
    'cat' : 'date_code',
    'tit': 'RMAs by Date Code of LF-IC-NT5TU32M16CG-3CI_ETX',
    'xaxis_tit' : 'Date Code',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['date_code'], cat='rad_part', cat_val='LF-IC-NT5TU32M16CG-3CI/ETX')
# dp.by_category(df, **options)

## Data codes for all
returned = 'date_code'
options = {
    'cat' : returned,
    'tit': 'RMAs by Date Code of all',
    'xaxis_tit' : 'Date Code',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=[returned])
# dp.by_category(df, **options)

# DOAs
returned = 'customers_name'
options = {
    'cat' : returned,
    'tit': 'RMAs by DOA',
    'xaxis_tit' : 'DOA',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=[returned], cat='doa', cat_val='1')
# dp.by_category(df, **options)

# DOAs by customers_name CANCOM GMBH
# returned = 'customers_name'
options = {
    'cat' : 'doa',
    'tit': 'RMAs by DOA CANCOM GMBH',
    'xaxis_tit' : 'DOA CANCOM GMBH',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['doa'], cat='customers_name', cat_val='CANCOM GMBH',cat2='doa', cat2_val='1')
# dp.by_category(df, **options)
# dp.by_cat_day(df, **options)

# NFF by customers_name Bynet
# returned = 'customers_name'
options = {
    'cat' : 'nff',
    'tit': 'RMAs by NFF Bynet',
    'xaxis_tit' : 'NFF Bynet',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
df = sql.read_table('RMA', date_from, date_upto, ret_cat=['nff'], cat='customers_name', cat_val='BYNET', cat2='nff', cat2_val='1')
dp.by_category(df, **options)
dp.by_cat_day(df, **options)

## what kinds of repair_types were shipped product_line ETX-203AX
returned = 'repair_types'
options = {
    'cat' : returned,
    'tit': 'RMAs by repair_types of ETX-203AX',
    'xaxis_tit' : 'repair_types',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=[returned], cat='product_line', cat_val="ETX-203AX")
# dp.by_category(df, **options)

##  kinds of repair_types
returned = 'repair_types'
options = {
    'cat' : returned,
    'tit': 'RMAs by repair_types',
    'xaxis_tit' : 'repair_types',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=[returned])
# dp.by_category(df, **options)

##  which components replaced more
returned = 'rad_part'
options = {
    'cat' : returned,
    'tit': 'RMAs by components',
    'xaxis_tit' : 'components',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=[returned])
# dp.by_category(df, **options)

##  Non Repairable units
returned = 'repair_types'
options = {
    'cat' : returned,
    'tit': 'Non Repairable units',
    'xaxis_tit' : 'Non Repairable',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=[returned], cat='repair_types', cat_val='Non Repairable')
# dp.by_category(df, **options)
# dp.by_cat_day(df, **options)

##  Non Repairable units per customer
# returned = 'repair_types'
options = {
    'cat' : 'customers_name',
    'tit': 'Non Repairable units per customer',
    'xaxis_tit' : 'Non Repairable',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['customers_name'], cat='repair_types', cat_val='Non Repairable')
# dp.by_category(df, **options)

##  Non Repairable units per "catalog"
# returned = 'repair_types'
options = {
    'cat' : 'catalog',
    'tit': 'Non Repairable units per catalog',
    'xaxis_tit' : 'Non Repairable',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['catalog'], cat='repair_types', cat_val='Non Repairable')
# dp.by_category(df, **options)



## which location (reference) is problematic in product_line ETX-203AX
returned = 'product_line'
options = {
    'cat' : 'location',
    'tit': 'RMAs by Reference of ETX-203AX',
    'xaxis_tit' : 'Reference',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['location'], cat='product_line', cat_val='ETX-203AX')
# dp.by_category(df, **options)