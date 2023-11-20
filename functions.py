# load key_stats into notebook
key_stats = pd.read_csv("raw_data/stats/key_stats.csv")
# create Real Madrid and Man. United list of players
real_player_list = list(key_stats[key_stats.club == 'Real Madrid'].player_name.unique())
man_player_list = list(key_stats[key_stats.club == 'Man. United'].player_name.unique())


def player_name_list_preprocessing(player_list):
    """ This function takes a list of player names from kaggle dataset and lowers + replaces spaces by dashes"""
    preprocessed_list = []
    for player in player_list:
        player = player.lower()
        player = player.replace(" ", "-")
        preprocessed_list.append(player)
    return preprocessed_list
