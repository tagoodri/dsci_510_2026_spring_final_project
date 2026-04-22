import pandas as pd
from config import regulation_quarters, quarter_length_sec, team_names

def process_playbyplay(df):
    # Cleaning pbp data and keeping only useful columns for now
    key_cols = ['WinningTeam', 'AwayTeam', 'HomeTeam', 'AwayScore',
                'HomeScore', 'Quarter', 'SecLeft', 'Date', 'Location'] 
    #keeping in data + location in anticipation of implementing days off/travel for the teams down the line
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

def process_payroll(pbp_df, payroll_df):
    # Merging payroll with pbp

    # Get season year from date
    # found datetime module from python - https://docs.python.org/3/library/datetime.html
    # dt is used to access certain parts - https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.html 
   
    pbp_df['Date'] = pd.to_datetime(pbp_df['Date'])
    pbp_df['seasonStartYear'] = pbp_df['Date'].dt.year
    
    #payroll does by start year (so 2015-2016 szn shows as 2015), need to adjust to show full szn (all non bubble szns start in oct)
    pbp_df.loc[pbp_df['Date'].dt.month < 10, 'seasonStartYear'] -= 1
   
    # abrvs to entire names
    pbp_df['HomeTeamFull'] = pbp_df['HomeTeam'].map(team_names)
    pbp_df['AwayTeamFull'] = pbp_df['AwayTeam'].map(team_names)


    # Merge home payroll
    #changing column names to make it merge smoothly (for home)
    home_payroll = payroll_df.rename(columns={'team': 'HomeTeamFull', 'inflationAdjPayroll': 'HomePayroll'})
    pbp_df = pbp_df.merge(home_payroll[['HomeTeamFull', 'seasonStartYear', 'HomePayroll']], on=['HomeTeamFull', 'seasonStartYear'])
   
    # Merge away payroll
    #changing column names to make it merge smoothly (for away)
    away_payroll = payroll_df.rename(columns={'team': 'AwayTeamFull', 'inflationAdjPayroll': 'AwayPayroll'})
    pbp_df = pbp_df.merge(away_payroll[['AwayTeamFull', 'seasonStartYear', 'AwayPayroll']], on=['AwayTeamFull', 'seasonStartYear'])


    # trying to solve pandas renaming issue
    # *** AI USE: had issues with merges, I then prompted AI (Claude) and I learned that pandas creates extra suffixes ***
    pbp_df = pbp_df.rename(columns={'HomePayroll_x': 'HomePayroll'})
    pbp_df = pbp_df.drop(columns=['HomePayroll_y'], errors='ignore')
    
    # find delta between two teams payrolls ($$$)
    pbp_df['PayrollDiff'] = pbp_df['HomePayroll'] - pbp_df['AwayPayroll']

    print(f"Payroll merged: {len(pbp_df)} rows remaining")
    return pbp_df
 