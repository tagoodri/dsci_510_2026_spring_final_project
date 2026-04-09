import os
import pandas as pd
import requests
from config import playbyplay_path, quarter_length_sec,regulation_quarters, data_dir

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


def min_to_sec(minutes):
    splitting = minutes.split(':')
    splitting_length = len(splitting)
    if splitting_length > 1:
        return float(splitting[0]) * 60 + float(splitting[1])
    else:
        return float(splitting[0])
    
def espn_scores(url):
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        plays = data['plays']
        plays_list = []
        for play in plays:
            home_score = play['homeScore']
            away_score = play['awayScore']
            # Margin = margin of score for home team (pos = home team winning, neg = home team losing)
            margin = float(home_score) - float(away_score)
            current_quarter =  play['period'] ['number']
            quarters_left = regulation_quarters - current_quarter
            time_in_quarter = play ['clock'] ['displayValue']
            secs = quarters_left * quarter_length_sec + min_to_sec(time_in_quarter)
            description = f'Home team has {home_score} and away team has {away_score} with {time_in_quarter} left in quarter {current_quarter}'
            # TODO: Add ESPN probability to play_list so we can compare to our model.
            plays_list.append({'margin': margin, 'secs': secs, 'description': description})
        return plays_list
    else:
        print(f'Error: {response.status_code}')

# TODO: Get the latest score for the game.
# def espn_latest_score(url):
