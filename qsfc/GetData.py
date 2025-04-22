import ssl
import socket
import requests
import json
import certifi
import urllib3
import urllib.parse
import re
## need panda import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from collections import Counter, defaultdict
from datetime import datetime
import sqlite3


class Qsfc:
    def __init__(self):
        self.headers = {'Authorization': 'Basic d2Vic2VydmljZXM6cmFkZXh0ZXJuYWw='}
        self.hostname = 'ws-proxy01.rad.com'
        self.port = '8445'
        self.path = '/ATE_WS/ws/rest/'
        self.data_obj = {}

    def connect(self):
        url = 'https://'

        # context = ssl.create_default_context()
        url += self.hostname + ':' + self.port + self.path
        try:
           with socket.create_connection((self.hostname, self.port)):
               # print(f'connect url:{url}')
               return True, url
        except Exception as e:
           return False, {f'Failed to connect to {self.hostname}:{self.port}, {e}'}

    def get_data_cert(self, qry_type):
        print(f'get_data_cert {self.url}')
        data = {}
        err_msg = {f"Fail to get data from QSFC"}
        http = urllib3.PoolManager(
            cert_reqs="CERT_REQUIRED",
            ca_certs=certifi.where()
        )

        resp = http.request('GET', self.url, headers=self.headers)
        print(f'resp.status:{resp.status}')
        if resp.status != 200:
            return False, err_msg

        if self.print_rtext:
            pass; #print(f'r.data:<{resp.data.decode()}>')

        #if self.print_rtext:
        #    print(f'r.text:<{data}>')
        #data = resp.json()
        data = json.loads(resp.data)
        #return data

        inside_data = data[f'{qry_type}ReportQSFC']
        #print(f'type(inside_data):{type(inside_data)} inside_data:{inside_data}')
        # # print(f'inside_data:{inside_data} type(inside_data):{type(inside_data)} len(inside_data):{len(inside_data)}')
        # if len(inside_data) == 0:
        #     return False, err_msg
        # else:
        #     if 'null' in inside_data[0].values():
        #         return False, err_msg
        #     return True, inside_data[0]
        return inside_data


    def get_data_from_qsfc(self, qry_type, dateFrom, dateTo):
        partial_url = qry_type + 'ReportQSFC' + '?dateFrom=' + dateFrom + '&dateTo=' + dateTo
        res, url = self.connect()
        if res:
            self.url = url + partial_url
            res = self.get_data_cert(qry_type)
            #print(f'type(res):{type(res)} res:{res}')
            return res
        else:
            return False, url

