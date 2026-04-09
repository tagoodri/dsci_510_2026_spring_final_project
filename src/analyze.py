import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from config import results_dir, test_size, random_state


def show_correlations(df):
    #Find main correlations between core variables and winning 
    print("\nCorrelations with HomeWin:")
    corr_cols = ['ScoreMargin', 'TotalSecLeft', 'HomeWin']
    print(df[corr_cols].corr())


def train_model(df):
    #train lr model
    X = df[['ScoreMargin', 'TotalSecLeft']]
    y = df['HomeWin']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    model = LogisticRegression()
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"\nModel Accuracy: {accuracy:.2%}")

    return model


def predict_win_probability(model, score_margin, seconds_left):
    # Show prob of home team winning in a real game scenario 
    play = pd.DataFrame({
        'ScoreMargin': [score_margin],
        'TotalSecLeft': [seconds_left]
    })
    prob = model.predict_proba(play)[0][1]
    return prob


def plot_correlation_heatmap(df):
    # main heatmap between variables

    corr = df[['ScoreMargin', 'TotalSecLeft', 'HomeWin']].corr()

    plt.figure(figsize=(8, 6))
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

    plt.figure(figsize=(8, 6))
    plt.bar([f'Q{q}' for q in quarters], win_rates, color='gold')
    plt.title('Win Rate When Home Team Leading at Each Quarter')
    plt.ylabel('Win Rate (%)')
    plt.ylim(0, 100)
    for i, v in enumerate(win_rates):
        plt.text(i, v + 1, f'{v:.1f}%', ha='center')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'win_rate_by_quarter.png'))
    plt.show()
    plt.close()
    print("Saved: win_rate_by_quarter.png")


def plot_win_prob_vs_margin(model):
    # line chart with win prob and scoring margin
    margins = range(-30, 31)
    probs = [predict_win_probability(model, m, 720) for m in margins]

    plt.figure(figsize=(10, 6))
    plt.plot(margins, probs, color='purple')
    plt.axhline(0.5, color='gray', linestyle='--')
    plt.axvline(0, color='gray', linestyle='--')
    plt.title('Win Probability vs Score Margin (Q3 Start)')
    plt.xlabel('Score Margin (positive = home team leading)')
    plt.ylabel('Home Team Win Probability')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'win_prob_vs_margin.png'))
    plt.show()
    plt.close()
    print("Saved: win_prob_vs_margin.png")


def plot_home_away_wins(df):
    # simple bar chart showing home vs away wins
    games = df.groupby(['Date', 'HomeTeam', 'AwayTeam']).last().reset_index()

    home_wins = games['HomeWin'].sum()
    away_wins = len(games) - home_wins

    plt.figure(figsize=(6, 6))
    plt.bar(['Home Wins', 'Away Wins'], [home_wins, away_wins], color=['purple', 'gold'])
    plt.title('Home vs Away Wins (2015-2021)')
    plt.ylabel('Number of Wins')
    for i, v in enumerate([home_wins, away_wins]):
        plt.text(i, v + 5, str(v), ha='center')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'home_away_wins.png'))
    plt.show()
    plt.close()
    print("Saved: home_away_wins.png")