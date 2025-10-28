import pandas as pd
import numpy as np
import json

# Custom JSON Encoder to handle NumPy types
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

# Read the IPL matches data from a public Google Sheet CSV.
ipl_matches = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRy2DUdUbaKx_Co9F0FSnIlyS-8kp4aKv_I0-qzNeghiZHAI_hw94gKG22XTxNJHMFnFVKsO4xWOdIs/pub?gid=1655759976&single=true&output=csv"
matches = pd.read_csv(ipl_matches)

# Read the IPL ball-by-ball data.
ipl_ball = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRu6cb6Pj8C9elJc5ubswjVTObommsITlNsFy5X0EiBY7S-lsHEUqx3g_M16r50Ytjc0XQCdGDyzE_Y/pub?output=csv"
balls = pd.read_csv(ipl_ball)

# Merge ball data with match data on 'ID'
ball_withmatch = pd.merge(balls, matches, on='ID', how='inner')

# Compute 'BowlingTeam' by concatenating 'Team1' and 'Team2', then removing the 'BattingTeam' substring.
ball_withmatch['BowlingTeam'] = ball_withmatch['Team1'] + ball_withmatch['Team2']
ball_withmatch['BowlingTeam'] = ball_withmatch[['BowlingTeam', 'BattingTeam']].apply(
    lambda x: x.iloc[0].replace(x.iloc[1], ''), axis=1

)

# Select relevant columns into batter_data.
batter_data = ball_withmatch.loc[:, np.append(balls.columns.values, ['BowlingTeam', 'Player_of_Match'])]

############################
# TEAM AND MATCH RECORDS
############################

def team1vsteam2(team1, team2):
    # Use query for clarity.
    df = matches.query(
        "((Team1 == @team1) and (Team2 == @team2)) or ((Team1 == @team2) and (Team2 == @team1))"
    )
    total_matches = len(df)
    win_counts = df['WinningTeam'].value_counts()
    team1_won = win_counts.get(team1, 0)
    team2_won = win_counts.get(team2, 0)
    no_result = total_matches - (team1_won + team2_won)
    return {
        'matchesplayed': total_matches,
        'won': int(team1_won),
        'loss': int(total_matches - team1_won - no_result),
        'noResult': int(no_result)
    }

def allRecord(team):
    # Filter rows where the team participated.
    df = matches.query("Team1 == @team or Team2 == @team")
    total_matches = len(df)
    won = df.query("WinningTeam == @team").shape[0]
    no_result = df['WinningTeam'].isna().sum()
    loss = total_matches - won - no_result
    title = df.query("MatchNumber == 'Final' and WinningTeam == @team").shape[0]
    return {
        'matchesplayed': total_matches,
        'won': won,
        'loss': loss,
        'noResult': no_result,
        'title': title
    }

def teamAPI(team, matches=matches):
    # Get records for matches involving the team.
    df = matches.query("Team1 == @team or Team2 == @team")
    self_record = allRecord(team)
    teams_list = matches['Team1'].unique()
    against = {opp: team1vsteam2(team, opp) for opp in teams_list}
    data = {team: {'overall': self_record, 'against': against}}
    return json.dumps(data, cls=NpEncoder)

############################
# BATSMAN RECORDS
############################

def batsmanRecord(batsman, df):
    if df.empty:
        return np.nan
    # Count dismissals (outs)
    out = df.query("player_out == @batsman").shape[0]
    # Filter rows for the specific batsman
    df_batsman = df.query("batter == @batsman")
    innings = df_batsman['ID'].nunique()
    runs = df_batsman['batsman_run'].sum()
    fours = df_batsman.query("batsman_run == 4 and non_boundary == 0").shape[0]
    sixes = df_batsman.query("batsman_run == 6 and non_boundary == 0").shape[0]
    avg = runs / out if out else np.inf
    nballs = df_batsman.query("extra_type != 'wides'").shape[0]
    strike_rate = runs / nballs * 100 if nballs else 0
    gb = df_batsman.groupby('ID').sum()
    fifties = gb.query("batsman_run >= 50 and batsman_run < 100").shape[0]
    hundreds = gb.query("batsman_run >= 100").shape[0]
    try:
        highest_score = gb['batsman_run'].max()
        hsindex = gb['batsman_run'].idxmax()
        # Check if the batsman was dismissed in the match corresponding to highest score.
        if (df_batsman.query("ID == @hsindex")['player_out'] == batsman).any():
            highest_score = str(highest_score)
        else:
            highest_score = str(highest_score) + '*'
    except Exception:
        highest_score = gb['batsman_run'].max()
    not_out = innings - out
    mom = df_batsman[df_batsman['Player_of_Match'] == batsman].drop_duplicates('ID').shape[0]
    return {
        'innings': innings,
        'runs': runs,
        'fours': fours,
        'sixes': sixes,
        'avg': avg,
        'strikeRate': strike_rate,
        'fifties': fifties,
        'hundreds': hundreds,
        'highestScore': highest_score,
        'notOut': not_out,
        'mom': mom
    }

