import pandas as pd
from process import process_playbyplay, process_payroll 
from analyze import train_model, predict_win_probability

def fake_data():
    # Fake dataset to test, but making more rows and instances for the model to have just enough data
    return pd.DataFrame({
        'WinningTeam': ['LAL'] * 100 + ['BOS'] * 100, #using abrvs for fake for now
        'AwayTeam':    ['BOS'] * 200,
        'HomeTeam':    ['LAL'] * 200,
        'AwayScore':   [90] * 200,
        'HomeScore':   [100] * 100 + [80] * 100,
        'Quarter':     [4] * 200,
        'SecLeft':     [0] * 200,
        'PayrollDiff': [15000000] * 200,
        'Date':        ['October 1 2019'] * 200, #placeholder, will be implemented with schedule data hopefully ;(
        'Location':    ['LA'] * 200, #placeholder, will be implemented with schedule data later ;( 

    })
def fake_payroll():
    # Fake payroll info to test
    return pd.DataFrame({
        'team': ['LA Lakers', 'Boston'],
        'seasonStartYear': [2019, 2019],
        'inflationAdjPayroll': [120000000, 110000000]
    })

def test_payroll_merge():
    # Test merge fake payroll and data 
    df = process_playbyplay(fake_data())
    payroll = fake_payroll()
    merged = process_payroll(df, payroll)
    print(merged['PayrollDiff'])

def test_home_win():
    # Double checking home win is done right
    df = process_playbyplay(fake_data())
    print(df['HomeWin'])


def test_processing():
    # confirm processing works alright 
    df = process_playbyplay(fake_data())
    print(df.columns)


def test_predictions():
    # Check that lopsided scores give obvious probabilities
    df = process_playbyplay(fake_data())
    df['PayrollDiff'] = 0 #setting salary to zero for now to make testing easier and level playing field of payroll 

    model = train_model(df)

    up30 = predict_win_probability(model, score_margin=30, seconds_left=60, payroll_diff=0)
    #confriming accuracy given up a lot with a little time
    down30 = predict_win_probability(model, score_margin=-30, seconds_left=60, payroll_diff=0)
    #confriming accuracy given down a lot with a little time

    print(f"Up 30 with 1 min left: {up30:.2%}")
    print(f"Down 30 with 1 min left: {down30:.2%}")
    

#check tests
if __name__ == "__main__":
    print("Running simple tests! \n")
    test_processing()
    test_predictions()
    test_payroll_merge()
    test_home_win()
  