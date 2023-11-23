import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Managing duplicate data
def dropping_duplicates(data) :
    print(f'The {data} dataset has {data.duplicated().sum()} duplicate.s')
    data = data.drop_duplicates()
    return data

# Lowering cases, that will be helpful for the creation of indexes
def lowercase_strings(data):
    for column in data.columns:
        if data[column].dtype == 'object':
            data[column] = data[column].astype(str).str.lower()
    return data

# Creating the new unique keys
def new_keys(data):
    data['player_id'] = data['player_name'] + '_' + data['club'] + '_' + data['position']
    data.set_index('key', inplace=True)
    return data

# Encoding the position columns
def encoding_positions(data) :
    encoder = LabelEncoder()
    encoder.fit(data["position"])
    data["encoded_position"] = encoder.transform(data["position"])
    return data
