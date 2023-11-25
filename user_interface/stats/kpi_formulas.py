import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df_attacking = pd.read_csv('../../data_processing/raw_data/stats/attacking.csv')
df_attempts = pd.read_csv('raw_data/stats/attempts.csv')
df_defending = pd.read_csv('raw_data/stats/defending.csv')
df_disciplinary = pd.read_csv('raw_data/stats/disciplinary.csv')
df_distributon = pd.read_csv('raw_data/stats/distributon.csv')
df_goalkeeping = pd.read_csv('raw_data/stats/goalkeeping.csv')
df_goals = pd.read_csv('raw_data/stats/goals.csv')
df_key_stats = pd.read_csv('raw_data/stats/key_stats.csv')


def goalkeeper(player_id) :
    # Creating KPIs
    saved_goalkeeper = round(df_goalkeeping[df_goalkeeping['player_id'] == player_id]['saved'].sum(),2)
    conceded_goalkeeper = round(df_goalkeeping[df_goalkeeping['player_id'] == player_id]['conceded'].sum(),2)
    freekicks_taken_goalkeeper = round(df_distributon[df_distributon['player_id'] == player_id]['freekicks_taken'].sum(),2)
    saved_penalties_goalkeeper = round(df_goalkeeping[df_goalkeeping['player_id'] == player_id]['saved_penalties'].sum(),2)
    cleansheets_goalkeeper = round(df_goalkeeping[df_goalkeeping['player_id'] == player_id]['cleansheets'].sum(),2)

    # Storing KPIs in a dictionary
    output_goalkeeper = {
        "Saved goals" : saved_goalkeeper,
        "Conceded goals" : conceded_goalkeeper,
        "Freekicks" : freekicks_taken_goalkeeper,
        "Saved penalties" : saved_penalties_goalkeeper,
        "Cleansheets" : cleansheets_goalkeeper}

    return output_goalkeeper

def forward(player_id) :
    # Creating KPIs
    goals_forward = round(df_goals[df_goals['player_id'] == player_id]['goals'].sum(),2)
    goals_forwardpergame = round(df_goals[df_goals['player_id'] == player_id]['goals'].sum() / df_attempts[df_attempts['player_id'] == player_id]['match_played'].sum(),2)
    assists_forward = round(df_attacking[df_attacking['player_id'] == player_id]['assists'].sum(),2)
    assists_forwardpergame = round(df_attacking[df_attacking['player_id'] == player_id]['assists'].sum() / df_attempts[df_attempts['player_id'] == player_id]['match_played'].sum(),2)
    shots_on_target_forward = round(df_attempts[df_attempts['player_id'] == player_id]['on_target'].sum(),2)
    shots_on_target_pergame_forward = round(df_attempts[df_attempts['player_id'] == player_id]['on_target'].sum() / df_attempts[df_attempts['player_id'] == player_id]['match_played'].sum(),2)
    successful_dribbles_forward = round(df_attacking[df_attacking['player_id'] == player_id]['dribbles'].sum(),2)

    # Storing KPIs in a dictionary
    output_forward = {
        "Total goals" : goals_forward,
        "Goals per game" : goals_forwardpergame,
        "Total assists" : assists_forward,
        "Assists per game" : assists_forwardpergame,
        "Shots on target" : shots_on_target_forward,
        "Shots on target per game" : shots_on_target_pergame_forward,
        "Successful dribbles" : successful_dribbles_forward}

    return output_forward

def midfielder(player_id) :
    # Creating KPIs
    ball_recoveries_midfielder = round(df_defending[df_defending['player_id'] == player_id]['balls_recoverd'].sum() / df_defending[df_defending['player_id'] == player_id]['match_played'].sum(),2)
    pass_accuracy_midfielder = round(df_distributon[df_distributon['player_id'] == player_id]['pass_accuracy'].mean(),2)
    total_assists_midfielder = round(df_attacking[df_attacking['player_id'] == player_id]['assists'].sum(),2)
    key_passes_pergame_midfielder = round(total_assists_midfielder / df_attacking[df_attacking['player_id'] == player_id]['match_played'].sum(),2)

    # Storing KPIs in a dictionary
    output_midfielder = {
        'Total assists': total_assists_midfielder,
        'Ball Recoveries per Game': ball_recoveries_midfielder,
        'Pass Accuracy': pass_accuracy_midfielder,
        'Key passes per game': key_passes_pergame_midfielder,
        }

    return output_midfielder

def defender(player_id) :
    # Creating KPIs
    tackles_won_defender = round(df_defending[df_defending['player_id'] == player_id]['t_won'].sum(),2)
    tackles_won_pergame_defender = round(df_defending[df_defending['player_id'] == player_id]['t_won'].sum() / df_defending[df_defending['player_id'] == player_id]['match_played'].sum(),2)
    fouls_pergame_defender = round(df_disciplinary[df_disciplinary['player_id'] == player_id]['fouls_committed'].sum() / df_defending[df_defending['player_id'] == player_id]['match_played'].sum(),2)

    # Storing KPIs in a dictionary
    output_defender = {
            'Tackles Won' : tackles_won_defender,
            'Tackles Won per Game': tackles_won_pergame_defender,
            'Fouls Committed per Game': fouls_pergame_defender,
        }

    return output_defender

def general(player_id) :
    # Creating KPIs
    red_yellow_cards_total = df_disciplinary[df_disciplinary['player_id'] == player_id][['red', 'yellow']].sum().to_dict()
    return red_yellow_cards_total


def building_kpis(player_id) :
    general = general(player_id)

    if df_key_stats[df_key_stats["player_id"] == player_id]["position"] == "Goalkeeper" :
        kpi = goalkeeper(player_id)

    if df_key_stats[df_key_stats["player_id"] == player_id]["position"] == "Defender" :
        kpi = defender(player_id)

    if df_key_stats[df_key_stats["player_id"] == player_id]["position"] == "Midfielder" :
        kpi = midfielder(player_id)

    if df_key_stats[df_key_stats["player_id"] == player_id]["position"] == "Forward" :
        kpi = forward(player_id)

    return general, kpi
