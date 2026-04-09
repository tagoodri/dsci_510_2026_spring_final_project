import os

# Paths 
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
results_dir = os.path.join(base_dir, "results")

# Data file paths
playbyplay_path = os.path.join(data_dir, "nba_playbyplay.csv")
schedule_path = os.path.join(data_dir, "nba_schedule.csv")

# Model Settings 
test_size = 0.2 #makes training model80%)
random_state = 42

# Game Settings 
regulation_quarters = 4
quarter_length_sec = 12 * 60