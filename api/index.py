import os

# Configuración temporal
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
os.environ['YFINANCE_CACHE_DIR'] = '/tmp/yfinance'

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import yfinance as yf

stock_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

app = Dash(__name__)

# CRÍTICO: app.server es lo que Vercel necesita
server = app.server

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
            data = yf.download(stock, period='1y', interval='1d')
            if not data.empty:
                traces.append(go.Scatter(
                    x=data.index,
                    y=data['Close'],
                    mode='lines',
                    name=stock
                ))
        except Exception as e:
            print(f"Error con {stock}: {e}")
    
    return {
        'data': traces,
        'layout': go.Layout(
            title='Precios de cierre diarios',
            xaxis={'title': 'Fecha'},
            yaxis={'title': 'Precio (USD)'}
        )
    }
