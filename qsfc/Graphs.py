import plotly.graph_objects as go
import plotly.io as pio
from collections import Counter, defaultdict
from datetime import date, timedelta, datetime



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

    '''
    kwargs['cat']     :  fields of DB (product_line, catalog, customer_name, ...)
    kwargs['subcat']  :  one value of cat. if cat==product_line then subcat may be ETX-203AX or SecFlow-1p or MP-DATA Modules
    kwargs['cat2'] :  an additional field we cat filter the cat. if cat==product_line and subcat is ETX-203AX,
                         then subcat2 may be location (for Reference U3, D1..) or rma_kind_desc
    '''
    def ne_by_str_cat_subcat(self, data, **kwargs):
        self.data = data
        field_str = kwargs['cat']
        # count how manu times each name is appearing
        if kwargs['subcat']:
            by_field_str = Counter(row[kwargs['subcat2']] for row in self.data if row[field_str] == kwargs['subcat'])
        else:
            if kwargs['subcat2']:
                by_field_str = Counter(row[kwargs['cat']] for row in self.data  if row[kwargs['subcat2']] == '1')
            else:
                by_field_str = Counter(row[kwargs['cat']] for row in self.data)
        print(by_field_str)
        ## ascending sort by number of records
        sorted_field_str_asc = sorted(by_field_str.items(), key=lambda x: x[1])
        names = [x[0] if x[0] != '' else 'not processed' for x in sorted_field_str_asc]
        if kwargs['subcat2'] == 'doa' or kwargs['subcat2'] == 'nff':
            names = [kwargs['subcat2'].upper() if x == "1" else f"Not {kwargs['subcat2'].upper()}" if x == '0' else x for x in names]
        counts = [x[1] for x in sorted_field_str_asc]
        print(names, counts)

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

        tit = kwargs['tit']
        xaxis_tit = kwargs['xaxis_tit']
        yaxis_tit = kwargs['yaxis_tit']
        if date_from != date_to:
            titl = f"{tit} {date_from.strftime(self.title_date_format)} — {date_to.strftime(self.title_date_format)}"
        else:
            titl = f"{tit} {date_from.strftime(self.title_date_format)}"

        figures = {}

        fig_bar = go.Figure(go.Bar(x=names, y=counts, orientation='v'))
        figures['bar'] = fig_bar
        fig_bar.update_layout(title=titl,
                          xaxis_title=xaxis_tit,
                          yaxis_title=yaxis_tit)
        #fig.show()
        pio.write_html(fig_bar, file=f'c:/temp/{tit}.bar.html', auto_open=True)

        #customer_counts = Counter(row[field_str] for row in data)
        if kwargs['subcat']:
            customer_counts = Counter(row[kwargs['subcat2']] for row in self.data if row[field_str] == kwargs['subcat'])
        else:
            if kwargs['subcat2']:
                customer_counts = Counter(row[kwargs['subcat2']] for row in self.data)
            else:
                customer_counts = Counter(row[kwargs['cat']] for row in self.data)
        print('customer_counts', customer_counts)
        cc = {"not processed" if len(k) == 0 else k: v for k, v in customer_counts.items()}
        print('cc', cc)
        if kwargs['subcat2'] == 'doa' or kwargs['subcat2'] == 'nff':
            ccc = {f"Not {kwargs['subcat2'].upper()}" if k == "0" else 'not processed' if k == 'not processed' else f"{kwargs['subcat2'].upper()}": v for k, v in cc.items()}
        else:
            ccc = cc
        print('ccc', ccc)
        fig_pie = go.Figure(data=[
            go.Pie(labels=list(ccc.keys()), values=list(ccc.values()), hole=0)
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


    def by_str_cat_subcat(self, data, **kwargs):
        self.data = data
        print('kwargs: ', kwargs)
        field_str = kwargs['cat']
        # count how many times each name is appearing
        #
        if kwargs['subcat']:
            # 'cat': 'rad_part', 'subcat': 'PS-250/48-4U', 'cat2': 'date_code'
            #by_field_str = Counter(row[kwargs['cat2']] for row in self.data if row[field_str] == kwargs['subcat'])
            # если в строке в поле rad_part ('cat') записано 'PS-250/48-4U' ('subcat'),
            # то считаем какие и сколько раз есть строк с разными  'date_code' ('cat2')

            # if in rad_part ('cat') is written 'PS-250/48-4U' ('subcat') then
            # we count in how many rows each date_code ('cat2') of given 'subcat' is appearing
            # '': 31, '1812': 30, '.': 5, '1646': 2, '1402': 1,
            by_field_str = Counter(row[kwargs['cat2']] for row in self.data if row[kwargs['cat']] == kwargs['subcat'])
        else:
            # if there is no subcat
            if kwargs['cat2']:
                # if there is cat2 - product_line['cat'] None nff['cat2'] - we count how many times each product_line has nff
                # 'cat': 'rad_part', 'subcat': None, 'cat2': 'date_code'
                # 'cat': None, 'subcat': None, 'cat2': 'date_code'
                #  we count in how many rows each non-empty date_code is appearing
                by_field_str = Counter(row[kwargs['cat2']] for row in self.data if row[kwargs['cat2']] != '')
            else:
                # 'cat': 'rad_part', 'subcat': None, 'cat2': None
                # we count in how many rows each non-empty rad_part ('cat') is appearing :
                # '': 2070, 'LF-IC-NT5TU32M16CG-3CI/ETX': 171, 'PS-250/AC-4U': 108, ...
                by_field_str = Counter(row[kwargs['cat']] for row in self.data if row[kwargs['cat']] != '')
        print('by_field_str: ', by_field_str)
        ## ascending sort by number of records
        sorted_field_str_asc = sorted(by_field_str.items(), key=lambda x: x[1])

        names = [x[0] if x[0] != '' else 'not processed' for x in sorted_field_str_asc]
        if kwargs['cat2'] == 'doa' or kwargs['cat2'] == 'nff':
            names = [kwargs['cat2'].upper() if x == "1" else
                     f"Not {kwargs['cat2'].upper()}" if x == '0' else
                     x for x in names]
        counts = [x[1] for x in sorted_field_str_asc]
        summ = sum(counts)

        #print('names: ', names, '\ncounts: ', counts, 'summ: ', summ)

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

        tit = kwargs['tit']
        xaxis_tit = kwargs['xaxis_tit']
        yaxis_tit = kwargs['yaxis_tit']
        if date_from != date_to:
            titl = f"{tit} {date_from.strftime(self.title_date_format)} — {date_to.strftime(self.title_date_format)}"
        else:
            titl = f"{tit} {date_from.strftime(self.title_date_format)}"

        figures = {}

        fig_bar = go.Figure(go.Bar(x=names, y=counts, orientation='v', text=counts))
        figures['bar'] = fig_bar
        fig_bar.update_layout(title=f'{titl},\t\tTotal: {summ}',
                          xaxis_title=xaxis_tit,
                          yaxis_title=yaxis_tit)
        #fig.show()
        pio.write_html(fig_bar, file=f'c:/temp/{tit}.bar.html', auto_open=True)

        #customer_counts = Counter(row[field_str] for row in data)
        if kwargs['subcat']:
            customer_counts = Counter(row[kwargs['cat2']] for row in self.data if row[field_str] == kwargs['subcat'])
        else:
            # if there is no subcat
            if kwargs['cat2']:
                # if there is cat2 - product_line['cat'] None nff['cat2'] - we count how many times each product_line has nff
                customer_counts = Counter(row[kwargs['cat2']] for row in self.data)
            else:
                customer_counts = Counter(row[kwargs['cat']] for row in self.data)
        print('customer_counts', customer_counts)
        cc = {"not processed" if len(k) == 0 else k: v for k, v in customer_counts.items()}
        print('cc', cc)
        if kwargs['subcat'] and (kwargs['cat2'] == 'doa' or kwargs['cat2'] == 'nff'):
            ccc = {f"Not {kwargs['cat2'].upper()}" if k == "0" else
                   'not processed' if k == 'not processed' else
                   f"{kwargs['cat2'].upper()}": v for k, v in cc.items()}
        else:
            ccc = cc
        print('ccc', ccc)
        fig_pie = go.Figure(data=[
            go.Pie(labels=list(ccc.keys()), values=list(ccc.values()), hole=0)
        ])
        figures['pie'] = fig_pie

        fig_pie.update_layout(title=f'{titl},\t\tTotal: {summ}')
        #fig.show()
        pio.write_html(fig_pie, file=f'c:/temp/{tit}.pie.html', auto_open=True)

        if 'chart_type' in kwargs:
            print (kwargs['chart_type'])
            return figures[kwargs['chart_type']]
        else:
            return fig_bar


    def by_category(self, data, **kwargs):
        self.data = data
        print('kwargs: ', kwargs)

        for x in data[:10]:
            print(x)
        # field_str = kwargs['cat']
        # count how many times each name is appearing

        by_field_str = Counter(row[kwargs['cat']] for row in self.data if row[kwargs['cat']] != '')
        print('by_field_str: ', type(by_field_str), by_field_str)
        ## ascending sort by number of records
        sorted_field_str_asc = sorted(by_field_str.items(), key=lambda x: x[1])

        names = [x[0] if x[0] != '' else 'not processed' for x in sorted_field_str_asc]
        counts = [x[1] for x in sorted_field_str_asc]
        summ = sum(counts)

        #print('names: ', names, '\ncounts: ', counts, 'summ: ', summ)

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

        tit = kwargs['tit']
        xaxis_tit = kwargs['xaxis_tit']
        yaxis_tit = kwargs['yaxis_tit']
        if date_from != date_to:
            titl = f"{tit} {date_from.strftime(self.title_date_format)} — {date_to.strftime(self.title_date_format)}"
        else:
            titl = f"{tit} {date_from.strftime(self.title_date_format)}"

        figures = {}

        fig_bar = go.Figure(go.Bar(x=names, y=counts, orientation='v', text=counts))
        figures['bar'] = fig_bar
        fig_bar.update_layout(title=f'{titl},\t\tTotal: {summ}',
                          xaxis_title=xaxis_tit,
                          yaxis_title=yaxis_tit)
        #fig.show()
        pio.write_html(fig_bar, file=f'c:/temp/{tit}.bar.html', auto_open=True)

        customer_counts = Counter(row[kwargs['cat']] for row in self.data)
        #print('customer_counts', customer_counts)
        ccc = {"not processed" if len(k) == 0 else k: v for k, v in customer_counts.items()}
        #print('ccc', ccc)
        fig_pie = go.Figure(data=[
            go.Pie(labels=list(ccc.keys()), values=list(ccc.values()), hole=0)
        ])
        figures['pie'] = fig_pie

        fig_pie.update_layout(title=f'{titl},\t\tTotal: {summ}')
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
            name = row['customers_name']  #  'customers_full_name'
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

    def by_cat_day(self, data, cat):
        self.data = data
        # Parse str into datetime
        self.parse_date_from_str_into_datetime()

        # Grouping: (date, name) → counter
        daily_counts = defaultdict(int)
        # for row in filtered_data:
        #     pass
        for row in data:
            date = row['open_date'].date()
            name = row[cat]  #  'customers_full_name'
            daily_counts[(date, name)] += 1

        # Preparing data: dict {name: {date: count}}
        cat_day_map = defaultdict(lambda: defaultdict(int))
        for (date, name), count in daily_counts.items():
            cat_day_map[name][date] = count

        # Take dates(axis X)
        all_dates = sorted({row['open_date'].date() for row in data})
        date_from = min(all_dates)
        date_to = max(all_dates)
        # Build graph
        fig_sca = go.Figure()
        fig_bar = go.Figure()

        for cate, date_counts in cat_day_map.items():
            y_values = [date_counts.get(d, 0) for d in all_dates]
            text_labels = [f"{cate}: {v}" for v in y_values]
            fig_sca.add_trace(go.Scatter(x=all_dates, y=y_values, mode='lines+markers', name=cat))
            fig_bar.add_trace(go.Bar(name=cate, x=all_dates, y=y_values, text = y_values, orientation='v'))
            ## , text = text_labels, textposition='inside', textfont=dict(size=22)

        tit = f'RMAs per Date and {cat}'
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
        #pio.write_html(fig_bar, file=f'c:/temp/{tit}.bars.html', auto_open=True)

        fig_bar.update_layout(
            barmode='group',  # 'group' stack
            title=titl,
            xaxis_title='Date',
            yaxis_title='Quantity'
        )
        pio.write_html(fig_bar, file=f'c:/temp/{tit}.barg.html', auto_open=True)

    def by_subcat_day(self, data, cat, subcat):
        self.data = data
        # Parse str into datetime
        self.parse_date_from_str_into_datetime()

        # Grouping: (date, name) → counter
        daily_counts = defaultdict(int)
        # for row in filtered_data:
        #     pass
        for row in data:
            date = row['open_date'].date()
            name = row[cat]
            if name == subcat:
                daily_counts[(date, name)] += 1
                # print(date, name, daily_counts)

        # Preparing data: dict {name: {date: count}}
        cat_day_map = defaultdict(lambda: defaultdict(int))
        for (date, name), count in daily_counts.items():
            cat_day_map[name][date] = count

        # Take dates(axis X)
        all_dates = sorted({row['open_date'].date() for row in data})
        date_from = min(all_dates)
        date_to = max(all_dates)
        # Build graph
        fig_sca = go.Figure()
        fig_bar = go.Figure()

        for cate, date_counts in cat_day_map.items():
            y_values = [date_counts.get(d, 0) for d in all_dates]
            text_labels = [f"{cate}: {v}" for v in y_values]
            fig_sca.add_trace(go.Scatter(x=all_dates, y=y_values, mode='lines+markers', name=cat))
            fig_bar.add_trace(go.Bar(name=cate, x=all_dates, y=y_values, text = y_values, orientation='v'))
            ## , text = text_labels, textposition='inside', textfont=dict(size=22)

        tit = f'RMAs per Date and {subcat}'
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
        pio.write_html(fig_bar, file=f'c:/temp/{tit}.bars.html', auto_open=True)

        # fig_bar.update_layout(
        #     barmode='group',  # 'group' stack
        #     title=titl,
        #     xaxis_title='Date',
        #     yaxis_title='Quantity'
        # )
        # pio.write_html(fig_bar, file=f'c:/temp/{tit}.barg.html', auto_open=True)


