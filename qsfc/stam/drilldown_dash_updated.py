
from dash import Dash, dcc, html, Input, Output, State, callback_context, dash_table
import plotly.graph_objects as go
from collections import defaultdict
from datetime import datetime

data1 = [
    {'date': datetime(2025, 4, 1), 'customer': 'Alice', 'product': 'Apples', 'quantity': 2, 'price': 3.5},
    {'date': datetime(2025, 4, 2), 'customer': 'Alice', 'product': 'Bananas', 'quantity': 3, 'price': 2.0},
    {'date': datetime(2025, 4, 3), 'customer': 'Bob', 'product': 'Cars', 'quantity': 1, 'price': 10000},
    {'date': datetime(2025, 4, 5), 'customer': 'Bob', 'product': 'Cars', 'quantity': 2, 'price': 12000},
    {'date': datetime(2025, 4, 7), 'customer': 'Bob', 'product': 'Apples', 'quantity': 5, 'price': 4.0},
]
data = [
    {"date": datetime(2025, 4, 3), "customer": "Alice", "product": "Oranges", "quantity": 4, "price": 2.5},
    {"date": datetime(2025, 4, 4), "customer": "Alice", "product": "Bananas", "quantity": 2, "price": 2.2},
    {"date": datetime(2025, 4, 8), "customer": "Alice", "product": "Cars", "quantity": 2, "price": 2.2},
    {"date": datetime(2025, 4, 9), "customer": "Alice", "product": "Oranges", "quantity": 2, "price": 2.5},
    {"date": datetime(2025, 4, 3), "customer": "Bob", "product": "Cars", "quantity": 1, "price": 30000},
    {"date": datetime(2025, 4, 4), "customer": "Bob", "product": "Apples", "quantity": 5, "price": 3.8},
    {"date": datetime(2025, 4, 5), "customer": "Charlie", "product": "Bikes", "quantity": 2, "price": 450},
    {"date": datetime(2025, 4, 6), "customer": "Charlie", "product": "Apples", "quantity": 3, "price": 3.6},
]


app = Dash(__name__)

app.layout = html.Div([
    dcc.Store(id='data-store', data=data),
    dcc.Store(id='current-level', data='customer'),
    dcc.Store(id='selected-customer'),
    dcc.Store(id='selected-product'),

    dcc.Graph(id='main-chart'),

    html.Button("Back", id='back-button', style={'display': 'none'}),

    html.Div([
        dash_table.DataTable(
            id='raw-data-table',
            page_size=10,
            sort_action='native',
            filter_action='native'
        )
    ], id='table-container', style={'display': 'block'}),
])

@app.callback(
    Output('main-chart', 'figure'),
    Output('back-button', 'style'),
    Output('raw-data-table', 'data'),
    Output('raw-data-table', 'columns'),
    Output('table-container', 'style'),
    Output('current-level', 'data'),
    Output('selected-customer', 'data'),
    Output('selected-product', 'data'),
    Input('main-chart', 'clickData'),
    Input('back-button', 'n_clicks'),
    State('current-level', 'data'),
    State('selected-customer', 'data'),
    State('selected-product', 'data'),
    State('data-store', 'data'),
)
def update_chart(clickData, n_clicks, level, selected_customer, selected_product, data):
    from collections import defaultdict
    from dash import callback_context
    import plotly.graph_objects as go

    print("Triggered by:", callback_context.triggered)
    print("clickData:", clickData)

    # Инициализация значений
    ctx = callback_context
    triggered = ctx.triggered[0]['prop_id'] if ctx.triggered else ''

    fig = go.Figure()
    back_style = {'display': 'none'}
    new_level = level
    new_selected_customer = selected_customer
    new_selected_product = selected_product
    filtered_data = data

    # === 1. Обработка переходов вперёд при клике на графике ===
    if triggered == "main-chart.clickData":
        if level == 'customer':
            new_selected_customer = clickData['points'][0]['x']
            new_level = 'product'
        elif level == 'product':
            new_selected_product = clickData['points'][0]['x']
            new_level = 'time'

    # === 2. Обработка переходов назад ===
    if triggered == "back-button.n_clicks":
        if level == 'time':
            new_level = 'product'
            new_selected_product = None
        elif level == 'product':
            new_level = 'customer'
            new_selected_customer = None

    # === 3. Отрисовка графика и таблицы в зависимости от текущего уровня ===
    if new_level == 'customer':
        customer_totals = defaultdict(int)
        for row in data:
            customer_totals[row['customer']] += row['quantity']
        fig.add_trace(go.Bar(
            x=list(customer_totals.keys()),
            y=list(customer_totals.values()),
            text=list(customer_totals.values()),
            textposition='auto'
        ))
        fig.update_layout(title="Total Purchases by Customer")
        filtered_data = data  # показываем все данные
        back_style = {'display': 'none'}  # кнопка назад не показывается

    elif new_level == 'product':
        filtered_data = [row for row in data if row['customer'] == new_selected_customer]
        product_totals = defaultdict(int)
        for row in filtered_data:
            product_totals[row['product']] += row['quantity']
        fig.add_trace(go.Bar(
            x=list(product_totals.keys()),
            y=list(product_totals.values()),
            text=list(product_totals.values()),
            textposition='auto'
        ))
        fig.update_layout(title=f"Products bought by {new_selected_customer}")
        back_style = {'display': 'inline-block'}

    elif new_level == 'time':
        filtered_data = [
            row for row in data if row['customer'] == new_selected_customer and row['product'] == new_selected_product
        ]
        filtered_data.sort(key=lambda x: x['date'])
        fig.add_trace(go.Scatter(
            x=[row['date'] for row in filtered_data],
            y=[row['price'] for row in filtered_data],
            mode='lines+markers+text',
            text=[f"${row['price']}" for row in filtered_data],
            textposition='top center'
        ))
        fig.update_layout(title=f"{new_selected_product} prices over time for {new_selected_customer}")
        back_style = {'display': 'inline-block'}

    # === 4. Построение таблицы ===
    table_columns = [{"name": k, "id": k} for k in filtered_data[0].keys()] if filtered_data else []

    return fig, back_style, filtered_data, table_columns, {'display': 'block'}, new_level, new_selected_customer, new_selected_product


if __name__ == '__main__':
    app.run(debug=True)
