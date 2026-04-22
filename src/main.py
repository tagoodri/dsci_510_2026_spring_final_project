from load import load_playbyplay, espn_scores, load_payroll, load_win_pct
from process import process_playbyplay, process_payroll
from analyze import (show_correlations, train_model,
                    plot_correlation_heatmap, plot_win_rate_by_quarter,
                    plot_home_away_wins, plot_lead_win_rate, plot_upset_rate, plot_payroll_vs_winrate, plot_winrate_by_payroll_tier, analyze_game)

print("Starting NBA win probability!")
#loading data
pbp_raw = load_playbyplay()
payroll = load_payroll()
win_pct = load_win_pct()

#processing data
pbp = process_playbyplay(pbp_raw)
pbp = process_payroll(pbp, payroll)

#analyzing data
show_correlations(pbp)

model = train_model(pbp)
  
#Running espn stuff
game_id = '401810801' #Lakers vs. Timberwolves in March 2026, can change if want to see diff game
game_info = espn_scores(game_id)
analyze_game(game_info['plays_list'], model, game_info['home_team'], game_info['away_team'],game_info['home_team_color'])

# Plotting data :D  
print("\nMaking plots") 
plot_correlation_heatmap(pbp) 
plot_win_rate_by_quarter(pbp)
plot_home_away_wins(pbp)
plot_lead_win_rate(pbp)
plot_upset_rate(pbp)
plot_payroll_vs_winrate(payroll, win_pct)
plot_winrate_by_payroll_tier(payroll, win_pct)
print("\nAll plots saved to results/")