class DrawPlot:
    def __init__(self):
        self.title_date_format = '%d %b %Y'
        self.strptime_format = "%Y-%m-%d %H:%M:%S.%f"

    def parse_date_from_str_into_datetime(self):
        for row in self.data:
            if isinstance(row['rma_open_date'], str):
                #print('1', row['rma_open_date'], type(row['rma_open_date']))
                row['rma_open_date'] = datetime.strptime(row['rma_open_date'], self.strptime_format)
                #print('2', row['rma_open_date'], type(row['rma_open_date']))

    def by_day(self, data):
        self.data = data
        # Parse str into datetime
        self.parse_date_from_str_into_datetime()

        # for row in self.data:
        #     print('1a',row['rma_open_date'], type(row['rma_open_date']))
        #     row['rma_open_date'] = datetime.strptime(row['rma_open_date'], self.strptime_format)
        #     print('2a',row['rma_open_date'], type(row['rma_open_date']))
        by_day = Counter(row['rma_open_date'].date() for row in self.data)

        # Convert to sorted lists for graph
        dates = sorted(by_day.keys())
        counts = [by_day[d] for d in dates]

        tit = 'Open RMAs per Date'
        date_from = min(dates)
        date_to = max(dates)
        if date_from != date_to:
            titl = f"{tit} from {date_from.strftime(self.title_date_format)} upto {date_to.strftime(self.title_date_format)}"
        else:
            titl = f"{tit} {date_from.strftime(self.title_date_format)}"

        # Build graph
        fig = go.Figure(data=go.Scatter(x=dates, y=counts, mode='lines+markers'))

        fig.update_layout(title=titl, xaxis_title='Date', yaxis_title='Quantity')
        pio.write_html(fig, file=f'c:/temp/{tit}.sca.html', auto_open=True)
        #fig.show()

        fig = go.Figure(go.Bar(x=dates, y=counts, orientation='v'))
        fig.update_layout(title=titl,
                          xaxis_title='Date',
                          yaxis_title='Quantity')
        pio.write_html(fig, file=f'c:/temp/{tit}.bar.html', auto_open=True)

    ##  field_str 'customers_full_name'
    ##  tit 'RMAs by customer'
    ##  xaxis_tit 'Quantity'
    ##  yaxis_tit 'Customer'
    def by_string(self, data, field_str, tit, xaxis_tit, yaxis_tit):
        self.data = data
        # count how manu times each name is appearing
        by_field_str = Counter(row[field_str] for row in self.data)
        ## ascending sort by number of records
        sorted_field_str_asc = sorted(by_field_str.items(), key=lambda x: x[1])
        names = [x[0] for x in sorted_field_str_asc]
        counts = [x[1] for x in sorted_field_str_asc]

        # dates_only = [
        #     datetime.strptime(row['rma_open_date'], '%Y-%m-%d %H:%M:%S.%f').date()
        #     for row in self.data
        # ]
        self.parse_date_from_str_into_datetime()

        dates_only = []
        for row in self.data:
            dates_only.append(row['rma_open_date'])
            # if isinstance(row['rma_open_date'], str):
            #     dates_only.append(datetime.strptime(row['rma_open_date'], self.strptime_format).date())
            # else:
            #     dates_only.append(row['rma_open_date'])

        date_from = min(dates_only)
        date_to = max(dates_only)
        #date_from.strftime('%d.%m.%Y')
        #date_to.strftime('%d.%m.%Y')
        if date_from != date_to:
            titl = f"{tit} {date_from.strftime(self.title_date_format)} — {date_to.strftime(self.title_date_format)}"
        else:
            titl = f"{tit} {date_from.strftime(self.title_date_format)}"

        fig = go.Figure(go.Bar(x=counts, y=names, orientation='h'))
        fig.update_layout(title=titl,
                          xaxis_title=xaxis_tit,
                          yaxis_title=yaxis_tit)
        #fig.show()
        pio.write_html(fig, file=f'c:/temp/{tit}.bar.html', auto_open=True)

        customer_counts = Counter(row[field_str] for row in data)
        fig = go.Figure(data=[
            go.Pie(labels=list(customer_counts.keys()), values=list(customer_counts.values()), hole=0)
        ])

        fig.update_layout(title=titl)
        #fig.show()
        pio.write_html(fig, file=f'c:/temp/{tit}.pie.html', auto_open=True)

    def by_customer_day(self, data):
        self.data = data
        # Parse str into datetime
        self.parse_date_from_str_into_datetime()
        # for row in data:
        #     if isinstance(row['rma_open_date'], str):
        #       row['rma_open_date'] = datetime.strptime(row['rma_open_date'], "%Y-%m-%d %H:%M:%S.%f")
        #
        # Range for filter ??
        # date_from = datetime(2000, 2, 1)
        # date_to = datetime(3025, 2, 13)
        # # Filter by date??
        # filtered_data = [
        #     row for row in data
        #     if date_from.date() <= row['rma_open_date'].date() <= date_to.date()
        # ]

        # Grouping: (date, name) → counter
        daily_counts = defaultdict(int)
        # for row in filtered_data:
        #     pass
        for row in data:
            date = row['rma_open_date'].date()
            name = row['customers_full_name']
            daily_counts[(date, name)] += 1

        # Preparing data: dict {name: {date: count}}
        client_day_map = defaultdict(lambda: defaultdict(int))
        for (date, name), count in daily_counts.items():
            client_day_map[name][date] = count

        # Take dates(axis X)
        all_dates = sorted({row['rma_open_date'].date() for row in data})
        date_from = min(all_dates)
        date_to = max(all_dates)
        # Build graph
        fig_sca = go.Figure()
        fig_bar = go.Figure()

        for client, date_counts in client_day_map.items():
            y_values = [date_counts.get(d, 0) for d in all_dates]
            text_labels = [f"{client}: {v}" for v in y_values]
            fig_sca.add_trace(go.Scatter(x=all_dates, y=y_values, mode='lines+markers', name=client))
            fig_bar.add_trace(go.Bar(name=client, x=all_dates, y=y_values, text = y_values, orientation='v'))
            ## , text = text_labels, textposition='inside', textfont=dict(size=22)

        tit = 'RMAs per Date and Client'
        if date_from != date_to:
            titl = f"{tit} {date_from.strftime(self.title_date_format)} — {date_to.strftime(self.title_date_format)}"
        else:
            titl = f"{tit} {date_from.strftime(self.title_date_format)}"
        fig_sca.update_layout(title=titl,
                          xaxis_title='Date',
                          yaxis_title='Quantity',
                          legend_title='Client')
        fig_bar.update_layout(
            barmode='stack', #'group' stack
            title=titl,
            xaxis_title='Date',
            yaxis_title='Quantity'
        )
        ## not fine pio.write_html(fig_sca, file=f'c:/temp/{tit}.sca.html', auto_open=True)
        pio.write_html(fig_bar, file=f'c:/temp/{tit}.bar.html', auto_open=True)


