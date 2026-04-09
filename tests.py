import pandas as pd
from process import process_playbyplay
from analyze import train_model, predict_win_probability

def fake_data():
    # Fake dataset to test, but making more rows and instances for the model to have just enough data
    return pd.DataFrame({
        'WinningTeam': ['LAL'] * 100 + ['BOS'] * 100,
        'AwayTeam':    ['BOS'] * 200,
        'HomeTeam':    ['LAL'] * 200,
        'AwayScore':   [90] * 200,
        'HomeScore':   [100] * 100 + [80] * 100,
        'Quarter':     [4] * 200,
        'SecLeft':     [0] * 200,
        'Date':        ['January 1 2020'] * 200, #placeholder, will be implemented with schedule data
        'Location':    ['LA'] * 200 #placeholder, will be implemented with schedule data

    })
def test_processing():
    # confirm processing works alright 
    df = process_playbyplay(fake_data())
    print("Columns created:", df.columns.tolist())


def test_predictions():
    # Check that lopsided scores give obvious probabilities
    df = process_playbyplay(fake_data())
    model = train_model(df)

    up30 = predict_win_probability(model, score_margin=30, seconds_left=60)
    #confriming accuracy given up a lot with a little time
    down30 = predict_win_probability(model, score_margin=-30, seconds_left=60)
    #confriming accuracy given down a lot with a little time


    print(f"Up 30 with 1 min left: {up30:.2%}")
    print(f"Down 30 with 1 min left: {down30:.2%}")

#check tests
if __name__ == "__main__":
    test_processing()
    test_predictions()