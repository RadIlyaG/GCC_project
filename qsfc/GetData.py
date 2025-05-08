import ssl
import requests
#import json
#import certifi

import plotly.graph_objects as go
import plotly.io as pio
from collections import Counter, defaultdict
from datetime import date, timedelta, datetime

from ReadQsfc_WriteLocDb import Qsfc
from sql_db_rw import SqliteDB



class DrawPlot:
    def __init__(self):
        self.title_date_format = '%d %b %Y'
        self.strptime_format = "%Y-%m-%d %H:%M:%S.%f"

    def parse_date_from_str_into_datetime(self):
        for row in self.data:
            if isinstance(row['open_date'], str):
                #print('1', row['open_date'], type(row['open_date']))
                row['open_date'] = datetime.strptime(row['open_date'], self.strptime_format)
                #print('2', row['open_date'], type(row['open_date']))

    def by_day(self, data):
        self.data = data
        # Parse str into datetime
        self.parse_date_from_str_into_datetime()

        # for row in self.data:
        #     print('1a',row['open_date'], type(row['open_date']))
        #     row['open_date'] = datetime.strptime(row['open_date'], self.strptime_format)
        #     print('2a',row['open_date'], type(row['open_date']))
        by_day = Counter(row['open_date'].date() for row in self.data)

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
    def by_string(self, data, field_str, tit, xaxis_tit, yaxis_tit, **kwargs):
        self.data = data
        # count how manu times each name is appearing
        by_field_str = Counter(row[field_str] for row in self.data)
        ## ascending sort by number of records
        sorted_field_str_asc = sorted(by_field_str.items(), key=lambda x: x[1])
        names = [x[0] for x in sorted_field_str_asc]
        counts = [x[1] for x in sorted_field_str_asc]

        # dates_only = [
        #     datetime.strptime(row['open_date'], '%Y-%m-%d %H:%M:%S.%f').date()
        #     for row in self.data
        # ]
        self.parse_date_from_str_into_datetime()

        dates_only = []
        for row in self.data:
            dates_only.append(row['open_date'])
            # if isinstance(row['open_date'], str):
            #     dates_only.append(datetime.strptime(row['open_date'], self.strptime_format).date())
            # else:
            #     dates_only.append(row['open_date'])

        date_from = min(dates_only)
        date_to = max(dates_only)
        #date_from.strftime('%d.%m.%Y')
        #date_to.strftime('%d.%m.%Y')
        if date_from != date_to:
            titl = f"{tit} {date_from.strftime(self.title_date_format)} — {date_to.strftime(self.title_date_format)}"
        else:
            titl = f"{tit} {date_from.strftime(self.title_date_format)}"

        figures = {}

        fig_bar = go.Figure(go.Bar(x=counts, y=names, orientation='h'))
        figures['bar'] = fig_bar
        fig_bar.update_layout(title=titl,
                          xaxis_title=xaxis_tit,
                          yaxis_title=yaxis_tit)
        #fig.show()
        pio.write_html(fig_bar, file=f'c:/temp/{tit}.bar.html', auto_open=True)

        customer_counts = Counter(row[field_str] for row in data)
        fig_pie = go.Figure(data=[
            go.Pie(labels=list(customer_counts.keys()), values=list(customer_counts.values()), hole=0)
        ])
        figures['pie'] = fig_pie

        fig_pie.update_layout(title=titl)
        #fig.show()
        pio.write_html(fig_pie, file=f'c:/temp/{tit}.pie.html', auto_open=True)

        if 'chart_type' in kwargs:
            print (kwargs['chart_type'])
            return figures[kwargs['chart_type']]
        else:
            return fig_bar

    def by_customer_day(self, data):
        self.data = data
        # Parse str into datetime
        self.parse_date_from_str_into_datetime()
        # for row in data:
        #     if isinstance(row['open_date'], str):
        #       row['open_date'] = datetime.strptime(row['open_date'], "%Y-%m-%d %H:%M:%S.%f")
        #
        # Range for filter ??
        # date_from = datetime(2000, 2, 1)
        # date_to = datetime(3025, 2, 13)
        # # Filter by date??
        # filtered_data = [
        #     row for row in data
        #     if date_from.date() <= row['open_date'].date() <= date_to.date()
        # ]

        # Grouping: (date, name) → counter
        daily_counts = defaultdict(int)
        # for row in filtered_data:
        #     pass
        for row in data:
            date = row['open_date'].date()
            name = row['customers_full_name']
            daily_counts[(date, name)] += 1

        # Preparing data: dict {name: {date: count}}
        client_day_map = defaultdict(lambda: defaultdict(int))
        for (date, name), count in daily_counts.items():
            client_day_map[name][date] = count

        # Take dates(axis X)
        all_dates = sorted({row['open_date'].date() for row in data})
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
        date_obj = datetime.strptime(row['open_date'], '%Y-%m-%d %H:%M:%S.%f')
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
    list_of_dicts = qsfc.get_data_from_qsfc('RMA', date_from, today_date_string)


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
    #dp = DrawPlot()
    #dp.by_day(list_of_dicts)
    dp = DrawPlot()
    #dp.by_string(list_of_dicts, 'reporter_name', 'RMAs by Reporter Name', 'Quantity', 'Reporter')
    #dp.by_string(list_of_dicts, 'tested_catalog', 'Prod by tested_catalog', 'Quantity', 'cat')
    #dp.by_string(list_of_dicts, 'tested_catalog', 'RMAs by catalog', 'Quantity', 'Catalog')
    dp.by_string(list_of_dicts, 'customers_name', 'RMAs by customer', 'Quantity', 'Customer')
    #dp.by_customer_day(list_of_dicts)

    # DrawPlot_byDay(list_of_dicts)
    #DrawPlot_byCustomer(list_of_dicts)
    # DrawPlot_byCustomerDay(list_of_dicts)
    # DrawPlot_byCatalog(list_of_dicts)
    #DrawPlot_byString(list_of_dicts, 'customers_full_name', 'RMAs by customer', 'Quantity', 'Customer')
    #DrawPlot_byString(list_of_dicts, 'catalog', 'RMAs by catalog', 'Quantity', 'Catalog')
    #DrawPlot_byString(list_of_dicts, 'reporter_name', 'RMAs by Reporter Name', 'Quantity', 'Reporter')
    #__DrawPlot_byCat(list_of_dicts)

    tbl = SqliteDB()
    tbl.fill_table('RMA', list_of_dicts)

    #import qsfc_dd
    #qsfc_dd.app.run(debug=True)