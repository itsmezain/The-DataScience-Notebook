import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash
from dash import html, dcc
import os

file_path = os.path.join(os.path.dirname(__file__), 'gapminder.csv')
data = pd.read_csv(file_path)

app = dash.Dash()

app.layout = html.H2(children = "My First Dashboard using Dash", style={'color': 'red', 'text-align' : 'center'})

if __name__ == '__main__':
    app.run(debug=True)