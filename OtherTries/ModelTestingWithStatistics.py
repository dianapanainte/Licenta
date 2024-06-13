import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

df = pd.read_csv('all_matches_final.csv')
# print(df.describe())

players = ['Player1_id', 'Player1_name', 'Player2_id', 'Player2_name']

to_drop = ['tourney_id', 'tourney_date', 'score']

cat_cols = ['tourney_name', 'surface', 'draw_size', 'tourney_level', 'Player1_entry', 'Player1_hand', 'Player1_ioc',
            'Player2_entry', 'Player2_hand', 'Player2_ioc', 'best_of', 'round']

num_cols = ['match_num', 'Player1_seed', 'Player1_ht', 'Player1_age', 'Player1_rank', 'Player1_rank_points',
            'Player2_seed', 'Player2_ht', 'Player2_age', 'Player2_rank', 'Player2_rank_points', 'minutes', 'w_ace',
            'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced', 'l_ace', 'l_df',
            'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced']

df = df.drop(to_drop, axis=1)

for i in cat_cols:
    df[i] = df[i].replace(np.NaN, df[i].mode()[0])
for i in num_cols:
    df[i] = df[i].replace(np.NaN, df[i].mean())


def convertCatToNum(dff):
    dff_new = pd.get_dummies(dff, columns=cat_cols)
    return dff_new

# print(df.head())


def normalize(dff, col_name_list):
    result = dff.copy()
    for feature_name in col_name_list:
        max_value = dff[feature_name].max()
        min_value = dff[feature_name].min()
        result[feature_name] = (dff[feature_name] - min_value) / (max_value - min_value)
    return result


df = convertCatToNum(df)
df = normalize(df, num_cols)
# print(df.head())

Y = pd.DataFrame(df['y'])
X = df.drop(['y'], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.01, random_state=42)

# print(X_test.head())


# GENERATING STATISTICS USING PAST MATCHES FOR THOSE IN TEST SET
def generate_head_to_head(playerA, playerB, past_matches):
    head_to_head_matches = pd.DataFrame({
        'player': [],
        'opponent': [],
        'first_serve_pct': [],
        'aces': [],
        'double_faults': [],
        'first_serve_in': [],
        'first_serve_points_won': [],
        'second_serve_points_won': [],
        'break_points_saved': [],
        'break_points_faced': []
    })
    i = 0
    for index, row in past_matches.iterrows():
        if row['Player1_name'] == playerA and row['Player2_name'] == playerB:
            new_data = pd.DataFrame(
                {'player': [playerA], 'opponent': [playerB], 'first_serve_pct': [row['first_serve_pct']],
                 'aces': [row['aces']],
                 'double_faults': [row['double_faults']], 'first_serve_points_won': [row['first_serve_points_won']],
                 'first_serve_in': [row['first_serve_in']],
                 'second_serve_points_won': [row['second_serve_points_won']],
                 'break_points_saved': [row['break_points_saved']],
                 'break_points_faced': [row['break_points_faced']]})
            head_to_head_matches = pd.concat([head_to_head_matches, new_data], ignore_index=True)

            new_data = pd.DataFrame(
                {'player': [playerB], 'opponent': [playerA], 'first_serve_pct': [row['l_first_serve_pct']],
                 'aces': [row['l_aces']],
                 'double_faults': [row['l_double_faults']], 'first_serve_points_won': [row['l_first_serve_points_won']],
                 'first_serve_in': [row['l_first_serve_in']],
                 'second_serve_points_won': [row['l_second_serve_points_won']],
                 'break_points_saved': [row['l_break_points_saved']],
                 'break_points_faced': [row['l_break_points_faced']]})
            head_to_head_matches = pd.concat([head_to_head_matches, new_data], ignore_index=True)
        elif row['Player1_name'] == playerB and row['Player2_name'] == playerA:
            new_data = pd.DataFrame(
                {'player': [playerB], 'opponent': [playerA], 'first_serve_pct': [row['first_serve_pct']],
                 'aces': [row['aces']],
                 'double_faults': [row['double_faults']], 'first_serve_points_won': [row['first_serve_points_won']],
                 'first_serve_in': [row['first_serve_in']],
                 'second_serve_points_won': [row['second_serve_points_won']],
                 'break_points_saved': [row['break_points_saved']],
                 'break_points_faced': [row['break_points_faced']]})
            head_to_head_matches = pd.concat([head_to_head_matches, new_data], ignore_index=True)

            new_data = pd.DataFrame(
                {'player': [playerA], 'opponent': [playerB], 'first_serve_pct': [row['l_first_serve_pct']],
                 'aces': [row['l_aces']],
                 'double_faults': [row['l_double_faults']], 'first_serve_points_won': [row['l_first_serve_points_won']],
                 'first_serve_in': [row['l_first_serve_in']],
                 'second_serve_points_won': [row['l_second_serve_points_won']],
                 'break_points_saved': [row['l_break_points_saved']],
                 'break_points_faced': [row['l_break_points_faced']]})
            head_to_head_matches = pd.concat([head_to_head_matches, new_data], ignore_index=True)

    # print("Head 2 head generated successfully!")
    return head_to_head_matches


