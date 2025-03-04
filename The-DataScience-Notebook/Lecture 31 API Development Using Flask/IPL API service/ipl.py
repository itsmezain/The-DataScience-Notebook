# this file contain all the logic of our API

# data analysis ipl.ipynb file me hia  

import numpy as np
import pandas as pd

ipl_matches = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRy2DUdUbaKx_Co9F0FSnIlyS-8kp4aKv_I0-qzNeghiZHAI_hw94gKG22XTxNJHMFnFVKsO4xWOdIs/pub?gid=1655759976&single=true&output=csv"
matches = pd.read_csv(ipl_matches)


def teamsAPI():
    teams = list(set(list(matches['Team1']) + list(matches['Team2'])))
    
    team_dict = {
        'teams': teams
    }
    
    return team_dict

def teamVteamAPI(team1, team2):
    # Use proper parentheses to ensure correct evaluation of conditions:
    
    valid_teams = list(set(list(matches['Team1']) + list(matches['Team2'])))

    if team1 in valid_teams and team2 in valid_teams:
        temp_df = matches[((matches['Team1'] == team1) & (matches['Team2'] == team2)) |
                      ((matches['Team1'] == team2) & (matches['Team2'] == team1))]
    
        total_matches = temp_df.shape[0]
    
    # Use .get() with default value 0 to avoid KeyError if team didn't win any match.
        win_counts = temp_df['WinningTeam'].value_counts()
        team1_won = win_counts.get(team1, 0)
        team2_won = win_counts.get(team2, 0)
    
        no_result = total_matches - (team1_won + team2_won)
    
        result_dict = {
            'total_matches': total_matches,
            team1: int(team1_won),
            team2: int(team2_won),
            'no_result': int(no_result)
        }
    
        return result_dict
    
    else:
        return {'message':'invalid team name'}

