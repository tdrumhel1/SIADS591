import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

df = pd.read_csv('nfl_small_end_of_drive.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

games = df['game_id'].unique()

# trace1 = go.Scatter(
#       x = df[df['game_id']=={input}]['drive'], 
#       y = df[df['game_id']=={input}]['total_home_score'], 
#       mode = 'lines', 
#       name = df['home_team'].unique()[0],
#       type = "scatter"
#     )

app.layout = html.Div([
    dcc.Dropdown(
        id='xaxis-column',
        options=[{'label': i, 'value': i} for i in games],
        value=2018121700
    ),
    dcc.Graph(id='graph-div')
]
)
#         figure={
#             'data': [
#                 {'x': df[df['game_id']=={input}]['drive'],
#                  'y': df[df['game_id']=={input}]['total_home_score'], 'type': 'line', 'name': df['home_team'].unique()[0]},
#             ],
#             'layout': {
#                 'plot_bgcolor': colors['background'],
#                 'paper_bgcolor': colors['background'],
#                 'font': {
#                     'color': colors['text']
#                 }
#             }
#         }
#     )


@app.callback(
    Output(component_id='graph-div', component_property='figure'),
    [Input(component_id='xaxis-column', component_property='value'),Input('xaxis-column', 'value')]
)
def update_output_div(input_value,input_value2):
    dff = df[df['game_id'] == input_value]
    
    
    return {
        'data': [dict(
            x=dff['drive'],
            y=dff['total_home_score'],
            text=dff['home_team'].unique()[0],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': 'Drive',
                'type': 'linear'
            },
            yaxis={
                'title': 'Score',
                'type': 'linear'
            },
#             margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)