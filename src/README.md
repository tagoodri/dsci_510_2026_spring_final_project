# Live NBA Outcome Prediction
This project aims to predict the outcome of an NBA game. I utilize both historical and real-time data. Crucial data points include score, home court advantage, time remaining, and more as I plan to display a live probability of the possible outcomes with a logistic regression model that is trained with over 3 million basketball plays.

# Data sources
I am currently using Kaggle NBA play-by-play data from seasons ranging from 2015-2021. [Kaggle NBA PBP](https://www.kaggle.com/datasets/schmadam97/nba-playbyplay-data-20182019)
I also used ESPN play-by-play data. As a test thus far, I fetched the [Lakers vs. Timberwolves](https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event=401810801) game from March 10 2026.
I am going to utilize NBA scheduling data from [Basketball Reference](https://www.basketball-reference.com/leagues/NBA_2016_games.html).

| # | Name | Source URL | Type | Fields | Format | Estimated Size |
|---|------|-----------|------|--------|--------|---------------|
| 1 | ESPN Undocumented API | site.api.espn.com | API | Score, time, player stats, team name, home/away team, location | JSON | 50,000 |
| 2 | Basketball Reference Schedule | basketball-reference.com/leagues/NBA_2026_games | Webpage | Schedule, timing, days off, home/away team, location, date, time | CSV | 1,230 |
| 3 | Kaggle Historical NBA Play-by-Play (2015-2021) | kaggle.com/datasets/schmadam97/nba-playbyplay-data-20182019 | File | Box score, player stats, play-by-play, game outcome | CSV | 3,000,000+ |


# Results 
Thus far I have found that home teams win the game roughly 58% of the time and that there is a somewhat strong correlation between scoring margin and being the home team at 0.53. I've also learned that home teams win 74.9% of the time when leading at half time, and 90.8% when winning at the start of the fourth quarter. These are the main results thus far, as I continue to gather and process more data. 

# Installation
There are no API keys required at the moment. 

The following python packages were used: requests, pandas, sklearn. 
I used pandas to read play-by-play CSVs. 
I used requests to fetch data from ESPN.
I used sklearn to help with model training and creating the logistic regression model. 
I used matplotlib to generate plots. 

# Running analysis 

From `src/` directory run:

`python3 main.py `

Results will appear in `results/` folder. All obtained will be stored in `data/`
