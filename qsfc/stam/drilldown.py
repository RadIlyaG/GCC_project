import dash
from dash import dcc, html, Input, Output, State
from dash import dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
]


# Convert dates to datetime
for row in data:
    row['date'] = datetime.strptime(row['date'], "%Y-%m-%d")

app = dash.Dash(__name__)
app.title = "Customer Drilldown"
server = app.server

app.layout = html.Div([
    html.H2("📦 Customer Purchase Dashboard"),
    html.Button("⬅ Back", id='back-button', n_clicks=0, style={"display": "none"}),
    dcc.RadioItems(
        id='view-toggle',
        options=[
            {'label': 'Combined View', 'value': 'combined'},
            {'label': 'Split View', 'value': 'split'}
        ],
        value='combined',
        labelStyle={'display': 'inline-block', 'margin-right': '15px'},
        style={'margin-bottom': '10px'}
    ),
    dcc.Graph(id='main-chart'),
    dcc.Store(id='current-level', data='customer'),  # 'customer', 'product', 'time'
    dcc.Store(id='selected-customer'),
    dcc.Store(id='selected-product'),
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

])

# Update graph based on current level
@app.callback(
    Output('main-chart', 'figure'),
    Output('back-button', 'style'),
    Input('main-chart', 'clickData'),  # клик
    Input('current-level', 'data'),  # уровень (важно!)
    Input('selected-customer', 'data'),
    Input('selected-product', 'data'),
    Input('view-toggle', 'value'),
    State('data-store', 'data'),


)
def update_chart(clickData, level, customer, product, view_mode):
    print("update_chart triggered")
    print("level:", level)
    print("customer:", customer)
    print("product:", product)
    print("view_mode:", view_mode)
    print("click_data:", clickData)
    print("data sample:", data[:2])

    ctx = dash.callback_context
    triggered = ctx.triggered[0]['prop_id'] if ctx.triggered else None

    # Handle navigation logic
    if triggered == "main-chart.clickData":
        if level == 'customer':
            customer = clickData['points'][0]['x']
            level = 'product'
        elif level == 'product':
            product = clickData['points'][0]['x']
            level = 'time'
    elif triggered == "back-button.n_clicks":
        if level == 'product':
            level = 'customer'
            customer = None
        elif level == 'time':
            level = 'product'
            product = None

    back_style = {'display': 'none'}

    # Generate appropriate chart
    if level == 'customer':
        # fig = go.Figure(
        #     data=[
        #         go.Bar(
        #             x=['Alice', 'Bob'],
        #             y=[6, 8],
        #             text=[6, 8],
        #             textposition='auto',
        #             marker_color='cornflowerblue'
        #         )
        #     ]
        # )
        # fig.update_layout(
        #     title="Total Purchases by Customer",
        #     xaxis_title="Customer",
        #     yaxis_title="Quantity",
        # )
        # back_style = {'display': 'none'}
        # return fig, back_style

        if True:
            grouped = defaultdict(int)
            for row in data:
                grouped[row['customer']] += row['quantity']
            fig = go.Figure(data=[
                go.Bar(x=list(grouped.keys()), y=list(grouped.values()), textposition='auto')
            ])
            fig.update_layout(title="Total Purchases by Customer")
            back_style = {"display": "none"}

            customer_totals = defaultdict(int)
            for row in data:
                if 'customer' not in row or 'quantity' not in row:
                    print("Missing keys in row:", row)
                else:
                    customer_totals[row['customer']] += row['quantity']

            print("customer_totals:", customer_totals)

            fig = go.Figure(data=[
                go.Bar(
                    x=list(customer_totals.keys()),
                    y=list(customer_totals.values()),
                    text=list(customer_totals.values()),
                    textposition='auto',
                    marker_color='steelblue'
                )
            ])
            print(f'x:{list(customer_totals.keys())}, y:{list(customer_totals.values())}')
            fig.update_layout(
                title="Purchases by Customer",
                xaxis_title="Customer",
                yaxis_title="Total Quantity",
            )
            back_style = {'display': 'none'}
            return fig, back_style


    elif level == 'product':
        grouped = defaultdict(int)
        for row in data:
            if row['customer'] == customer:
                grouped[row['product']] += row['quantity']
        fig = go.Figure(data=[
            go.Bar(x=list(grouped.keys()), y=list(grouped.values()), textposition='auto')
        ])
        fig.update_layout(title=f"Products bought by {customer}")
        back_style = {"display": "inline-block"}
        return fig, back_style

    elif level == 'time':
        quantity_by_date = defaultdict(int)
        price_by_date = {}

        for row in data:
            if row['customer'] == customer and row['product'] == product:
                date = row['date'].date()
                quantity_by_date[date] += row['quantity']
                price_by_date[date] = row['price']  # override with latest price on that date

        dates = sorted(set(quantity_by_date.keys()) | set(price_by_date.keys()))


        if view_mode == 'combined':
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=dates,
                y=[quantity_by_date.get(d, 0) for d in dates],
                name='Quantity',
                yaxis='y1',
                marker_color='steelblue'
            ))
            fig.add_trace(go.Scatter(
                x=dates,
                y=[price_by_date.get(d, None) for d in dates],
                name='Price',
                yaxis='y2',
                mode='lines+markers',
                marker_color='crimson'
            ))
            fig.update_layout(
                title=f"{product} by {customer} – Quantity & Price",
                yaxis=dict(title='Quantity'),
                yaxis2=dict(
                    title='Price',
                    overlaying='y',
                    side='right',
                    showgrid=False
                ),
                legend=dict(x=0.01, y=0.99),
            )
            #return fig, back_style
        else:  # split view
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Quantity", "Price"))
            fig.add_trace(go.Bar(
                x=dates,
                y=[quantity_by_date.get(d, 0) for d in dates],
                name='Quantity',
                marker_color='steelblue'
            ), row=1, col=1)
            fig.add_trace(go.Scatter(
                x=dates,
                y=[price_by_date.get(d, None) for d in dates],
                name='Price',
                mode='lines+markers',
                marker_color='crimson'
            ), row=2, col=1)
            fig.update_layout(
                title_text=f"{product} by {customer} – Quantity & Price (Split View)",
                height=600
            )
        return fig, back_style
    back_style = {'display': 'block'}
    fig = go.Figure()
    fig.update_layout(title="No data to display")
    return fig, back_style

# Update drilldown state
@app.callback(
    Output('current-level', 'data'),
    Output('selected-customer', 'data'),
    Output('selected-product', 'data'),
    Input('main-chart', 'clickData'),
    Input('back-button', 'n_clicks'),
    Input('current-level', 'data'),
    Input('selected-customer', 'data'),
    Input('selected-product', 'data')
)
def update_state(clickData, back_clicks, level, customer, product):
    ctx = dash.callback_context
    triggered = ctx.triggered[0]['prop_id']

    if triggered == "main-chart.clickData":
        if level == 'customer':
            return 'product', clickData['points'][0]['x'], None
        elif level == 'product':
            return 'time', customer, clickData['points'][0]['x']
    elif triggered == "back-button.n_clicks":
        if level == 'product':
            return 'customer', None, None
        elif level == 'time':
            return 'product', customer, None

    return level, customer, product

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


# Run app
if __name__ == '__main__':
    app.run(debug=True)
