# Introduction - Live NBA Outcome Prediction
This project aims to predict the outcome of an NBA game. I utilize both historical and real-time data. Crucial data points include score, home court advantage, time remaining, and team salaries as a live probability is displayed for each play with a logistic regression model that is trained with over 3 million basketball plays.

# Data sources
I am currently using Kaggle NBA play-by-play data from seasons ranging from 2015-2021. [Kaggle NBA PBP](https://www.kaggle.com/datasets/schmadam97/nba-playbyplay-data-20182019)
I also used ESPN play-by-play data. As a test, I fetched the [Lakers vs. Timberwolves](https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event=401810801) game from March 10, 2026 as a proof of concept, but the notebook allows you to choose any matchup.
 Lastly, I utilized an NBA payroll dataset from [Kaggle](https://www.kaggle.com/datasets/loganlauton/nba-players-and-team-data). I inputted team salaries myself for this year.
 Not featured in notebooks, but also implemented in additional visualizations was a historic collection of team records from [Kaggle](https://www.kaggle.com/datasets/mharvnek/nba-team-stats-00-to-18). 

| # | Name | Source URL | Type | Fields | Format | Estimated Size |
|---|------|-----------|------|--------|--------|---------------|
| 1 | ESPN Undocumented API | site.api.espn.com | API | Score, time, player stats, team name, home/away team, location | JSON | 50,000 |
| 2 | Kaggle NBA Players & Team Data | basketball-reference.com/leagues/NBA_2026_games | File | teams, payrolls, seasons, | CSV | 180 |
| 3 | Kaggle Historical NBA Play-by-Play (2015-2021) | kaggle.com/datasets/schmadam97/nba-playbyplay-data-20182019 | File | Box score, player stats, play-by-play, game outcome | CSV | 3,000,000+ |

# Analysis
A logistic regression model is trained with over 3,000,000 NBA play-by-play data points to provide accurate win probabilities for NBA games as they happen in real time, with key features including score margin, time remaining, and payroll difference.  

# Results 
I have found that home teams win the game roughly 58% of the time and that there is a somewhat strong correlation between scoring margin and being the home team at 0.53. I've also learned that home teams win 74.9% of the time when leading at half time, and 90.8% when winning at the start of the fourth quarter. I've also gathered that the team with the higher payroll (team salary) won only roughly 58% of the games during the 2015 to 2021 NBA seasons.

# Installation
There are no API keys required at the moment. 

The following python packages were used: requests, pandas, sklearn, matplotlib, and seaborn. 
I used pandas to read play-by-play CSVs. 
I used requests to fetch data from ESPN.
I used sklearn to help with model training and creating the logistic regression model. 
I used matplotlib and seaborn to generate plots. 
Claude AI was also used to assist in parts of this project. They are labeled as such with '# AI Generated' notes in the code. 

# How to run
1. Install all requirements from `requirements.txt`

2. Download the following datasets and place in `data/` 
   - [Kaggle NBA PBP](https://www.kaggle.com/datasets/schmadam97/nba-playbyplay-data-20182019) 
   - [Kaggle Salaries](https://www.kaggle.com/datasets/loganlauton/nba-players-and-team-data) - rename to `Payrolls.csv`
   - [Kaggle Win % Info](https://www.kaggle.com/datasets/mharvnek/nba-team-stats-00-to-18) - rename to `Win_Pct.csv`

3. From `src/` directory run:

  `python3 main.py `

4. Results will appear in `results/` folder. All obtained will be stored in `data/`

# Running Notebooks
1. Ensure all datasets are downloaded from above (How to Run)
2. Open `src/results.ipynb` in Jupyter
3. Do `Restart & Run All` to run all cells
4. User input required at cells 11 and 12 for date and game selection (may show error at first if date not inputted)
5. On completion, a graph will be created displaying a play-by-play win probability for the home team throughout the selected game, with a comparison to ESPN's model too. 
