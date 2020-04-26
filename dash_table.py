# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

nfl_small2 = pd.read_csv('nfl_small_cleaned.csv').drop(columns=['Unnamed: 0']).sort_values(by=['game_id','play_id'])
nfl_small3 = nfl_small2[['play_id', 'game_id', 'game_date', 'time',
       'quarter_seconds_remaining', 'half_seconds_remaining',
       'game_seconds_remaining', 'game_half', 'quarter_end', 'qtr',
       'home_team', 'away_team', 'posteam', 'posteam_type', 'defteam']]

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='NFL Play-by-Play'),
    generate_table(nfl_small3)
])

if __name__ == '__main__':
    app.run_server(debug=True)