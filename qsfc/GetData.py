#import ssl
#import requests
#import json
#import certifi

# import plotly.graph_objects as go
# import plotly.io as pio
# from collections import Counter, defaultdict
from datetime import date, timedelta, datetime

from ReadQsfc_WriteLocDb import Qsfc
from sql_db_rw import SqliteDB
from Graphs import DrawPlot






if __name__ == '__main__':
    #https://ws-proxy01.rad.com:8445/ATE_WS/ws/rest/RMAReportQSFC?dateFrom=13/02/2025&dateTo=13/02/2025
    #https://ws-proxy01.rad.com:8445/ATE_WS/ws/rest/ProdReportQSFC?dateFrom=02/04/2024&dateTo=09/04/2024
    qsfc = Qsfc()
    qsfc.print_rtext = True
    res_list =[]
    #list_of_dicts = qsfc.get_data_from_qsfc('RMA', "13/02/2025", "13/02/2025")
    #for row in list_of_dicts:
    #    if row['reporter_name'] == "":
    #        row['reporter_name'] = "No name reported"
            # print('2', row['open_date'], type(row['open_date']))
    #print(list_of_dicts[0].keys())

    #list_of_dicts = qsfc.get_data_from_qsfc('RMA', "13/01/2025", "13/02/2025")
    date_from = str((date.today() - timedelta(days=30)).strftime("%d/%m/%Y"),)
    today_date_string = date.today().strftime('%d/%m/%Y')
    # date_from = '08/04/2025'
    # today_date_string = '12/04/2025'
    list_of_dicts = qsfc.get_data_from_qsfc('RMA', date_from, today_date_string)
    print('dd',  list_of_dicts, list_of_dicts[0])
    if list_of_dicts[0] is False:
        print ('ee', list_of_dicts[1])
    else:
        print(f'len of list:{len(list_of_dicts)}')
        for dicti in list_of_dicts:
            print(dicti)
            #for key, volume in dicti.items():
            #    print(key, volume)

            # if dicti['reporter_name']=='YEHOSHAFAT RAZIEL':
            #     pass; #res_list.append(dicti)
            # if re.search('ETX-220A', dicti['catalog']):
            #     pass; #res_list.append(dicti)

            # if dicti['reporter_name']=='YEHOSHAFAT RAZIEL' and not re.search('ETX-220A', dicti['catalog']):
            #     pass; #res_list.append(dicti)
            #     #print(dicti)

        # print(f'len of res_list:{len(res_list)}')
        # for dicti in res_list:
        #     print(dicti)

        #stri = input()
        #dp = DrawPlot()
        #dp.by_day(list_of_dicts)
        dp = DrawPlot()
        #dp.by_string(list_of_dicts, 'reporter_name', 'RMAs by Reporter Name', 'Quantity', 'Reporter')
        #dp.by_string(list_of_dicts, 'tested_catalog', 'Prod by tested_catalog', 'Quantity', 'cat')
        #dp.by_string(list_of_dicts, 'catalog', 'RMAs by catalog', 'Quantity', 'Catalog')
        dp.by_string(list_of_dicts, 'customers_name', 'RMAs by customer', 'Quantity', 'Customer')
        dp.by_customer_day(list_of_dicts)
        #dp.by_day(list_of_dicts)

        # DrawPlot_byDay(list_of_dicts)
        #DrawPlot_byCustomer(list_of_dicts)
        # DrawPlot_byCustomerDay(list_of_dicts)
        # DrawPlot_byCatalog(list_of_dicts)
        #DrawPlot_byString(list_of_dicts, 'customers_full_name', 'RMAs by customer', 'Quantity', 'Customer')
        #DrawPlot_byString(list_of_dicts, 'catalog', 'RMAs by catalog', 'Quantity', 'Catalog')
        #DrawPlot_byString(list_of_dicts, 'reporter_name', 'RMAs by Reporter Name', 'Quantity', 'Reporter')
        #__DrawPlot_byCat(list_of_dicts)

        #tbl = SqliteDB()
        #tbl.fill_table('RMA', list_of_dicts)

        #import qsfc_dd
        #qsfc_dd.app.run(debug=True)