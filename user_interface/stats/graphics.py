import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.express as px
import os

ospath = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(ospath, "stats_data")

df_attacking = pd.read_csv(os.path.join(csv_path, "attacking.csv"))
df_attempts = pd.read_csv(os.path.join(csv_path, "attempts.csv"))
df_defending = pd.read_csv(os.path.join(csv_path, "defending.csv"))
df_disciplinary = pd.read_csv(os.path.join(csv_path, "disciplinary.csv"))
df_distributon = pd.read_csv(os.path.join(csv_path, "distributon.csv"))
df_goalkeeping = pd.read_csv(os.path.join(csv_path, "goalkeeping.csv"))
df_goals = pd.read_csv(os.path.join(csv_path, "goals.csv"))
df_key_stats = pd.read_csv(os.path.join(csv_path, "key_stats.csv"))


def plot_combined_goal_types(*args):
    # Convert player names to lowercase
    player_stats = []
    colors = ['blue', 'red', 'green', 'orange', 'purple']  # Define colors for players

    for i, player_name in enumerate(args, start=1):
        player_name = player_name.lower()
        player_data = df_goals[df_goals['player_name'].str.lower() == player_name]

        if player_data.empty:
            print(f"No data found for player {i}: {player_name.capitalize()}")
            continue

        player_stats.append({
            'name': player_name.capitalize(),
            'data': player_data,
            'color': colors[i - 1] if i <= len(colors) else None  # Assign colors to players
        })

    if not player_stats:
        print("No valid player data available.")
        return

    # Create subplots based on the number of players
    fig = make_subplots(rows=1, cols=2, subplot_titles=('How scored', 'From where scored'))

    for player in player_stats:
        # Summarize goal types for 'How scored' analysis
        gl_sum_how_scored = player['data'][['right_foot', 'left_foot', 'headers', 'others']].sum()
        gl_sum_how_scored = gl_sum_how_scored.to_frame(name='Goals').reset_index()

        # Summarize goal types for 'From where scored' analysis
        gl_sum_from_where = player['data'][['inside_area', 'outside_areas', 'penalties']].sum()
        gl_sum_from_where = gl_sum_from_where.to_frame(name='Goals').reset_index()

        # Add traces for 'How scored' analysis
        fig.add_trace(go.Bar(x=gl_sum_how_scored['index'], y=gl_sum_how_scored['Goals'], name=f'{player["name"]}',
                             marker_color=player['color'], text=gl_sum_how_scored['Goals'], textposition='auto'),
                      row=1, col=1)

        # Add traces for 'From where scored' analysis
        fig.add_trace(go.Bar(x=gl_sum_from_where['index'], y=gl_sum_from_where['Goals'], name=f'{player["name"]}',
                             marker_color=player['color'], text=gl_sum_from_where['Goals'], textposition='auto'),
                      row=1, col=2)

    # Update layout
    fig.update_layout(title='Goal types analysis', showlegend=True)
    fig.update_xaxes(title_text='Goal Types', row=1, col=1)
    fig.update_xaxes(title_text='Goal Locations', row=1, col=2)
    fig.update_yaxes(title_text='Goals', row=1, col=1)

    return fig