def batsmanVsTeam(batsman, team, df):
    df_filtered = df.query("BowlingTeam == @team")
    return batsmanRecord(batsman, df_filtered)

def batsmanAPI(batsman, balls=batter_data):
    # Exclude super overs
    df = balls.query("innings in [1, 2]")
    self_record = batsmanRecord(batsman, df)
    teams_list = matches['Team1'].unique()
    against = {team: batsmanVsTeam(batsman, team, df) for team in teams_list}
    data = {batsman: {'all': self_record, 'against': against}}
    return json.dumps(data, cls=NpEncoder)

############################
# BOWLER RECORDS
############################

# Work on bowler data by computing additional columns
bowler_data = batter_data.copy()

# Use vectorized lambda with .apply(axis=1)
bowler_data['bowler_run'] = bowler_data.apply(
    lambda row: 0 if row['extra_type'] in ['penalty', 'legbyes', 'byes'] else row['total_run'], axis=1
)

bowler_data['isBowlerWicket'] = bowler_data.apply(
    lambda row: row['isWicketDelivery'] if row['kind'] in ['caught', 'caught and bowled', 'bowled', 'stumped', 'lbw', 'hit wicket'] else 0, axis=1
)

def bowlerRecord(bowler, df):
    df_bowler = df.query("bowler == @bowler")
    innings = df_bowler['ID'].nunique()
    nballs = df_bowler.query("extra_type not in ['wides', 'noballs']").shape[0]
    runs = df_bowler['bowler_run'].sum()
    eco = runs / nballs * 6 if nballs else 0
    fours = df_bowler.query("batsman_run == 4 and non_boundary == 0").shape[0]
    sixes = df_bowler.query("batsman_run == 6 and non_boundary == 0").shape[0]
    wicket = df_bowler['isBowlerWicket'].sum()
    avg = runs / wicket if wicket else np.inf
    strike_rate = nballs / wicket * 100 if wicket else np.nan
    gb = df_bowler.groupby('ID').sum()
    w3 = gb.query("isBowlerWicket >= 3").shape[0]
    best_fig = gb[['isBowlerWicket', 'bowler_run']].sort_values(by=['isBowlerWicket', 'bowler_run'], ascending=[False, True])
    best_fig_values = best_fig.head(1).values
    best_figure = f'{best_fig_values[0][0]}/{best_fig_values[0][1]}' if best_fig_values.size else np.nan
    mom = df_bowler[df_bowler['Player_of_Match'] == bowler].drop_duplicates('ID').shape[0]
    return {
        'innings': innings,
        'wicket': int(wicket),
        'economy': eco,
        'average': avg,
        'strikeRate': strike_rate,
        'fours': fours,
        'sixes': sixes,
        'best_figure': best_figure,
        '3+W': w3,
        'mom': mom
    }

def bowlerVsTeam(bowler, team, df):
    df_filtered = df.query("BattingTeam == @team")
    return bowlerRecord(bowler, df_filtered)

def bowlerAPI(bowler, balls=bowler_data):
    df = balls.query("innings in [1, 2]")  # Exclude super overs
    self_record = bowlerRecord(bowler, df)
    teams_list = matches['Team1'].unique()
    against = {team: bowlerVsTeam(bowler, team, df) for team in teams_list}
    data = {bowler: {'all': self_record, 'against': against}}
    return json.dumps(data, cls=NpEncoder)

