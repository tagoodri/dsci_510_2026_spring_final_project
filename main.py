from load import load_playbyplay, espn_scores
from process import process_playbyplay
from analyze import (show_correlations, train_model, predict_win_probability,
                     plot_correlation_heatmap, plot_win_rate_by_quarter,
                     plot_win_prob_vs_margin, plot_home_away_wins)
import csv

#loading data
pbp_raw = load_playbyplay()

#processing data
pbp = process_playbyplay(pbp_raw)

#analyzing  data
show_correlations(pbp)
model = train_model(pbp)

url = 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event=401810801'
plays = espn_scores(url)

with open('lakers_twolves.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    for play in plays:
        margin = play['margin']
        secs = play['secs']
        description = play['description']
        prob = predict_win_probability(model, margin, secs)
        row = f"{description}: {prob:.2%}"
        # TODO: Get the play that had the biggest delta in win percentage.
        writer.writerow([row]) 

# Plotting data :D 
print("\nGenerating plots...")
plot_correlation_heatmap(pbp)
plot_win_rate_by_quarter(pbp)
plot_win_prob_vs_margin(model)
plot_home_away_wins(pbp)
print("\nAll plots saved to results/")