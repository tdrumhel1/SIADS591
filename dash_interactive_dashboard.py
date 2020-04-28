import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

df = pd.read_csv('nfl_small_end_of_drive.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

games = df['game_id'].unique()

app.layout = html.Div([
#     dcc.Input(id='my-id', value='initial value', type='text'),
    dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in games],
                value=2018121700
            ),
    html.Div(id='my-div')
])


# @app.callback(
#     Output(component_id='xaxis-column', component_property='children'),
#     [Input(component_id='xaxis-column', component_property='value'),Input('xaxis-column', 'value')]
# )


if __name__ == '__main__':
    app.run_server(debug=True)