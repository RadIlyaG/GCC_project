import dash
from dash import dcc, html, Input, Output, State
from dash import dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from collections import defaultdict

app = dash.Dash(__name__)

# Sample data
import dash
from dash import dcc, html, Input, Output, State
from dash import dash_table
import plotly.graph_objects as go
from datetime import datetime
from collections import defaultdict

# Sample Data
data = [
    {'date': '2025-04-01', 'customer': 'Alice', 'product': 'Apples', 'quantity': 2, 'price': 3.5},
    {'date': '2025-04-02', 'customer': 'Alice', 'product': 'Bananas', 'quantity': 3, 'price': 2.0},
    {'date': '2025-04-01', 'customer': 'Bob', 'product': 'Cars', 'quantity': 1, 'price': 20000},
    {'date': '2025-04-02', 'customer': 'Bob', 'product': 'Cars', 'quantity': 2, 'price': 21000},
    {'date': '2025-04-03', 'customer': 'Alice', 'product': 'Cars', 'quantity': 1, 'price': 19500},
    {'date': '2025-04-03', 'customer': 'Bob', 'product': 'Bananas', 'quantity': 5, 'price': 1.8},
    {'date': '2025-04-04', 'customer': 'Alice', 'product': 'Bananas', 'quantity': 6, 'price': 2.0},
]
# Convert dates to datetime
for row in data:
    row['date'] = datetime.strptime(row['date'], "%Y-%m-%d")

app.layout = html.Div([
    html.H1("Drilldown Dashboard"),
    html.Button("⬅ Back", id='back-button', n_clicks=0, style={"display": "none"}),
    dcc.RadioItems(
        id='view-toggle',
        options=[
            {'label': 'Combined View', 'value': 'combined'},
            {'label': 'Split View', 'value': 'split'}
        ],
        value='combined',
        inline=True,
        labelStyle={'display': 'inline-block', 'margin-right': '15px'},
        style={'margin-bottom': '10px'}
    ),
    dcc.Graph(id='main-chart'),

    # Stores to manage app state
    dcc.Store(id='current-level', data='customer'),
    dcc.Store(id='selected-customer'),
    dcc.Store(id='selected-product'),
    dcc.Store(id='data-store', data=[{
        'date': row['date'].isoformat(),
        'customer': row['customer'],
        'product': row['product'],
        'quantity': row['quantity'],
        'price': row['price']
    } for row in data]),
    html.Div(
        dash_table.DataTable(
            id='raw-data-table',
            columns=[],  # filled dynamically
            data=[],
            style_table={'overflowX': 'auto', 'maxHeight': '400px', 'overflowY': 'scroll'},
            style_cell={'textAlign': 'left', 'padding': '6px'},
            style_header={'backgroundColor': '#f0f0f0', 'fontWeight': 'bold'},
            sort_action='native',
            filter_action='native',
            page_action='native',
            page_size=10,  # show 10 rows at a time
        ),
    ),
])

@app.callback(
    Output('current-level', 'data'),
    Output('selected-customer', 'data'),
    Output('selected-product', 'data'),
    Input('main-chart', 'clickData'),
    Input('back-button', 'n_clicks'),
    State('current-level', 'data'),
    State('selected-customer', 'data'),
    State('selected-product', 'data'),
    prevent_initial_call=True
)
def update_level(click_data, back_clicks, level, customer, product):

    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'main-chart' and click_data:
        if level == 'customer':
            return 'product', click_data['points'][0]['x'], None
        elif level == 'product':
            return 'time', customer, click_data['points'][0]['x']

    elif triggered_id == 'back-button':
        if level == 'time':
            return 'product', customer, None
        elif level == 'product':
            return 'customer', None, None

    raise dash.exceptions.PreventUpdate

@app.callback(
    Output('main-chart', 'figure'),
    Output('back-button', 'style'),
    Input('main-chart', 'clickData'),
    Input('current-level', 'data'),
    Input('selected-customer', 'data'),
    Input('selected-product', 'data'),
    Input('view-toggle', 'value'),
    State('data-store', 'data'),

)
def update_chart(click_data, level, customer, product, view_mode, data):
    print("update_chart triggered")
    ctx = dash.callback_context
    triggered = ctx.triggered[0]['prop_id'] if ctx.triggered else None
    print("triggered:", triggered)

    # Преобразуем строки обратно в datetime
    for row in data:
        row['date'] = datetime.fromisoformat(row['date'])

    back_style = {'display': 'none'}

    if level == 'customer':
        customer_totals = defaultdict(int)
        for row in data:
            customer_totals[row['customer']] += row['quantity']

        x = list(customer_totals.keys())
        y = list(customer_totals.values())
        fig = go.Figure([
            go.Bar(x=x, y=y, text=y, textposition='auto', marker_color='cornflowerblue')
        ])
        fig.update_layout(title="Total Purchases by Customer", xaxis_title="Customer", yaxis_title="Quantity")
        return fig, back_style

    elif level == 'product' and customer:
        product_totals = defaultdict(int)
        for row in data:
            if row['customer'] == customer:
                product_totals[row['product']] += row['quantity']

        x = list(product_totals.keys())
        y = list(product_totals.values())
        fig = go.Figure([
            go.Bar(x=x, y=y, text=y, textposition='auto', marker_color='mediumseagreen')
        ])
        fig.update_layout(title=f"Products bought by {customer}", xaxis_title="Product", yaxis_title="Quantity")
        back_style = {'display': 'block'}
        return fig, back_style

    elif level == 'time' and customer and product:
        date_totals = defaultdict(float)
        for row in data:
            if row['customer'] == customer and row['product'] == product:
                day = row['date'].strftime('%Y-%m-%d')
                date_totals[day] += row['price']

        dates = sorted(date_totals.keys())
        values = [date_totals[d] for d in dates]
        fig = go.Figure([
            go.Scatter(x=dates, y=values, mode='lines+markers', line=dict(color='tomato', width=2))
        ])
        fig.update_layout(
            title=f"Price Trend for {product} (Customer: {customer})",
            xaxis_title="Date",
            yaxis_title="Total Price"
        )
        back_style = {'display': 'block'}
        return fig, back_style

    fig = go.Figure()
    fig.update_layout(title="No Data to Display")
    return fig, back_style

@app.callback(
    Output('raw-data-table', 'data'),
    Output('raw-data-table', 'columns'),
    Input('current-level', 'data'),
    Input('selected-customer', 'data'),
    Input('selected-product', 'data')
)
def update_table(level, customer, product):
    filtered_data = []

    for row in data:
        row_copy = row.copy()
        row_copy['date'] = row_copy['date'].strftime('%Y-%m-%d')  # for display
        if level == 'customer':
            filtered_data.append(row_copy)
        elif level == 'product' and row['customer'] == customer:
            filtered_data.append(row_copy)
        elif level == 'time' and row['customer'] == customer and row['product'] == product:
            filtered_data.append(row_copy)

    if not filtered_data:
        return [], []

    columns = [{"name": k, "id": k} for k in filtered_data[0].keys()]
    return filtered_data, columns

if __name__ == '__main__':
    app.run(debug=True)
