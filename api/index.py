import os
import json
from flask import Flask, render_template_string
import yfinance as yf
import plotly
import plotly.graph_objs as go

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard de Acciones</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { font-family: Arial; margin: 40px; }
        select { padding: 10px; margin: 20px 0; width: 300px; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <h1>Dashboard de Acciones</h1>
    <form method="GET">
        <select name="stocks" multiple size="5">
            <option value="AAPL">Apple</option>
            <option value="MSFT">Microsoft</option>
            <option value="GOOGL">Google</option>
            <option value="AMZN">Amazon</option>
            <option value="TSLA">Tesla</option>
            <option value="META">Meta</option>
        </select>
        <button type="submit">Actualizar</button>
    </form>
    <div id="graph"></div>
    <script>
        var graphs = {{ graphs | safe }};
        Plotly.newPlot('graph', graphs, {title: 'Precios de acciones'});
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    selected_stocks = ['AAPL']  # Valor por defecto
    
    traces = []
    for stock in selected_stocks:
        try:
            data = yf.download(stock, period='1mo', interval='1d')
            if not data.empty:
                trace = go.Scatter(
                    x=data.index,
                    y=data['Close'],
                    mode='lines',
                    name=stock
                )
                traces.append(trace)
        except:
            continue
    
    graphs_json = json.dumps(traces, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template_string(HTML_TEMPLATE, graphs=graphs_json)

if __name__ == '__main__':
    app.run()
