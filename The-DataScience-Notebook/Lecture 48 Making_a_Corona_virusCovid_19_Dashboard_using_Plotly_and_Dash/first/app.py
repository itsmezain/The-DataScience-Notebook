# 📦 Importing the libraries
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import os

# Importing the dataset
csv_path = os.path.join(os.path.dirname(__file__), 'IndividualDetails.csv')
patients = pd.read_csv(csv_path)

# Making cards data
total_cases = patients.shape[0]
active = patients[patients['current_status'] == 'Hospitalized'].shape[0]
recovered = patients[patients['current_status'] == 'Recovered'].shape[0]
death = patients[patients['current_status'] == 'Deceased'].shape[0]

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Creating website layout(UI)
app.layout = dbc.Container(
    [
        html.H1("Corona Virus Pandemic", style={
                "color": "#fff", "text-align": "center", 'padding': 8, 'margin': 15}),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("Total Cases"),
                                html.H4(total_cases),
                            ]
                        ),
                        color="danger",
                        inverse=True
                    ),
                    width=3,
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("Active Cases"),
                                html.H4(active),
                            ]
                        ),
                        color="info",
                        inverse=True
                    ), width=3),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("Recovered"),
                                html.H4(recovered),
                            ]
                        ),
                        color="warning",
                        inverse=True
                    ), width=3),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("Deaths"),
                                html.H4(death),
                            ]
                        ),
                        color="success",
                        inverse=True
                    ), width=3)
            ], style={'padding': 8, 'margin': 15}
        ),

        dbc.Row([]),

        # Adding Dropdown and graph
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            dcc.Dropdown(
                                id='picker', options=[{'label': c, 'value': c} for c in ['All', 'Hospitalized', 'Recovered', 'Deceased']], value='All'
                            ),
                            dcc.Graph(id='bar')
                        ]
                    )
                )
            )
        ])
    ],
    fluid=True,
)

# Function with Decorator (@callback) to update the graph using the user input
@app.callback(
    Output('bar', 'figure'),
    Input('picker', 'value')
)
def update_graph(val):
    if val == 'All':
        pbar = patients['detected_state'].value_counts().reset_index()
        fig = go.Figure(
            data=[go.Bar(x=pbar['detected_state'],
                         y=pbar['count'], text=pbar['count'])],

            layout=go.Layout(title='State Total Count'
                             )
        )
    else:
        npat = patients[patients['current_status'] == val]
        pbar = npat['detected_state'].value_counts().reset_index()
        fig = go.Figure(
            data=[go.Bar(x=pbar['detected_state'],
                         y=pbar['count'], text=pbar['count'])],
            layout=go.Layout(title=f'{val} Count by State')
        )

    return fig


if __name__ == "__main__":
    app.run(port=8081, debug=True)
