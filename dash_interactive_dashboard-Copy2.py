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
    dcc.Dropdown(
        id='xaxis-column',
        options=[{'label': i, 'value': i} for i in games],
        value=2018121700,
        style=dict(
                    width='40%',
                    display='inline-block',
                    verticalAlign="middle",
                )
#         placeholder="Select Answer"
    ),
    dcc.Graph(id='graph-div')
]
)

@app.callback(
    Output(component_id='graph-div', component_property='figure'),
    [Input(component_id='xaxis-column', component_property='value'),Input('xaxis-column', 'value')]
)
def update_output_div(input_value,input_value2):
    dff = df[df['game_id'] == input_value]
    
    traces = [
        dict(
            x=dff['drive'],
            y=dff['total_home_score'],
            text=dff['home_team'].unique()[0],
            mode='lines',
            name=dff['home_team'].unique()[0],
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
                }
            ),
        dict(
            x=dff['drive'],
            y=dff['total_away_score'],
            text=dff['away_team'].unique()[0],
            mode='lines',
            name=dff['away_team'].unique()[0],
            marker={
                    'size': 15,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'white'}
                }
            )
        ]
    
    
    return {
        'data': traces,
        'layout': dict(
            xaxis={
                'title': 'Drive',
                'type': 'linear'
            },
            yaxis={
                'title': 'Score',
                'type': 'linear'
            },height=700,width=600,
#            hovermode='closest',
            title='In-Game Score'
            )
        }


if __name__ == '__main__':
    app.run_server(debug=True)