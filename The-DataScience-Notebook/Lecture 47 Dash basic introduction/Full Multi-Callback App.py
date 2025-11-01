import plotly.express as px
from dash import Dash, html, dcc, Input, Output, State

app = Dash(__name__)

df = px.data.gapminder()

app.layout = html.Div([
    html.H1("Interactive Dash App", style={'textAlign': 'center'}),

    dcc.Dropdown(
        id='continent',
        options=[{'label': c, 'value': c} for c in df['continent'].unique()],
        value='Asia'
    ),
    dcc.Dropdown(id='country'),

    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        step=5,
        value=df['year'].min(),
        marks={str(y): str(y) for y in df['year'].unique()}
    ),

    html.Button('Show Data', id='btn', n_clicks=0),
    html.Div(id='output-data'),
    dcc.Graph(id='gdp-chart')
])

@app.callback(
    Output('country', 'options'),
    Input('continent', 'value')
)
def update_country_options(cont):
    return [{'label': i, 'value': i} for i in df[df['continent'] == cont]['country'].unique()]

@app.callback(
    Output('gdp-chart', 'figure'),
    [Input('country', 'value'), Input('year-slider', 'value')]
)
def update_chart(country, year):
    filtered = df[(df['country'] == country) & (df['year'] <= year)]
    fig = px.line(filtered, x='year', y='gdpPercap', title=f'{country} GDP over Time')
    return fig

@app.callback(
    Output('output-data', 'children'),
    Input('btn', 'n_clicks'),
    State('country', 'value')
)
def show_data(n, country):
    if n == 0:
        return ''
    pop = df[df['country'] == country]['pop'].iloc[-1]
    return f"Population (latest year): {pop:,}"

if __name__ == '__main__':
    app.run(port= 8083, debug=True)
