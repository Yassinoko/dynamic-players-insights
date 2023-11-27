import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df_attacking = pd.read_csv('stats/stats_data/attacking.csv')
df_attempts = pd.read_csv('stats/stats_data/attempts.csv')
df_defending = pd.read_csv('stats/stats_data/defending.csv')
df_disciplinary = pd.read_csv('stats/stats_data/disciplinary.csv')
df_distributon = pd.read_csv('stats/stats_data/distributon.csv')
df_goalkeeping = pd.read_csv('stats/stats_data/goalkeeping.csv')
df_goals = pd.read_csv('stats/stats_data/goals.csv')
df_key_stats = pd.read_csv('stats/stats_data/key_stats.csv')
#     general = general(player_id)

#     if df_key_stats[df_key_stats["player_id"] == player_id]["position"] == "Goalkeeper" :
#         kpi = goalkeeper(player_id)

#     if df_key_stats[df_key_stats["player_id"] == player_id]["position"] == "Defender" :
#         kpi = defender(player_id)

#     if df_key_stats[df_key_stats["player_id"] == player_id]["position"] == "Midfielder" :
#         kpi = midfielder(player_id)

#     if df_key_stats[df_key_stats["player_id"] == player_id]["position"] == "Forward" :
#         kpi = forward(player_id)

#     return general, kpi


def forward(player_name):
    player_name = player_name.lower()
    # Creating KPIs
    goals_forward = df_goals[df_goals['player_name'].str.lower() == player_name]['goals'].sum()
    goals_forwardpergame = np.nan_to_num(round(
        goals_forward / np.where(
            df_attempts[df_attempts['player_name'].str.lower() == player_name]['match_played'].sum() == 0,
            1,
            df_attempts[df_attempts['player_name'].str.lower() == player_name]['match_played'].sum()
        ),
        2
    ))

    assists_forward = df_attacking[df_attacking['player_name'].str.lower() == player_name]['assists'].sum()
    assists_forwardpergame = np.nan_to_num(round(
        assists_forward / np.where(
            df_attempts[df_attempts['player_name'].str.lower() == player_name]['match_played'].sum() == 0,
            1,
            df_attempts[df_attempts['player_name'].str.lower() == player_name]['match_played'].sum()
        ),
        2
    ))

    shots_on_target_forward = df_attempts[df_attempts['player_name'].str.lower() == player_name]['on_target'].sum()
    shots_on_target_pergame_forward = np.nan_to_num(round(
        shots_on_target_forward / np.where(
            df_attempts[df_attempts['player_name'].str.lower() == player_name]['match_played'].sum() == 0,
            1,
            df_attempts[df_attempts['player_name'].str.lower() == player_name]['match_played'].sum()
        ),
        2
    ))

    successful_dribbles_forward = df_attacking[df_attacking['player_name'].str.lower() == player_name]['dribbles'].sum()

    # Storing KPIs in a dictionary
    output_forward = {
        "Total goals": goals_forward,
        "Goals per game": goals_forwardpergame,
        "Total assists": assists_forward,
        "Assists per game": assists_forwardpergame,
        "Shots on target": shots_on_target_forward,
        "Shots on target per game": shots_on_target_pergame_forward,
        "Successful dribbles": successful_dribbles_forward
    }

    return output_forward

def midfielder(player_name):
    player_name = player_name.lower()
    # Creating KPIs
    ball_recoveries_midfielder = np.nan_to_num(round(
        df_defending[df_defending['player_name'].str.lower() == player_name]['balls_recoverd'].sum() / np.where(
            df_defending[df_defending['player_name'].str.lower() == player_name]['match_played'].sum() == 0,
            1,
            df_defending[df_defending['player_name'].str.lower() == player_name]['match_played'].sum()
        ),
        2
    ))

    pass_accuracy_midfielder = np.nan_to_num(round(
        df_distributon[df_distributon['player_name'].str.lower() == player_name]['pass_accuracy'].mean(),
        2
    ))

    total_assists_midfielder = df_attacking[df_attacking['player_name'].str.lower() == player_name]['assists'].sum()
    key_passes_pergame_midfielder = np.nan_to_num(round(
        total_assists_midfielder / np.where(
            df_attacking[df_attacking['player_name'].str.lower() == player_name]['match_played'].sum() == 0,
            1,
            df_attacking[df_attacking['player_name'].str.lower() == player_name]['match_played'].sum()
        ),
        2
    ))

    # Storing KPIs in a dictionary
    output_midfielder = {
        'Total assists': total_assists_midfielder,
        'Ball Recoveries per Game': ball_recoveries_midfielder,
        'Pass Accuracy': pass_accuracy_midfielder,
        'Key passes per game': key_passes_pergame_midfielder
    }

    return output_midfielder