def generate_for_A_vs_B(playerA, playerB, actual_surface):
    csv_file_path = 'data_from_past_matches_with_opponent.csv'
    # print("File loaded successfully!")
    past_matches = pd.read_csv(csv_file_path)

    numeric_columns = ['first_serve_pct', 'aces', 'double_faults', 'first_serve_in', 'first_serve_points_won',
                       'second_serve_points_won', 'break_points_saved', 'break_points_faced']

    print(f"Generating statistics for {playerA} vs {playerB} on {actual_surface} surface...")
    player_a_stats = past_matches[past_matches['Player1_name'] == playerA][numeric_columns].mean()
    player_b_stats = past_matches[past_matches['Player1_name'] == playerB][numeric_columns].mean()

    surface = actual_surface

    player_a_surface_stats = \
        past_matches[(past_matches['Player1_name'] == playerA) & (past_matches['surface'] == surface)][
            numeric_columns].mean()
    player_b_surface_stats = \
        past_matches[(past_matches['Player1_name'] == playerB) & (past_matches['surface'] == surface)][
            numeric_columns].mean()

    weights = {
        'overall': 0.2,
        'surface': 0.2,
        'head_to_head': 0.6
    }

    head_to_head_matches = generate_head_to_head(playerA, playerB, past_matches)
    player_a_h2h_stats = head_to_head_matches[head_to_head_matches['player'] == playerA][numeric_columns].mean()
    player_b_h2h_stats = head_to_head_matches[head_to_head_matches['player'] == playerB][numeric_columns].mean()

    def weighted_average(player_stats, surface_stats, h2h_stats, weights):
        combined_stats = {}
        if head_to_head_matches.empty:
            # print("H2H empty! No matches between these players.")
            weights = {
                'overall': 0.4,
                'surface': 0.6
            }
            for stat in player_stats.index:
                combined_stats[stat] = (
                        player_stats[stat] * weights['overall'] +
                        surface_stats[stat] * weights['surface'])
        else:
            for stat in player_stats.index:
                combined_stats[stat] = (
                        player_stats[stat] * weights['overall'] +
                        surface_stats[stat] * weights['surface'] +
                        h2h_stats[stat] * weights['head_to_head']
                )
        return combined_stats

    player_a_combined_stats = weighted_average(player_a_stats, player_a_surface_stats, player_a_h2h_stats, weights)
    player_b_combined_stats = weighted_average(player_b_stats, player_b_surface_stats, player_b_h2h_stats, weights)

    # print(f"{playerA} Combined Statistics:")
    # print(player_a_combined_stats)
    #
    # print(f"{playerB} Combined Statistics:")
    # print(player_b_combined_stats)

    return player_a_combined_stats, player_b_combined_stats


if __name__ == '__main__':
    player_A, player_B = generate_for_A_vs_B('Hubert Hurkacz', 'Denis Shapovalov', 'Clay')
    print(player_A)
    print(player_B)


