def game_schedule(year):
    
    import requests
    import urllib.request
    import time
    import pandas as pd
    
    url = 'https://www.pro-football-reference.com/years/' + year + '/games.htm'
    
    df = pd.read_html(url)[0]
    
    # Renaming column that determine location of game
    df = df.rename(columns={"Unnamed: 5": "location"})
    
    df['year'] = year
    
    df['home_team'] = df.apply(lambda x : x['Loser/tie'] if x['location'] == '@' else x['Winner/tie'],axis=1)
    df['away_team'] = df.apply(lambda x : x['Winner/tie'] if x['location'] == '@' else x['Loser/tie'],axis=1)
    
    team_mapping = {
    'Arizona Cardinals':'ARI',
    'Atlanta Falcons':'ATL',
    'Baltimore Ravens':'BAL',
    'Buffalo Bills':'BUF',
    'Carolina Panthers':'CAR',
    'Chicago Bears':'CHI',
    'Cincinnati Bengals':'CIN',
    'Cleveland Browns':'CLE',
    'Dallas Cowboys':'DAL',
    'Denver Broncos':'DEN',
    'Detroit Lions':'DET',
    'Green Bay Packers':'GB',
    'Houston Texans':'HOU',
    'Indianapolis Colts':'IND',
    'Jacksonville Jaguars':'JAX',
    'Kansas City Chiefs':'KC',
    'Los Angeles Rams':'LA',
    'Los Angeles Chargers':'LAC',
    'Miami Dolphins':'MIA',
    'Minnesota Vikings':'MIN',
    'New England Patriots':'NE',
    'New Orleans Saints':'NO',
    'New York Giants':'NYG',
    'New York Jets':'NYJ',
    'Oakland Raiders':'OAK',
    'Philadelphia Eagles':'PHI',
    'Pittsburgh Steelers':'PIT',
    'Seattle Seahawks':'SEA',
    'San Francisco 49ers':'SF',
    'Tampa Bay Buccaneers':'TB',
    'Tennessee Titans':'TEN',
    'Washington Redskins':'WAS'
    }
    
    # Replacing team names to be consistent with play-by-play data
    df = df.replace({'home_team':team_mapping}).replace({'away_team':team_mapping})
    
    # Removing date headers
    df = df[~df['Date'].isin(['Date','Playoffs'])]
    
    # Casting date object as date
    df['Date'] = pd.to_datetime(df['Date'] + ', ' + year)
    
    # Casting Time object as time
    df['Time'] = pd.to_datetime(df['Time']).dt.time
    
    return df[['Date','Time','home_team','away_team']]