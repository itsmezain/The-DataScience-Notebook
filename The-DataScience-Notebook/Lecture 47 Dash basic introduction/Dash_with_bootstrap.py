import dash_bootstrap_components as dbc
from dash import Dash, html, dcc

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Dashboard", className="text-center text-light mb-4"), width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.H5("Options"),
            dcc.Dropdown(['A', 'B', 'C'], 'A', id='dropdown')
        ], width=4),

        dbc.Col([
            dcc.Graph(id='chart')
        ], width=8)
    ])
], fluid=True)

if __name__ == '__main__':
    app.run(port=8087, debug=True)