def plot_pass_stats(*players):
    if len(players) == 1:
        player_name = players[0].capitalize()

        # Filter data for the specified player (lowercase)
        filtered_data = df_distributon[df_distributon['player_name'].str.lower() == player_name.lower()]

        if filtered_data.empty:
            print(f"No data found for player: {player_name}")
            return

        # Extract pass columns and check validity
        pass_columns = ["pass_attempted", "pass_completed"]
        valid_pass_columns = [col for col in pass_columns if col in filtered_data.columns]

        if len(valid_pass_columns) != 2:
            print(f"Not enough valid pass columns available for player: {player_name}")
            return

        # Extract the required pass statistics
        pass_data = filtered_data[valid_pass_columns].iloc[0]

        # Create bar chart for Pass Statistics
        fig = go.Figure()
        for col_name in valid_pass_columns:
            pass_data_str = pass_data[col_name].astype(str)  # Convert pass data to strings for text parameter
            fig.add_trace(go.Bar(x=[player_name], y=[pass_data[col_name]],
                                 name=col_name.capitalize(), text=pass_data_str, textposition='inside'))

        # Update layout for Pass Statistics
        fig.update_xaxes(title_text='Players')
        fig.update_yaxes(title_text='Count')
        fig.update_layout(showlegend=True, title=f'Pass Statistics for {player_name}', barmode='group')

        return fig
    else:
        fig = make_subplots(rows=1, cols=2, subplot_titles=('Pass Attempted', 'Pass Completed'))

        pass_colors = px.colors.qualitative.Pastel  # Get a set of colors for pass statistics
        unique_players = set()

        for i, player_name in enumerate(players, start=1):
            # Filter data for the specified player (lowercase)
            filtered_data = df_distributon[df_distributon['player_name'].str.lower() == player_name.lower()]

            if filtered_data.empty:
                print(f"No data found for player: {player_name.capitalize()}")
                continue

            unique_players.add(player_name.capitalize())

            # Extract pass columns and check validity
            pass_columns = ["pass_attempted", "pass_completed"]
            valid_pass_columns = [col for col in pass_columns if col in filtered_data.columns]

            if len(valid_pass_columns) != 2:
                print(f"Not enough valid pass columns available for player: {player_name.capitalize()}")
                continue

            # Extract the required pass statistics
            pass_data = filtered_data[valid_pass_columns].iloc[0]

            # Create bar chart for Pass Statistics
            for j, col_name in enumerate(valid_pass_columns, start=1):
                # Convert pass data to strings for text parameter
                pass_data_str = pass_data[col_name].astype(str)

                fig.add_trace(go.Bar(x=[player_name.capitalize()], y=[pass_data[col_name]],
                                     name=col_name.capitalize(), legendgroup=player_name.capitalize(), marker_color=pass_colors[i - 1], text=pass_data_str, textposition='inside'), row=1, col=j)

        # Update layout for Pass Statistics
        fig.update_xaxes(title_text='Players', row=1, col=1)
        fig.update_xaxes(title_text='Players', row=1, col=2)
        fig.update_yaxes(title_text='Count', row=1, col=1)
        fig.update_yaxes(title_text='Count', row=1, col=2)
        fig.update_layout(showlegend=True, title='Pass Statistics Comparison', barmode='group')

        # Set legend items based on unique player names
        fig.for_each_trace(lambda trace: trace.update(showlegend=trace.name in unique_players))

        return fig


def plot_tackle_stats(*args):
    if len(args) == 1:
        player_name = args[0].lower()

        # Filter data for the specified player
        player_stats = df_defending[df_defending['player_name'].str.lower() == player_name]

        if player_stats.empty:
            print(f"No data found for player: {player_name.capitalize()}")
            return

        # Summarize tackle won vs lost
        tackle_won = player_stats['t_won'].sum()
        tackle_lost = player_stats['t_lost'].sum()

        fig = go.Figure()
        fig.add_trace(go.Bar(x=['Tackle WON'], y=[tackle_won], name='Tackle WON', marker_color='blue', text=[tackle_won],
                             textposition='auto'))
        fig.add_trace(go.Bar(x=['Tackle LOST'], y=[tackle_lost], name='Tackle LOST', marker_color='red', text=[tackle_lost],
                             textposition='auto'))

        fig.update_xaxes(title_text='Tackle')
        fig.update_yaxes(title_text='Count')
        fig.update_layout(title=f'{player_name.capitalize()} - Tackle Stats', showlegend=True)

        return fig
    else:
        fig = make_subplots(rows=1, cols=2, subplot_titles=['Tackle WON', 'Tackle LOST'])

        colors = px.colors.qualitative.Pastel  # Get a set of colors for players

        # Create a consolidated legend for all players
        for i, player_name in enumerate(args, start=1):
            player_name = player_name.lower()

            # Filter data for the specified player
            player_stats = df_defending[df_defending['player_name'].str.lower() == player_name]

            if player_stats.empty:
                print(f"No data found for player: {player_name.capitalize()}")
                continue

            # Summarize tackle won vs lost
            tackle_won = player_stats['t_won'].sum()
            tackle_lost = player_stats['t_lost'].sum()

            # Add bar chart trace for Tackle WON
            fig.add_trace(go.Bar(x=[f'{player_name.capitalize()}'], y=[tackle_won],
                                 name=f'{player_name.capitalize()} - Tackle WON', marker_color=colors[i - 1],
                                 text=[tackle_won], textposition='auto'), row=1, col=1)

            # Add bar chart trace for Tackle LOST
            fig.add_trace(go.Bar(x=[f'{player_name.capitalize()}'], y=[tackle_lost],
                                 name=f'{player_name.capitalize()} - Tackle LOST', marker_color=colors[i - 1],
                                 text=[tackle_lost], textposition='auto'), row=1, col=2)

        # Update layout for Tackle WON
        fig.update_xaxes(title_text='Players', row=1, col=1)
        fig.update_yaxes(title_text='Tackle Count', row=1, col=1)

        # Update layout for Tackle LOST
        fig.update_xaxes(title_text='Players', row=1, col=2)
        fig.update_yaxes(title_text='Tackle Count', row=1, col=2)

        fig.update_layout(showlegend=True)

        return fig



