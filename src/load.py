import os
import pandas as pd
import requests
from config import quarter_length_sec,regulation_quarters, data_dir, payroll_path, win_pct_path, espn_scoreboard_url, espn_game_url

def load_playbyplay():
    #load all csvs and combine
    all_seasons = []
    for filename in os.listdir(data_dir):
            filepath = os.path.join(data_dir, filename)
            df = pd.read_csv(filepath)
            all_seasons.append(df)
            print(f"Loaded: {filename} — {df.shape[0]} rows")
    
    combined = pd.concat(all_seasons, ignore_index=True)
    print(f"\nAll seasons combined: {combined.shape[0]} total rows")
    return combined


def load_all():
    #load all pbps and return
    playbyplay = load_playbyplay()
    return playbyplay

def load_payroll():
    # Load salary cap data, manually removed rows from normal csv to make sure i get inflation adjusted
    df = pd.read_csv(payroll_path)
    
    #remove the $ and the commas from CSV and turn into float value... could use regex maybe instead?
    df['inflationAdjPayroll'] = df['inflationAdjPayroll'].str.replace('$', '')
    df['inflationAdjPayroll'] = df['inflationAdjPayroll'].str.replace(',', '')
    df['inflationAdjPayroll'] = df['inflationAdjPayroll'].astype(float)
    
    print(f"Payroll loaded: {len(df)} rows") #will be an extra 30 rows then win% b/c I have this years team salary too
    return df

def min_to_sec(minutes):
    #converting to secs 
    splitting = minutes.split(':')
    splitting_length = len(splitting)
    if splitting_length > 1:
        return float(splitting[0]) * 60 + float(splitting[1])
    else:
        return float(splitting[0])

def play_by_play_url(game_id):
    # when give correct game id, shows the ESPN play-by-play url
    return f'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={game_id}'

def get_games_on_date(date):
    #making it easier for ESPN data and with the widget 
    if date.month < 10: # building conditional to put a zero in front of month if before october for api stuff
        formattedMonth = f'0{date.month}'
    else:
        formattedMonth = date.month

    if date.day < 10: # building conditional to put a zero in front of date for api stuff
        formattedDay = f'0{date.day}'
    else:
        formattedDay = date.day

    date_string = f'{date.year}{formattedMonth}{formattedDay}'
    url = f'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={date_string}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        events = data["events"] #find all games played that day
        all_games = {} # setting empty game list
        for e in events:
            game_id = e['id'] #finds id at end of espn link
            matchup = e['name'] #gets the two teams in the game in 'team at team' format
            all_games[matchup] = game_id
        return all_games
    
    else:
        print(f'Error: {response.status_code}')

def load_win_pct():
    #bringing in team win pct per year 
    df = pd.read_csv(win_pct_path)
    df = df[['Team', 'win_percentage', 'season']]
    df = df.rename(columns={'season': 'seasonStartYear', 'Team': 'team'}) #rename & lower to match others
    print(f"Win percentage loaded: {len(df)} rows")
    return df

    
def espn_scores(game_id):
    url = play_by_play_url (game_id)
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        teams = data['boxscore']['teams']
        home_team = None
        away_team = None
        home_team_color = None #to get team colors for the plot
       # away_team_color = None #to get team colors for the plot (not active atm)

        for t in teams:
            team = t['team']
            team_color = team['color']
            team_city = team ['location']
            team_name = team ['name']
            
            if team_name == 'Lakers':
                team_city = 'LA Lakers' # lakers and clippers dont map based off purely city, clarify between both LA teams
            elif team_name == 'Clippers':
                team_city = 'LA Clippers' # lakers and clippers dont map based off purely city, clarify between both LA teams
            home_or_away = t['homeAway']
            if home_or_away == 'home':
                home_team = team_city
                home_team_color = team_color
            else:
                away_team = team_city
                #away_team_color = team_color Not using atm 
     


        win_probs = data ['winprobability'] #finds all win probabilities in all games plays
        play_win_dict = {} #dict for specfic play to espn's win prob
        for win_prob in win_probs:
            play_id = win_prob ['playId']
            win_percentage = win_prob ['homeWinPercentage']
            play_win_dict[play_id] = win_percentage
        plays = data['plays']
        plays_list = []
        for play in plays:
            home_score = play['homeScore']
            away_score = play['awayScore']
            # Margin = margin of score for home team (pos = home team winning, neg = home team losing)
            play_id = play['id'] #finds unique espn id for each play
            play_description = play['text'] #shows espn description of play in game: e.g 'Lebron missed 25 ft 3-pointer)
            margin = float(home_score) - float(away_score)
            espn_win_percentage = play_win_dict[play_id]
             
            current_quarter =  play['period'] ['number']
            quarters_left = regulation_quarters - current_quarter
            time_in_quarter = play ['clock'] ['displayValue']
            secs = quarters_left * quarter_length_sec + min_to_sec(time_in_quarter)
            description = f'Home team has {home_score} and away team has {away_score} with {time_in_quarter} left in quarter {current_quarter}. Play: {play_description}.'
            plays_list.append({'margin': margin, 'secs': secs, 'description': description, 'espn_win_percentage': espn_win_percentage, 'play_description': play_description})
        return {'plays_list': plays_list, 'home_team': home_team, 'away_team': away_team, 'home_team_color': home_team_color,}
    else:
        print(f'Error: {response.status_code}')
