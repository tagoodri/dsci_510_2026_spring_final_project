import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from load import load_payroll
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from config import results_dir, test_size, random_state, plot_size, plot_size_smallish


def show_correlations(df):
    #Find main correlations between core variables and winning 
    print("\nCorrelations with HomeWin:")
    corr_cols = ['ScoreMargin', 'TotalSecLeft','PayrollDiff', 'HomeWin']
    print(df[corr_cols].corr())


def train_model(df):
    #train lr model
    X = df[['ScoreMargin', 'TotalSecLeft', 'PayrollDiff']]
    y = df['HomeWin']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    
    model = LogisticRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)

    print(f"Model Accuracy: {accuracy:.2%}")
    print(f"Mean Squared Error: {mse:.2f}")

    return model

def get_team_payroll(team):
    # Main Payroll stuff
    payrolls = load_payroll()
    value = payrolls.loc[(payrolls['team'] == team) & (payrolls['seasonStartYear'] == 2025), 'inflationAdjPayroll'] #using loc from class
    team_payroll = value.values[0]
    return team_payroll



def predict_win_probability(model, score_margin, seconds_left, payroll_diff = 0 ):
    # Show prob of home team winning in a real game scenario 
    play = pd.DataFrame({
        'ScoreMargin': [score_margin],
        'TotalSecLeft': [seconds_left],
        'PayrollDiff': [payroll_diff]
    })

    prob = model.predict_proba(play)[0][1]
    return prob


def plot_correlation_heatmap(df):
    # main heatmap between variables, using seaborn

    # used this seaborn guide: https://seaborn.pydata.org/generated/seaborn.heatmap.html
    corr = df[['ScoreMargin', 'TotalSecLeft','PayrollDiff','HomeWin']].corr()

    corr.columns = ['Score Margin', 'Time Remaining', 'Payroll Difference', 'Home Team Win']
    corr.index = ['Score Margin', 'Time Remaining', 'Payroll Difference', 'Home Team Win']

    plt.figure(figsize=plot_size_smallish)
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'correlation_heatmap.png'))
    plt.show()
    plt.close()
    print("Saved: correlation_heatmap.png")

# *using purple and gold for lakers colors :D*

def plot_win_rate_by_quarter(df):
    # bar cheart revealing higher win prob as game progresses (by quarter)
    quarters = [1, 2, 3, 4]
    win_rates = []

    for q in quarters:
        subset = df[df['Quarter'] == q]
        leading = subset[subset['ScoreMargin'] > 0]
        win_rate = (leading['HomeWin'] == 1).mean()
        win_rates.append(win_rate * 100)

    plt.figure(figsize=plot_size_smallish)
    plt.bar([f'Q{q}' for q in quarters], win_rates, color='gold')
    plt.title('Win Rate When Home Team Leading at Each Quarter')
    plt.ylabel('Win Rate (%)')
    plt.ylim(0, 100)
    for i, v in enumerate(win_rates): #adds percentage for each bar.. learned from this tutorial https://www.tutorialspoint.com/article/how-to-display-percentage-above-a-bar-chart-in-matplotlib
        plt.text(i, v + 1, f'{v:.1f}%', ha='center')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'win_rate_by_quarter.png'))
    plt.show()
    plt.close()
    print("Saved: win_rate_by_quarter.png")


# def plot_win_prob_vs_margin(model):
#     # Seems to show that the model learned something weird in the data, don't provide in slides/notebooks
    
#     # line chart with win prob and scoring margin thru all 4 quarters

#     margins = range(-30, 31) # max scoring margin for sake of excluding outlier blowout games
    