def plot_goalkeeper_performance(*args):
    if len(args) == 1:
        player_name = args[0].lower()

        # Filter data for the specified player
        player_stats = df_goalkeeping[df_goalkeeping['player_name'].str.lower() == player_name]

        if player_stats.empty:
            print(f"No data found for player: {player_name.capitalize()}")
            return

        # Summarize saved and conceded
        gl_sum = player_stats[['saved', 'conceded']].sum()
        gl_sum = gl_sum.to_frame(name='Values').reset_index()

        # Calculate the values and set lower limit for 'Conceded'
        values = gl_sum['Values'].tolist()
        values[1] = max(values[1], 0)

        fig = go.Figure()
        fig.add_trace(go.Bar(x=gl_sum['index'], y=values,
                             marker_color=['blue', 'red'],
                             text=values, textposition='auto',
                             name=['Saved', 'Conceded']))

        fig.update_xaxes(title_text='Metrics')
        fig.update_yaxes(title_text='Count')
        fig.update_layout(title=f'{player_name.capitalize()} - Goalkeeper Performance',
                          showlegend=True)

        return fig
    else:
        fig = make_subplots(rows=1, cols=2, subplot_titles=['Saved', 'Conceded'])

        colors = px.colors.qualitative.Pastel  # Get a set of colors for players

        # Create a consolidated legend for all players
        for i, player_name in enumerate(args, start=1):
            player_name = player_name.lower()

            # Filter data for the specified player
            player_stats = df_goalkeeping[df_goalkeeping['player_name'].str.lower() == player_name]

            if player_stats.empty:
                print(f"No data found for player: {player_name.capitalize()}")
                continue

            # Summarize saved and conceded
            gl_sum = player_stats[['saved', 'conceded']].sum()
            gl_sum = gl_sum.to_frame(name='Values').reset_index()

            # Calculate the values and set lower limit for 'Conceded'
            values = gl_sum['Values'].tolist()
            if i % 2 == 0:
                values[1] = max(values[1], 0)

            # Add bar chart trace for Saved
            fig.add_trace(go.Bar(x=[f'{player_name.capitalize()}'], y=[values[0]],
                                 name=f'{player_name.capitalize()} - Saved', marker_color=colors[i - 1],
                                 text=[values[0]], textposition='auto'), row=1, col=1)

            # Add bar chart trace for Conceded
            fig.add_trace(go.Bar(x=[f'{player_name.capitalize()}'], y=[values[1]],
                                 name=f'{player_name.capitalize()} - Conceded', marker_color=colors[i - 1],
                                 text=[values[1]], textposition='auto'), row=1, col=2)

        # Update layout for Saved
        fig.update_xaxes(title_text='Players', row=1, col=1)
        fig.update_yaxes(title_text='Saved Count', row=1, col=1)

        # Update layout for Conceded
        fig.update_xaxes(title_text='Players', row=1, col=2)
        fig.update_yaxes(title_text='Conceded Count', row=1, col=2)

        fig.update_layout(showlegend=True)

        return fig