def generate_for_test_set(y_test):
    new_x_test = pd.DataFrame(columns=X_test.columns)
    i = 0
    for index, row in X_test.iterrows():
        if i % 100 == 0:
            print("Adding generated data to X_test: " + str(i) + " / " + str(len(X_test)))
        i += 1
        playerA = row['Player1_name']
        playerB = row['Player2_name']
        if row['surface_Carpet'] == 1:
            surface = 'Carpet'
        elif row['surface_Clay'] == 1:
            surface = 'Clay'
        elif row['surface_Grass'] == 1:
            surface = 'Grass'
        elif row['surface_Hard'] == 1:
            surface = 'Hard'
        player_a_combined_stats, player_b_combined_stats = generate_for_A_vs_B(playerA, playerB, surface)
        # if any of player_a_combined_stats['first_serve_pct], player_a_combined_stats['aces'] etc is np.NaN, we dont add it to the new_x_test
        if np.isnan(player_a_combined_stats['first_serve_pct']) or np.isnan(
                player_a_combined_stats['aces']) or np.isnan(
                player_a_combined_stats['double_faults']) or np.isnan(
                player_a_combined_stats['first_serve_in']) or np.isnan(
                player_a_combined_stats['first_serve_points_won']) or np.isnan(
                player_a_combined_stats['second_serve_points_won']) or np.isnan(
                player_a_combined_stats['break_points_saved']) or np.isnan(player_a_combined_stats['break_points_faced']):
            #delete the row from y_test
            y_test = y_test.drop(index)
            continue
        # if any of player_b_combined_stats['first_serve_pct], player_b_combined_stats['aces'] etc is np.NaN we dont add it to the new_x_test
        if np.isnan(player_b_combined_stats['first_serve_pct']) or np.isnan(
                player_b_combined_stats['aces']) or np.isnan(
                player_b_combined_stats['double_faults']) or np.isnan(
                player_b_combined_stats['first_serve_in']) or np.isnan(
                player_b_combined_stats['first_serve_points_won']) or np.isnan(
                player_b_combined_stats['second_serve_points_won']) or np.isnan(
                player_b_combined_stats['break_points_saved']) or np.isnan(player_b_combined_stats['break_points_faced']):
            y_test = y_test.drop(index)
            continue
        # modify the row from X_test with the new data
        row['w_svpt'] = player_a_combined_stats['first_serve_pct']
        row['w_ace'] = player_a_combined_stats['aces']
        row['w_df'] = player_a_combined_stats['double_faults']
        row['w_1stIn'] = player_a_combined_stats['first_serve_in']
        row['w_1stWon'] = player_a_combined_stats['first_serve_points_won']
        row['w_2ndWon'] = player_a_combined_stats['second_serve_points_won']
        row['w_bpSaved'] = player_a_combined_stats['break_points_saved']
        row['w_bpFaced'] = player_a_combined_stats['break_points_faced']
        row['l_svpt'] = player_b_combined_stats['first_serve_pct']
        row['l_ace'] = player_b_combined_stats['aces']
        row['l_df'] = player_b_combined_stats['double_faults']
        row['l_1stIn'] = player_b_combined_stats['first_serve_in']
        row['l_1stWon'] = player_b_combined_stats['first_serve_points_won']
        row['l_2ndWon'] = player_b_combined_stats['second_serve_points_won']
        row['l_bpSaved'] = player_b_combined_stats['break_points_saved']
        row['l_bpFaced'] = player_b_combined_stats['break_points_faced']
        # add the row to the new_x_test dataframe
        new_x_test.loc[len(new_x_test)] = row
    return new_x_test, y_test


def generate_dataframe_from_training_set():
    past_matches = pd.DataFrame({
        'Player1_name': [],
        'Player2_name': [],
        'surface': [],
        'first_serve_pct': [],
        'aces': [],
        'double_faults': [],
        'first_serve_in': [],
        'first_serve_points_won': [],
        'second_serve_points_won': [],
        'break_points_saved': [],
        'break_points_faced': [],
        'l_first_serve_pct': [],
        'l_aces': [],
        'l_double_faults': [],
        'l_first_serve_in': [],
        'l_first_serve_points_won': [],
        'l_second_serve_points_won': [],
        'l_break_points_saved': [],
        'l_break_points_faced': []
    })
    i = 0
    for index, row in X_train.iterrows():
        i += 1
        if i % 10000 == 0:
            print(i)

        new_data = pd.DataFrame({'Player1_name': [row['Player1_name']], 'Player2_name': [row['Player2_name']],
                                 'surface': [row['surface']], 'first_serve_pct': [row['w_svpt']],
                                 'aces': [row['w_ace']],
                                 'double_faults': [row['w_df']], 'first_serve_in': [row['w_1stIn']],
                                 'first_serve_points_won': [row['w_1stWon']],
                                 'second_serve_points_won': [row['w_2ndWon']],
                                 'break_points_saved': [row['w_bpSaved']], 'break_points_faced': [row['w_bpFaced']],
                                 'l_first_serve_pct': [row['l_svpt']], 'l_aces': [row['l_ace']],
                                 'l_double_faults': [row['l_df']],
                                 'l_first_serve_in': [row['l_1stIn']], 'l_first_serve_points_won': [row['l_1stWon']],
                                 'l_second_serve_points_won': [row['l_2ndWon']],
                                 'l_break_points_saved': [row['l_bpSaved']],
                                 'l_break_points_faced': [row['l_bpFaced']]})
        past_matches = pd.concat([past_matches, new_data], ignore_index=True)

    csv_file_path = 'data_from_past_matches_with_opponent.csv'  # Specify your file path and name
    past_matches.to_csv(csv_file_path, index=False)  # Set index=False to exclude the DataFrame index from the CSV

    print("Past matches data generated successfully!")
    print(f"DataFrame saved to {csv_file_path}")

# Uncomment to generate data from training set - takes a while - done only once, then I load the data from csv
# generate_dataframe_from_training_set()
