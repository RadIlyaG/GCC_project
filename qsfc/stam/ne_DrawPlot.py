
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
