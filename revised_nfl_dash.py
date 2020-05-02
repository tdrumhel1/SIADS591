import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd

df = pd.read_csv('nfl_small_end_of_drive.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

games = df.groupby(['game_id','game_name']).count().reset_index()[['game_id','game_name']]
game_list = games.apply(lambda x : [x['game_id'], x['game_name']],axis=1)

app.layout = html.Div([
    
    # First Row
    html.Div([
        # Game Select Dropdown (First Row - Left Side)
        html.Div([
    
        html.Label(children='Select Game Here',style={'textAlign':'left'}),
        dcc.Dropdown(
            id='xaxis-column',
            options=[{'label': i[1], 'value': i[0]} for i in game_list],
            value=2018121700
                )
            ],className='four columns'),
        
#         # Middle Space
#         html.Div([
#             html.Img(src='NFL_Logo.png')
#             ],className='four columns'),
        
        # Logo in Right
        html.Div([
            html.Img(src='assets/NFL_Logo.png',style={'height':'30%','width':'30%'})
            ],className='two columns',style={'float':'right'})
        ],className='row'),
    
    # Second Row - Does not resize yet
    html.Div([
        
        html.Div([
            dcc.Graph(id='graph-div')
            ],className='twelve columns',
                style={'float':'middle',
                         'height':'100%', 
                          'width':'100%'})
    ],className='row'),
    
    
    # Third Row
    html.Div([
        
        # Total Yards
        html.Div([
            html.Label(children='Total Yards')
            ],className='three columns',style={'textAlign':'center'})
        
        ],className='row'),

    # Fourth Row
    html.Div([
        
        html.Div([
            html.Label(children='Home Team',style={'display': 'inline-block','textAlign':'center'},className='three columns'),
            html.Label(children='Away Team',style={'display': 'inline-block','textAlign':'center'},className='three columns')
            ],className='six columns')
            
    ],className='row'),

    # Fifth Row
    html.Div([
        
        html.Div([
            html.Label(id='home-yards',style={'display': 'inline-block','textAlign':'center'},className='three columns'),
            html.Label(id='away-yards',style={'display': 'inline-block','textAlign':'center'},className='three columns')
            ],className='six columns')
            
    ],className='row')
    
    ])


# Callback for Away Yards - Sum isn't filtering on team or Yards are off
@app.callback(
    Output(component_id='home-yards', component_property='children'),
    [Input(component_id='xaxis-column', component_property='value')]
)
def update_home_yards(input_value):
    dff = df[df['game_id'] == input_value]
    
    team = dff['home_team'].unique()[0]
    
    return dff[dff['posteam']==team]['ydsnet'].sum()

# Callback for Away Yards - Sum isn't filtering on team or Yards are off
@app.callback(
    Output(component_id='away-yards', component_property='children'),
    [Input(component_id='xaxis-column', component_property='value')]
)
def update_away_yards(input_value):
    dff = df[df['game_id'] == input_value]
    
    team = dff['away_team'].unique()[0]
    
    return dff[dff['posteam']==team]['ydsnet'].sum()



@app.callback(
    Output(component_id='graph-div', component_property='figure'),
    [Input(component_id='xaxis-column', component_property='value'),Input('xaxis-column', 'value')] # Right now this is redundant
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
            },height=700,width=700,
#            hovermode='closest',
            title='In-Game Score'
            )
        }


if __name__ == '__main__':
    app.run_server(debug=True)