def defender(player_name):
    player_name = player_name.lower()
    # Creating KPIs
    tackles_won_defender = round(
        df_defending[df_defending['player_name'].str.lower() == player_name]['t_won'].sum(),
        2
    )

    matches_played = df_defending[df_defending['player_name'].str.lower() == player_name]['match_played'].sum()
    tackles_won_pergame_defender = np.nan_to_num(round(
        df_defending[df_defending['player_name'].str.lower() == player_name]['t_won'].sum() / np.where(
            matches_played == 0,
            1,
            matches_played
        ),
        2
    ))

    fouls_pergame_defender = np.nan_to_num(round(
        df_disciplinary[df_disciplinary['player_name'].str.lower() == player_name]['fouls_committed'].sum() / np.where(
            matches_played == 0,
            1,
            matches_played
        ),
        2
    ))

    # Storing KPIs in a dictionary
    output_defender = {
        'Tackles Won': tackles_won_defender,
        'Tackles Won per Game': tackles_won_pergame_defender,
        'Fouls Committed per Game': fouls_pergame_defender
    }

    return output_defender

def goalkeeper(player_name):
    player_name = player_name.lower()
    # Creating KPIs
    saved_goalkeeper = round(
        df_goalkeeping[df_goalkeeping['player_name'].str.lower() == player_name]['saved'].sum(),
        2
    )

    conceded_goalkeeper = round(
        df_goalkeeping[df_goalkeeping['player_name'].str.lower() == player_name]['conceded'].sum(),
        2
    )

    freekicks_taken_goalkeeper = round(
        df_distributon[df_distributon['player_name'].str.lower() == player_name]['freekicks_taken'].sum(),
        2
    )

    saved_penalties_goalkeeper = round(
        df_goalkeeping[df_goalkeeping['player_name'].str.lower() == player_name]['saved_penalties'].sum(),
        2
    )

    cleansheets_goalkeeper = round(
        df_goalkeeping[df_goalkeeping['player_name'].str.lower() == player_name]['cleansheets'].sum(),
        2
    )

    # Storing KPIs in a dictionary
    output_goalkeeper = {
        "Saved goals": saved_goalkeeper,
        "Conceded goals": conceded_goalkeeper,
        "Freekicks": freekicks_taken_goalkeeper,
        "Saved penalties": saved_penalties_goalkeeper,
        "Cleansheets": cleansheets_goalkeeper
    }

    return output_goalkeeper

def general(player_name):
    # Creating KPIs
    player_name = player_name.lower()
    disciplinary_data = df_disciplinary[df_disciplinary['player_name'].str.lower() == player_name][['red', 'yellow']]
    red_yellow_cards_total = disciplinary_data.sum().to_dict()

    # Handling potential NaN values
    for key in red_yellow_cards_total:
        red_yellow_cards_total[key] = 0 if np.isnan(red_yellow_cards_total[key]) else red_yellow_cards_total[key]

    return red_yellow_cards_total

def building_kpis(player_name):
    player_name_lower = player_name.lower()
    player_position = df_key_stats[df_key_stats["player_name"].str.lower() == player_name_lower]["position"].iloc[0]

    if player_position == "Goalkeeper":
        kpi = goalkeeper(player_name_lower)
    elif player_position == "Defender":
        kpi = defender(player_name_lower)
    elif player_position == "Midfielder":
        kpi = midfielder(player_name_lower)
    elif player_position == "Forward":
        kpi = forward(player_name_lower)

    general_stats = general(player_name_lower)
    return general_stats, kpi

def plot_stats(disciplinary_stats, offensive_stats):
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # Plot for disciplinary stats
    axs[0].bar(disciplinary_stats.keys(), disciplinary_stats.values(), color=['red', 'yellow'])
    axs[0].set_title('Disciplinary Stats')

    # Plot for offensive stats
    axs[1].bar(offensive_stats.keys(), offensive_stats.values(), color='blue')
    axs[1].set_title('Offensive Stats')

    # Display the plots
    plt.tight_layout()
    plt.show()
