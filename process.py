import pandas as pd
from config import regulation_quarters, quarter_length_sec

def process_playbyplay(df):
    # Cleaning pbp data and keeping only useful columns for now
    key_cols = ['WinningTeam', 'AwayTeam', 'HomeTeam', 'AwayScore',
                'HomeScore', 'Quarter', 'SecLeft', 'Date', 'Location'] 
    #keeping in data + location in anticipation of implementing days off/travel for the teams
    df = df[key_cols].copy()

    # Score margin... positive = home team leading
    df['ScoreMargin'] = df['HomeScore'] - df['AwayScore']

    # Total seconds left in the game
    df['TotalSecLeft'] = ((regulation_quarters - df['Quarter']) * quarter_length_sec) + df['SecLeft']

    # Target variable... 1 = home team won, 0 = away team won
    df['HomeWin'] = (df['WinningTeam'] == df['HomeTeam']).astype(int)

    # Drop rows missing key columns
    df = df.dropna(subset=['ScoreMargin', 'TotalSecLeft', 'HomeWin'])

    print(f"Play-by-play processed: {df.shape[0]} rows remaining")
    return df

 