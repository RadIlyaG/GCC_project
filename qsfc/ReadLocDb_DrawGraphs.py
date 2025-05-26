from datetime import date, timedelta, datetime
from sql_db_rw import SqliteDB
from Graphs import DrawPlot
from utils import lib_gen

gen = lib_gen.FormatDates()
date_from = gen.format_date_to_uso('01/01/2025')
date_upto = gen.format_date_to_uso('31/05/2025', last_sec=True)
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

#############################################################################################


# what kinds of failure_desc were shipped product_line ETX-203AX
## Show me all 'failure_desc' where 'product_line' is 'ETX-203AX'
options = {
    'cat' : 'failure_desc',
    'tit': 'Failure Types of ETX-203AX',
    'xaxis_tit' : 'Failure Types',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['failure_desc'], cat='product_line', cat_val="ETX-203AX")
# dp.by_category(df, **options)

#  NFF or not
## Show me all 'nff'
returned = 'nff'
options = {
    'cat' : 'nff',
    'tit': 'NFF or not',
    'xaxis_tit' : 'NFF',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto,  ret_cat=['nff'])
# dp.by_category(df, **options)


# which customers send NFF
## Show me all 'customers_name' which sent 'nff'
options = {
    'cat' : 'customers_name',
    'tit': 'NFF by customer',
    'xaxis_tit' : 'Customer',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['customers_name'], cat='nff', cat_val='1')
# dp.by_category(df, **options)

# which clients send RMA
## Show me all 'customers_name'
options = {
    'cat' : 'customers_name',
    'tit': 'RMA by customer',
    'xaxis_tit' : 'Customer',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['customers_name'])
#dp.by_category(df, **options)

## which catalog shipped as NFF
## Swhow me all 'catalog' where 'nff' is '1'
options = {
    'cat' : 'catalog',
    'tit': 'NFF by catalog',
    'xaxis_tit' : 'NFF by catalog',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['catalog'], cat='nff', cat_val='1')
# dp.by_category(df, **options)


## which product_line shipped as NFF
## Show me all 'product_line' where 'nff' is '1'
options = {
    'cat' : 'product_line',
    'tit': 'NFF by product_line',
    'xaxis_tit' : 'NFF by product_line',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
    'drill_plot_only' : False,
}
df = sql.read_table('RMA', date_from, date_upto, ret_cat=['product_line'], cat='nff', cat_val='1')
dp.by_category(df, **options)


## Data codes for LF-IC-NT5TU32M16CG-3CI/ETX
## Show me all 'date_code' where 'rad_part' is 'LF-IC-NT5TU32M16CG-3CI/ETX'
options = {
    'cat' : 'date_code',
    'tit': 'RMAs by Date Code of LF-IC-NT5TU32M16CG-3CI_ETX',
    'xaxis_tit' : 'Date Code',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['date_code'], cat='rad_part', cat_val='LF-IC-NT5TU32M16CG-3CI/ETX')
# dp.by_category(df, **options)

# Data codes for all
## Show me all 'date_code'
options = {
    'cat' : 'date_code',
    'tit': 'RMAs by Date Code of all',
    'xaxis_tit' : 'Date Code',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['date_code'])
# dp.by_category(df, **options)

# DOAs
## Show me all 'customers_name' where 'doa' is '1'
options = {
    'cat' : 'customers_name',
    'tit': 'RMAs by DOA',
    'xaxis_tit' : 'DOA',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['customers_name'], cat='doa', cat_val='1')
# dp.by_category(df, **options)
# dp.by_cat_day(df, **options)

# DOAs by customers_name CANCOM GMBH
## Show me when 'doa' were sent where 'customers_name' is CANCOM GMBH
options = {
    'cat' : 'doa',
    'tit': 'RMAs by DOA CANCOM GMBH',
    'xaxis_tit' : 'DOA CANCOM GMBH',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['doa'], cat='customers_name', cat_val='CANCOM GMBH',cat2='doa', cat2_val='1')
# # # dp.by_category(df, **options)
# dp.by_cat_day(df, **options)

## Show me all 'doa'  where 'customers_name' is CANCOM GMBH
options = {
    'cat' : 'catalog',
    'tit': 'Catalog DOA CANCOM GMBH',
    'xaxis_tit' : 'DOA CANCOM GMBH',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['catalog', 'doa'], cat='customers_name', cat_val='CANCOM GMBH',cat2='doa', cat2_val='1')
# dp.by_category(df, **options)
# dp.by_cat_day(df, **options)

