
import yfinance as yf
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

stock_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA']

app = Dash(__name__)
server = app.server  # 👈 clave para Vercel

app.layout = html.Div([
    html.H1("Dashboard de Acciones (Yahoo Finance)", style={'textAlign': 'center'}),
    
    dcc.Dropdown(
        id='stock-dropdown',
        options=[{'label': symbol, 'value': symbol} for symbol in stock_symbols],
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
        
        data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
        
        traces.append(go.Scatter(
            x=data.index,
            y=data['Close'].values,
            mode='lines',
            name=stock
        ))
    
    return {
        'data': traces,
        'layout': go.Layout(title='Precios de cierre diarios')
    }

# 👇 handler para Vercel
def handler(request):
    return server