#     plt.figure(figsize=plot_size)
#     for secs, label in [(2160, 'Q1'), (1440, 'Q2'), (720, 'Q3'), (60, 'Q4')]:
#         probs = [predict_win_probability(model, m, secs, payroll_diff=0) for m in margins]
#         plt.plot(margins, probs, label=label)
        
    
#     plt.axhline(0.5, color='gray', linestyle='--') #midway marker 
#     plt.axvline(0, color='gray', linestyle='--') #midway marker
#     plt.title('Win Probability vs Score Margin by Quarter')
#     plt.xlabel('Score Margin')
#     plt.ylabel('Home Team Win Probability')
#     plt.legend()
#     plt.tight_layout()
#     plt.savefig(os.path.join(results_dir, 'win_prob_vs_margin.png'))
#     plt.show()
#     plt.close()
#     print()
#     print("Saved: wins_with_margins.png")


def plot_espn_vs_model(my_probs, plays, home_team, away_team, home_team_color):
    # chart win probs for my model vs. ESPN's to see how they compare
    elapsed = []
    espn_probs = []

    for play in plays:
        elapsed.append(2880 - play['secs'])
        espn_probs.append(play['espn_win_percentage'])
        
    plt.axhline(0.5, color='gray', linestyle='--') # line to mark 50% threshold, putting first so in background
    plt.plot(elapsed, my_probs, label="My Model", color = f'#{home_team_color}') #putting hex color code of home team 
    plt.plot(elapsed, espn_probs, label="ESPN Model", color = 'black') #just making this one black so not any confusion w/ colors
    plt.title(f'{home_team} vs {away_team}')
    plt.ylabel(f'Home Win Probability ({home_team})')
    plt.xticks([0, 720, 1440, 2160, 2880], ['Q1', 'Q2', 'Q3', 'Q4', 'End']) #change ticks to start of quarter (seconds)
    plt.ylim(0, 1) # make sure to go till full 100p
    plt.xlim(elapsed[0], elapsed[-1]) #ensure it starts at first play and ends at lasst 
    plt.legend()
    plt.savefig(os.path.join(results_dir, f'espn_vs_model.png'))
    plt.show()
    plt.close()
    print("saved:espn_vs_model.png")


def plot_home_away_wins(df):
    # simple bar chart showing home vs away wins
    games = df.groupby(['Date', 'HomeTeam', 'AwayTeam']).last().reset_index()

    home_wins = games['HomeWin'].sum()
    away_wins = len(games) - home_wins

    plt.figure(figsize=(6, 6))
    plt.bar(['Home Wins', 'Away Wins'], [home_wins, away_wins], color=['purple', 'gold'])
    plt.title('Home vs Away Wins (2015-2021)')
    plt.ylabel('Number of Wins')
    for i, v in enumerate([home_wins, away_wins]): #adds percentage for each bar.. learned from this tutorial https://www.tutorialspoint.com/article/how-to-display-percentage-above-a-bar-chart-in-matplotlib
        plt.text(i, v + 5, str(v), ha='center')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'home_away_wins.png'))
    plt.show()
    plt.close()
    print("Saved: home_away_wins.png")