# NFF by customers_name Bynet
## Show me all 'nff' where 'customers_name' is BYNET
## Show me when 'nff' were sent where  'customers_name' is BYNET
options = {
    'cat' : 'nff',
    'tit': 'RMAs by NFF Bynet',
    'xaxis_tit' : 'NFF Bynet',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['nff'], cat='customers_name', cat_val='BYNET', cat2='nff', cat2_val='1')
# # dp.by_category(df, **options)
# dp.by_cat_day(df, **options)

## what kinds of repair_types were shipped product_line ETX-203AX
## Show me all 'repair_types' where 'product_line' is ETX-203AX
options = {
    'cat' : 'repair_types',
    'tit': 'RMAs by repair_types of ETX-203AX',
    'xaxis_tit' : 'repair_types',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['repair_types'], cat='product_line', cat_val="ETX-203AX")
# dp.by_category(df, **options)

##  kinds of repair_types
## Show me all 'repair_types'
options = {
    'cat' : 'repair_types',
    'tit': 'RMAs by repair_types',
    'xaxis_tit' : 'repair_types',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['repair_types'])
# dp.by_category(df, **options)

#  which components replaced more
## Show me all 'rad_part'
options = {
    'cat' : 'rad_part',
    'tit': 'RMAs by Components',
    'xaxis_tit' : 'Components',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['rad_part'])
# dp.by_category(df, **options)

##  Non Repairable
## Show me all ???  where 'repair_types' is 'Non Repairable'
## ??? Show me when 'repair_types' is 'Non Repairable'
### Show me when 'nff' were sent where  'customers_name' is BYNET
options = {
    'cat' : 'repair_types',
    'tit': 'Non Repairable',
    'xaxis_tit' : 'Non Repairable',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['repair_types'], cat='repair_types', cat_val='Non Repairable')
# # dp.by_category(df, **options)
# dp.by_cat_day(df, **options)

##  Non Repairable units per customer
## Show me all 'customer_names' where 'repair_types' is 'Non Repairable'
# returned = 'repair_types'
options = {
    'cat' : 'customers_name',
    'tit': 'Non Repairable units per customer',
    'xaxis_tit' : 'Customer',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['customers_name'], cat='repair_types', cat_val='Non Repairable')
# dp.by_category(df, **options)

##  Non Repairable units per "catalog"
## Show me all 'catalog' where 'repair_types' is 'Non Repairable'
options = {
    'cat' : 'catalog',
    'tit': 'Non Repairable units per catalog',
    'xaxis_tit' : 'Catalog',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['catalog'], cat='repair_types', cat_val='Non Repairable')
# dp.by_category(df, **options)


## which location (reference) is problematic in product_line ETX-203AX
## Show me all location where 'product_line' is ETX-203AX
options = {
    'cat' : 'location',
    'tit': 'RMAs by Reference of ETX-203AX',
    'xaxis_tit' : 'Reference',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
    'drill_plot_only' : False,
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['location'], cat='product_line', cat_val='ETX-203AX')
# dp.by_category(df, **options)

## 1. show me when and how many RMAs were opened
options = {
    'cat' : 'form_number',
    'tit': 'Total RMAs',
    'xaxis_tit' : 'RMAs',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['form_number'])
# # # dp.by_category(df, **options)
# dp.by_cat_day(df, **options)

## 2.1 Show me when and how many product_line=ETX-203AX were sent
options = {
    'cat' : 'product_line',
    'tit': 'RMAs of ETX-203AX',
    'xaxis_tit' : 'Reference',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['product_line'], cat='product_line', cat_val=['ETX-203AX'])
# # dp.by_category(df, **options)
# dp.by_cat_day(df, **options)

## 2.1 Show me when and how many product_line=ETX-2i-100G were sent
options = {
    'cat' : 'product_line',
    'tit': 'RMAs of ETX-2i-100G',
    'xaxis_tit' : 'Reference',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
    'drill_plot_only' : False,
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['product_line'], cat='product_line', cat_val=['ETX-2i-100G'])
# dp.by_category(df, **options)
# dp.by_cat_day(df, **options)

## 2.2 Show me when and how many product_line=ETX-203AX and ETX-2i-100G were sent
options = {
    'cat' : 'product_line',
    'tit': 'RMAs of ETX-203AX and ETX-2i-100G',
    'xaxis_tit' : 'Reference',
    'yaxis_tit' : 'Quantity',
    'chart_type' : 'bar',
    #'group_by': 'ddd',
    'drill_plot_only' : False,
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['product_line'], cat='product_line', cat_val=['ETX-203AX', 'ETX-2i-100G'])
# # dp.by_category(df, **options)
# dp.by_cat_day(df, **options)

