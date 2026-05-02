import os
# Configuramos directorios temporales permitidos
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
os.environ['YFINANCE_CACHE_DIR'] = '/tmp/yfinance'

import yfinance as yf
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go


stock_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA']

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Dashboard de Acciones (Yahoo Finance)", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='stock-dropdown',
        options=[{'label': s, 'value': s} for s in stock_symbols],
        value=['AAPL'],
        multi=True
    ),
    dcc.Graph(id='stock-graph')
])

@app.callback(
    Output('stock-graph', 'figure'),
    Input('stock-dropdown', 'value')
)
def update_graph(selected_stocks):
    traces = []
    for stock in selected_stocks:
        data = yf.download(stock, period='1y', interval='1d')
        if data.empty:
            continue
        traces.append(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name=stock
        ))
    return {
        'data': traces,
        'layout': go.Layout(title='Precios de cierre diarios')
    }