#*** AI USE: Asked AI (Claude) to help build me a graph that followed the structure of a previous one I had inputted, but tracked the lead better for 5 and 10 point leads***
def plot_lead_win_rate(df):
    # checking win rate during all 4 quarters when up by 5 and when up by 10, trying as way to standardize

    quarters = [1, 2, 3, 4]
    win_rate_2 = []
    win_rate_5 = []
    win_rate_10 = []

    win_rate_trailing_2 = []
    win_rate_trailing_5 = []
    win_rate_trailing_10 = []
    for q in quarters:
        # get last play of each quarter
        end_of_quarter = df[df['Quarter'] == q].groupby(['Date', 'HomeTeam', 'AwayTeam']).last().reset_index()
        
        leading_2 = end_of_quarter[(end_of_quarter['ScoreMargin'] >= 1) & (end_of_quarter['ScoreMargin'] <= 3)]
        leading_5 = end_of_quarter[(end_of_quarter['ScoreMargin'] >= 4) & (end_of_quarter['ScoreMargin'] <= 6)]
        leading_10 = end_of_quarter[(end_of_quarter['ScoreMargin'] >= 9) & (end_of_quarter['ScoreMargin'] <= 11)]

        trailing_2 = end_of_quarter[(end_of_quarter['ScoreMargin'] >= -3) & (end_of_quarter['ScoreMargin'] <= -1)]
        trailing_5 = end_of_quarter[(end_of_quarter['ScoreMargin'] >= -6) & (end_of_quarter['ScoreMargin'] <= -4)]
        trailing_10 = end_of_quarter[(end_of_quarter['ScoreMargin'] >= -11) & (end_of_quarter['ScoreMargin'] <= -9)]

        win_rate_2.append((leading_2['HomeWin'] == 1).mean() * 100)
        win_rate_5.append((leading_5['HomeWin'] == 1).mean() * 100)
        win_rate_10.append((leading_10['HomeWin'] == 1).mean() * 100)

        win_rate_trailing_2.append((trailing_2['HomeWin'] == 1).mean() * 100)
        win_rate_trailing_5.append((trailing_5['HomeWin'] == 1).mean() * 100)
        win_rate_trailing_10.append((trailing_10['HomeWin'] == 1).mean() * 100)

    plt.figure(figsize=plot_size_smallish)

    plt.plot([f'Q{q}' for q in quarters], win_rate_2, marker='o', label='~2 point lead', color='gray')
    plt.plot([f'Q{q}' for q in quarters], win_rate_5, marker='o', label='~5 point lead', color='purple')
    plt.plot([f'Q{q}' for q in quarters], win_rate_10, marker='o', label='~10 point lead', color='gold')

    plt.plot([f'Q{q}' for q in quarters], win_rate_trailing_2, marker='o', label='~2 point deficit', color='gray', linestyle='--')
    plt.plot([f'Q{q}' for q in quarters], win_rate_trailing_5, marker='o', label='~5 point deficit', color='purple', linestyle='--')
    plt.plot([f'Q{q}' for q in quarters], win_rate_trailing_10, marker='o', label='~10 point deficit', color='gold', linestyle='--')

    plt.title('Win Rate When Leading or Trailing by 2, 5, or 10 at End of Each Quarter')
    plt.ylabel('Win Rate (%)')
    plt.ylim(0, 100)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'lead_win_rate.png'))
    plt.show()
    plt.close()
    print("Saved: lead_win_rate.png")

def plot_upset_rate(df):
    # Get one row per game
    games = df.groupby(['Date', 'HomeTeam', 'AwayTeam']).last().reset_index()

    upsets = 0
    total = 0

    for thing, game in games.iterrows():
        home_payroll = game['HomePayroll']
        away_payroll = game['AwayPayroll']
        home_won = game['HomeWin']

        if home_payroll != away_payroll: #doubtful but making sure salaries arent equal
            total += 1
            if home_payroll < away_payroll and home_won == 1: # 1 since binary w/l for home
                upsets += 1
            elif away_payroll < home_payroll and home_won == 0: # 0 since binary w/l for away too 
                upsets += 1

    upset_rate = upsets / total * 100
    non_upset_rate = 100 - upset_rate

    plt.figure(figsize=(6, 6))
    plt.bar(['Higher Payroll Wins', 'Lower Payroll Wins'],
            [non_upset_rate, upset_rate],
            color=['purple', 'gold'])
    plt.title('How Often Does the Higher Payroll Team Win?')
    plt.ylabel('Percentage of Games (%)')
    plt.ylim(0, 100)
    for i, v in enumerate([non_upset_rate, upset_rate]):#adds percentage for each bar.. learned from this tutorial https://www.tutorialspoint.com/article/how-to-display-percentage-above-a-bar-chart-in-matplotlib
        plt.text(i, v + 1, f'{v:.1f}%', ha='center')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'upset_rate.png'))
    plt.show()
    plt.close()
    print("Saved: upset_rate.png")

