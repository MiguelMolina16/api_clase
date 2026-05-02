import os
import json
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
os.environ['YFINANCE_CACHE_DIR'] = '/tmp/yfinance'

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import yfinance as yf
from flask import Flask

# Crear Flask server
server = Flask(__name__)

# Dash app montada en Flask
app = Dash(__name__, server=server, url_base_pathname='/')

stock_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

app.layout = html.Div([
    html.H1("Dashboard de Acciones", style={'textAlign': 'center'}),
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
        try:
            data = yf.download(stock, period='1mo', interval='1d')  # Reducido a 1 mes
            if not data.empty:
                traces.append(go.Scatter(
                    x=data.index,
                    y=data['Close'],
                    mode='lines',
                    name=stock
                ))
        except:
            continue
    
    return {
        'data': traces,
        'layout': go.Layout(title='Precios de cierre')
    }

# Handler para Vercel
def handler(request, context):
    return server(request.environ, lambda s, h: None)