def _DrawPlot_byCustomer(data):
    # count how manu times each name is appearing
    by_customer = Counter(row['customers_full_name'] for row in data)
    # Sort in descending order
    # sorted_customers = by_customer.most_common()
    ## ascending sort by number of records
    sorted_customers_asc = sorted(by_customer.items(), key=lambda x: x[1])
    # names = list(by_customer.keys())
    # counts = list(by_customer.values())
    names = [x[0] for x in sorted_customers_asc]
    counts = [x[1] for x in sorted_customers_asc]
    fig = go.Figure(go.Bar(x=counts, y=names, orientation='h'))
    fig.update_layout(title='RMAs by customer',
                      xaxis_title='Quantity',
                      yaxis_title='Customer')
    fig.show()

    customer_counts = Counter(row['customers_full_name'] for row in data)
    fig = go.Figure(data=[
        go.Pie(labels=list(customer_counts.keys()), values=list(customer_counts.values()), hole=0)
    ])

    fig.update_layout(title='Distribution by customer')
    fig.show()

def _DrawPlot_byCatalog(data):
    # count how manu times each name is appearing
    by_catalog = Counter(row['catalog'] for row in data)
    # Sort in descending order
    # sorted_customers = by_customer.most_common()

    ## ascending sort by number of records
    sorted_catalogs_asc = sorted(by_catalog.items(), key=lambda x: x[1])
    # names = list(by_customer.keys())
    # counts = list(by_customer.values())
    names = [x[0] for x in sorted_catalogs_asc]
    counts = [x[1] for x in sorted_catalogs_asc]
    fig = go.Figure(go.Bar(x=counts, y=names, orientation='h'))
    fig.update_layout(title='RMAs per Catalog',
                      xaxis_title='Quantity',
                      yaxis_title='Catalogs')
    fig.show()


def _DrawPlot_byCat(data):

    # Суммируем значения по дате
    daily_sums = defaultdict(float)

    for row in data:
        # преобразуем дату
        date_obj = datetime.strptime(row['rma_open_date'], '%Y-%m-%d %H:%M:%S.%f')
        day_str = date_obj.date().isoformat()  # '2025-02-14'

        # Суммируем по нужному полю, например 'total'
        daily_sums[day_str] += float(row['rfh_id'])  # замените 'total' на нужный ключ

    # Сортируем по дате
    sorted_items = sorted(daily_sums.items())
    dates = [item[0] for item in sorted_items]
    totals = [item[1] for item in sorted_items]

    # Строим график
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=totals, mode='lines+markers', name='Сумма'))

    fig.update_layout(
        title='Сумма по дням',
        xaxis_title='Дата',
        yaxis_title='Сумма',
        xaxis=dict(type='category'),
    )

    fig.show()


class SqliteDB:
    def __init__(self):
        self.db = 'db.db'

    def fill_table(self, qry_type, data):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        columns = list(data[0].keys())
        columns_def = ", ".join([f"{col} TEXT" for col in columns])
        cursor.execute(f"DROP TABLE IF EXISTS {qry_type};")
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {qry_type} ({columns_def})")
        # Динамически вставляем данные
        placeholders = ", ".join(["?" for _ in columns])
        insert_sql = f"INSERT INTO {qry_type} ({', '.join(columns)}) VALUES ({placeholders})"
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






if __name__ == '__main__':
    #https://ws-proxy01.rad.com:8445/ATE_WS/ws/rest/RMAReportQSFC?dateFrom=13/02/2025&dateTo=13/02/2025
    #https://ws-proxy01.rad.com:8445/ATE_WS/ws/rest/ProdReportQSFC?dateFrom=02/04/2024&dateTo=09/04/2024
    qsfc = Qsfc()
    qsfc.print_rtext = True
    res_list =[]
    list_of_dicts = qsfc.get_data_from_qsfc('RMA', "02/01/2025", "03/02/2025")
    #print(list_of_dicts[0].keys())
    #list_of_dicts = qsfc.get_data_from_qsfc('Prod', "13/01/2025", "13/02/2025")
    #print(f'len of list:{len(list_of_dicts)}')
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
    dp = DrawPlot()
    #dp.by_day(list_of_dicts)
    #dp = DrawPlot()
    #dp.by_string(list_of_dicts, 'reporter_name', 'RMAs by Reporter Name', 'Quantity', 'Reporter')
    #dp.by_string(list_of_dicts, 'catalog', 'RMAs by catalog', 'Quantity', 'Catalog')
    #dp.by_string(list_of_dicts, 'customers_full_name', 'RMAs by customer', 'Quantity', 'Customer')
    dp.by_customer_day(list_of_dicts)
    # DrawPlot_byDay(list_of_dicts)
    #DrawPlot_byCustomer(list_of_dicts)
    # DrawPlot_byCustomerDay(list_of_dicts)
    # DrawPlot_byCatalog(list_of_dicts)
    #DrawPlot_byString(list_of_dicts, 'customers_full_name', 'RMAs by customer', 'Quantity', 'Customer')
    #DrawPlot_byString(list_of_dicts, 'catalog', 'RMAs by catalog', 'Quantity', 'Catalog')
    #DrawPlot_byString(list_of_dicts, 'reporter_name', 'RMAs by Reporter Name', 'Quantity', 'Reporter')
    #__DrawPlot_byCat(list_of_dicts)

    # tbl = SqliteDB()
    # tbl.fill_table('RMA', list_of_dicts)