def plot_payroll_vs_winrate(payroll_df, win_pct_df):
    #scatter of win rate in whole szn vs payroll
    merged = payroll_df.merge(win_pct_df, on=['team', 'seasonStartYear'])
    #merge team w team win rate 
    plt.figure(figsize=plot_size)
    sns.regplot(data=merged, x='inflationAdjPayroll', y='win_percentage', scatter_kws={'alpha':0.6, 'color':'purple'}, line_kws={'color':'gold'})
    #alpha is used for transparency to see different points if they overlap
    #refering to this seaborn guide: https://seaborn.pydata.org/generated/seaborn.regplot.html
    #using seaborn in particular for line to see trend

    plt.xlabel('Inflation Adjusted Payroll ($)')
    plt.ylabel('Win Rate')
    plt.title('Payroll vs Win Rate per Team per Season (2015-2021)')
    plt.ticklabel_format(style='plain', axis='x')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'payroll_vs_winrate.png'))
    plt.show()
    plt.close()
    print("Saved: payroll_vs_winrate.png")



# *** AI USE: Prompted AI (Claude) to give me a graph similar to the ones I had already created that shows different 'buckets' and tiers of salary and win rate***
# Not using for presentation, just for own findings to see impact/differences in payroll 
def plot_winrate_by_payroll_tier(payroll_df, win_pct_df):

    merged = payroll_df.merge(win_pct_df, on=['team', 'seasonStartYear'])
    
    merged['tier'] = pd.qcut(merged['inflationAdjPayroll'], q=3, labels=['Low Payroll', 'Mid Payroll', 'High Payroll'])
    
    avg_win_rate = merged.groupby('tier', observed=True)['win_percentage'].mean()   

    plt.figure(figsize=plot_size_smallish)
    plt.bar(avg_win_rate.index, avg_win_rate.values, color=['gold', 'gray', 'purple'])
    plt.title('Average Win Rate by Payroll Tier')
    plt.ylabel('Average Win Rate')
    plt.ylim(avg_win_rate.min() * 0.9, avg_win_rate.max() * 1.1)
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'winrate_by_payroll_tier.png'))
    plt.show()
    plt.close()
    print("Saved: winrate_by_payroll_tier.png")


def analyze_game(plays, model, home_team, away_team, home_team_color):
    #sorting thru ESPN, finding espn prob, my prob, and difference 
    my_probs = [] 
    filename = f'{away_team}@{home_team}.csv'
    filepath = (os.path.join(results_dir, filename))
    home_payroll = get_team_payroll(home_team)
    away_payroll = get_team_payroll(away_team)
    difference_payroll = home_payroll - away_payroll
    
    with open(filepath, 'w', encoding='utf-8') as file:

        number_plays = len(plays)
        total_diff = 0 #setting difference between the two models as 0 for now
        for play in plays:
            margin = play['margin']
            secs = play['secs']
            description = play['description']
            espn_prob = play['espn_win_percentage']
            prob = predict_win_probability(model, margin, secs, difference_payroll)
            my_probs.append(prob)  #putting in my model from plot so it can exist for rest 
            diff = abs(prob - espn_prob) #finding difference between my model and espn's (in abs value so the numbers dont cancel out)
            total_diff += diff #adds per each row
            row = f"{description}: ty's probability: {prob:.2%}, ESPN's probability:{espn_prob:.2%}, difference: {diff:.2%}\n"
            file.write(row)
        difference_tot = total_diff/number_plays
        file.write(f'Average diff: {difference_tot:.2%}\n')

    
    plot_espn_vs_model(my_probs, plays, home_team, away_team, home_team_color)
    
    #Finding the play that had the biggest delta in win percentage (aka the biggest sway/play of the game)
    biggest_delta = 0
    biggest_play = None

    # will show during live game, no matter how far along! 
    for i in range(1, len(plays)):
        delta = abs(my_probs[i] - my_probs[i-1])
        if delta > biggest_delta:
            biggest_delta = delta
            biggest_play = plays[i]
    descrip = biggest_play['description']
    print(f'Biggest play: {descrip}')