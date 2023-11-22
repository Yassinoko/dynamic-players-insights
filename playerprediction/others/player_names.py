import pandas as pd
import numpy as np

# import key_stats file
key_stats = pd.read_csv("raw_data/stats/key_stats.csv")

# create dictionary of team_names keys and player_name values
team_names = ['Real Madrid', 'Liverpool', 'Man. United', 'Villareal', 'Benfica', 'Bayern', 'Atlético', 'Chelsea']
team_players_dict = {}
for team_name in team_names:
    team_players_dict[team_name] = list(key_stats[key_stats.club == team_name].player_name.unique())
