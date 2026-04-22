import os

# Paths 
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
data_dir = os.path.join(base_dir, "data")
results_dir = os.path.join(base_dir, "results")

# Data file paths for payroll and win 
payroll_path = os.path.join(data_dir, "Payrolls.csv")
win_pct_path = os.path.join(data_dir, "Win_Pct.csv")

#data sources configs
espn_scoreboard_url = 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={}'
espn_game_url = 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={}'

# Model Settings & plot sizes
test_size = 0.2 #makes training model 80%
random_state = 42 #common random state #?
plot_size = (10,6)
plot_size_smallish = (8,6)

# Game Settings 
regulation_quarters = 4
quarter_length_sec = 12 * 60

# Correcting Team names & abrvs from Payroll & PBP data
# followed this list on alphabetical order https://en.wikipedia.org/wiki/Wikipedia:WikiProject_National_Basketball_Association/National_Basketball_Association_team_abbreviations
team_names = {
    'ATL': 'Atlanta',
    'BRK': 'Brooklyn',
    'BOS': 'Boston',
    'CHO': 'Charlotte',
    'CHI': 'Chicago',
    'CLE': 'Cleveland',
    'DAL': 'Dallas',
    'DEN': 'Denver',
    'DET': 'Detroit',
    'GSW': 'Golden State',
    'HOU': 'Houston',
    'IND': 'Indiana',
    'LAC': 'LA Clippers',
    'LAL': 'LA Lakers',
    'MEM': 'Memphis',
    'MIA': 'Miami',
    'MIL': 'Milwaukee',
    'MIN': 'Minnesota',
    'NOP': 'New Orleans',
    'NYK': 'New York',
    'OKC': 'Oklahoma City',
    'ORL': 'Orlando',
    'PHI': 'Philadelphia',
    'PHO': 'Phoenix',
    'POR': 'Portland',
    'SAC': 'Sacramento',
    'SAS': 'San Antonio',
    'TOR': 'Toronto',
    'UTA': 'Utah',
    'WAS': 'Washington'
}