import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash
from dash import html, dcc
import os

file_path = os.path.join(os.path.dirname(__file__), "gapminder.csv")
data = pd.read_csv(file_path)

app = dash.Dash()

app.layout = html.Div(
    [
        html.Div(
            children=[
                html.H2(
                    "My First Dashboard", style={"color": "red", "text-align": "center"}
                )
            ],
            style={
                "border": "1px black solid",
                "float": "left",
                "width": "100%",
                "height": "50px",
            },
        ),
        html.Div(
            children=[
                dcc.Graph(
                    id="scatter-plot",
                    figure={
                        "data": [
                            go.Scatter(
                                x=data["population_total"],
                                y=data["gdp_total_yearly_growth"],
                                mode="markers",
                            )
                        ],
                        "layout": go.Layout(title=" Scatter Plot"),
                    },
                )
            ],
            style={
                "border": "1px black solid",
                "float": "left",
                "width": "49.5%",
                "height": "350px",
            },
        ),
        html.Div(
            children=[
                dcc.Graph(
                    id="Box Plot",
                    figure={
                        "data": [go.Box(x=data["gdp_total_yearly_growth"])],
                        "layout": go.Layout(title="Box Plot"),
                    },
                )
            ],
            style={
                "border": "1px black solid",
                "float": "left",
                "width": "49.5%",
                "height": "350px",
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)