# options = {
#     'cat' : 'product_line',
#     'tit': 'RMAss of ETX-203AX',
#     'xaxis_tit' : 'Reference',
#     'yaxis_tit' : 'Quantity',
#     'chart_type' : 'bar',
#     'group_by': 'week'
# }
# df = sql.read_table_with_aggrigation(
#     'RMA', date_from, date_upto, ret_cat=['product_line'], cat='product_line', cat_val=['ETX-203AX', 'ETX-2i-100G'], group_by='week'
# )
# # dp.by_category(df, **options)
# dp.by_cat_day(df, **options)


## 4.1 Show me all 'product_line'
options = {
    'cat' : 'product_line',
    'tit': 'RMAs by all Product Line',
    'xaxis_tit' : 'Product Line',
    'yaxis_tit' : 'Quantity',
    'chart_type' : ['pie', 'bar'],
    'excludes' : None,
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['product_line'])
# dp.by_category(df, **options)


options = {
    'cat' : 'product_line',
    'tit': 'RMAs by Product Line',
    'xaxis_tit' : 'Product Line',
    'yaxis_tit' : 'Quantity',
    'chart_type' : ['pie', 'bar'],
    'excludes' : 'Component, SFP',
    'drill_plot_only' : False,
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['product_line'], excludes=['Component', 'SFP'])
# dp.by_category(df, **options)

## 4.2 Show me all 'customers_name'
options = {
    'cat' : 'customers_name',
    'tit': 'RMAs by Customer',
    'xaxis_tit' : 'Customer',
    'yaxis_tit' : 'Quantity',
    'chart_type' : ['pie', 'bar'],
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['customers_name'])
# dp.by_category(df, **options)


## 5.1 Show me all 'rad_part'
options = {
    'cat' : 'rad_part',
    'tit': 'RMAs by rad_part',
    'xaxis_tit' : 'rad_part',
    'yaxis_tit' : 'Quantity',
    'chart_type' : ['bar'],

}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['rad_part'])
# dp.by_category(df, **options)

## 5.2 Show me all 'rad_part' where 'product_line' is 'ETX-2i-10G'
options = {
    'cat' : 'rad_part',
    'tit': 'RMAs by rad_part for product_line ETX-2i-10G',
    'xaxis_tit' : 'rad_part',
    'yaxis_tit' : 'Quantity',
    'chart_type' : ['bar'],

}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['rad_part'], cat='product_line', cat_val='ETX-2i-10G')
# dp.by_category(df, **options)

## 5.3 Show me all 'date_code' where 'rad_part' is 'C-06030C226MATJ'
options = {
    'cat' : 'date_code',
    'tit': 'RMAs by date_code for C-06030C226MATJ',
    'xaxis_tit' : 'Date Codes',
    'yaxis_tit' : 'Quantity',
    'chart_type' : ['bar'],

}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['date_code'], cat='rad_part', cat_val='C-06030C226MATJ')
# dp.by_category(df, **options)



## 6.1 Show me all 'location'
options = {
    'cat' : 'location',
    'tit': 'RMAs by References',
    'xaxis_tit' : 'Reference',
    'yaxis_tit' : 'Quantity',
    'chart_type' : ['bar'],

}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['location'])
# dp.by_category(df, **options)

## 6.2 Show me all 'catalog' where 'location' is 'MH'
options = {
    'cat' : 'catalog',
    'tit': 'RMAs by catalog for location MH',
    'xaxis_tit' : 'catalog',
    'yaxis_tit' : 'Quantity',
    'chart_type' : ['bar'],

}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['catalog'], cat='location', cat_val='MH')
# dp.by_category(df, **options)

## 6.3 Show me all 'product_line' where 'location' is 'MH'
options = {
    'cat' : 'product_line',
    'tit': 'RMAs by Product Line for Refference MH',
    'xaxis_tit' : 'Product Line',
    'yaxis_tit' : 'Quantity',
    'chart_type' : ['bar'],

}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['product_line'], cat='location', cat_val='MH')
# dp.by_category(df, **options)



## 7.2.1 Show me all 'customers_name' which sent 'nff'
options = {
    'cat' : 'customers_name',
    'tit': 'NFF by customer',
    'xaxis_tit' : 'Customer',
    'yaxis_tit' : 'Quantity',
    'chart_type' : ['bar', 'pie'],
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['customers_name'], cat='nff', cat_val='1')
# dp.by_category(df, **options)

## 7.2.2 Show me all 'catalog' which sent 'nff'
options = {
    'cat' : 'catalog',
    'tit': 'NFF by Catalog',
    'xaxis_tit' : 'Catalog',
    'yaxis_tit' : 'Quantity',
    'chart_type' : ['bar'],
}
# df = sql.read_table('RMA', date_from, date_upto, ret_cat=['catalog'], cat='nff', cat_val='1')
# dp.by_category(df, **options)