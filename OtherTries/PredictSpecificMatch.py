import keras
import numpy as np
import pandas as pd
import ModelTestingWithStatistics as mts

# try 1 to predict a specific match
cat_cols_row = ['tourney_name', 'surface', 'draw_size', 'tourney_level', 'Player1_entry', 'Player1_hand', 'Player1_ioc',
                'Player2_entry', 'Player2_hand', 'Player2_ioc', 'best_of', 'round']

num_cols_row = ['match_num', 'Player1_seed', 'Player1_ht', 'Player1_age', 'Player1_rank', 'Player1_rank_points',
                'Player2_seed', 'Player2_ht', 'Player2_age', 'Player2_rank', 'Player2_rank_points', 'minutes']
model = keras.models.load_model("my_model.h5")
print("Model loaded successfully")
# this should work to predict any game with these features
official_df = pd.read_csv('all_matches_final.csv')
official_data = [
    ["Roland Garros", "Clay", 64, "G", 6, np.NaN, "Hubert Hurkacz", "R", 196.0, "POL", 27.2, 5, "R16", 0.0, np.NaN,
     np.NaN, "Denis Shapovalov", "L", 185.0, "CAN", 25.5, 8.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 118, 540, 8, 3885]]
official_match = pd.DataFrame(official_data,
                              columns=['tourney_name', "surface", "draw_size", "tourney_level", "match_num",
                                       "Player1_entry", "Player1_name", "Player1_hand", "Player1_ht", "Player1_ioc",
                                       "Player1_age", "best_of", "round", "minutes", "Player2_seed",
                                       "Player2_entry", "Player2_name", "Player2_hand", "Player2_ht", "Player2_ioc",
                                       "Player2_age", "Player1_seed", "w_ace", "w_df", "w_svpt", "w_1stIn", "w_1stWon",
                                       "w_2ndWon", "w_SvGms", "w_bpSaved", "w_bpFaced", "l_ace", "l_df", "l_svpt",
                                       "l_1stIn", "l_1stWon", "l_2ndWon", "l_SvGms", "l_bpSaved", "l_bpFaced",
                                       "Player2_rank", "Player2_rank_points", "Player1_rank", "Player1_rank_points"])
# official_match = official_match.drop("score", axis=1)

for i in cat_cols_row:
    official_match[i] = official_match[i].replace(np.NaN, official_df[i].mode()[0])
for i in num_cols_row:
    official_match[i] = official_match[i].replace(np.NaN, official_match[i].mean())


def convertCatToNum_row(dff):
    dff_new = pd.get_dummies(dff, columns=cat_cols_row)
    return dff_new


def normalize_one_row(dff, col_name_list, match_row):
    result = match_row.copy()
    for feature_name in col_name_list:
        max_value = dff[feature_name].max()
        min_value = dff[feature_name].min()
        result[feature_name] = (match_row[feature_name] - min_value) / (max_value - min_value)
    return result


def add_generated_data(official_match, player_A_statistics, player_B_statistics):
    #, 'w_ace',
                # 'w_df',
                # 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced', 'l_ace', 'l_df',
                # 'l_svpt', 'l_1stIn',
                # 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced'
    official_match['w_ace'] = player_A_statistics['aces']
    official_match['w_df'] = player_A_statistics['double_faults']
    official_match['w_svpt'] = player_A_statistics['first_serve_pct']
    official_match['w_1stIn'] = player_A_statistics['first_serve_in']
    official_match['w_1stWon'] = player_A_statistics['first_serve_points_won']
    official_match['w_2ndWon'] = player_A_statistics['second_serve_points_won']
    official_match['w_SvGms'] = player_A_statistics['first_serve_in'] #TODO !! this is not right now
    official_match['w_bpSaved'] = player_A_statistics['break_points_saved']
    official_match['w_bpFaced'] = player_A_statistics['break_points_faced']

    official_match['l_ace'] = player_B_statistics['aces']
    official_match['l_df'] = player_B_statistics['double_faults']
    official_match['l_svpt'] = player_B_statistics['first_serve_pct']
    official_match['l_1stIn'] = player_B_statistics['first_serve_in']
    official_match['l_1stWon'] = player_B_statistics['first_serve_points_won']
    official_match['l_2ndWon'] = player_B_statistics['second_serve_points_won']
    official_match['l_SvGms'] = player_B_statistics['first_serve_in'] #TODO !! this is not right now
    official_match['l_bpSaved'] = player_B_statistics['break_points_saved']
    official_match['l_bpFaced'] = player_B_statistics['break_points_faced']
    return official_match

# print(official_match.iloc[0])
row = official_match.iloc[0]
# add generated columns instead of the known ones
player_A_statistics, player_B_statistics = mts.generate_for_A_vs_B(row['Player1_name'],
                                                                   row['Player2_name'],
                                                                   row['surface'])
# print(f"{official_match['Player1_name']}: {player_A_statistics}")
# print(f"{official_match['Player2_name']}: {player_B_statistics}")

official_match = convertCatToNum_row(official_match)
official_match = normalize_one_row(official_df, num_cols_row, official_match)
official_match = add_generated_data(official_match, player_A_statistics, player_B_statistics)
print(official_match.iloc[0])

player_A = official_match.iloc[0]['Player1_name']
player_B = official_match.iloc[0]['Player2_name']
# print(row_i)

# preparing official_df
to_drop = ['tourney_id', 'tourney_date', 'score']
official_df = official_df.drop(to_drop, axis=1)
for i in mts.cat_cols:
    official_df[i] = official_df[i].replace(np.NaN, official_df[i].mode()[0])
for i in mts.num_cols:
    official_df[i] = official_df[i].replace(np.NaN, official_df[i].mean())
official_df = mts.convertCatToNum(official_df)
official_df = mts.normalize(official_df, mts.num_cols)
official_df = official_df.drop(['Player1_name'], axis=1)
official_df = official_df.drop(['Player2_name'], axis=1)
official_df = official_df.drop(['Player1_id'], axis=1)
official_df = official_df.drop(['Player2_id'], axis=1)
official_df = official_df.drop(['y'], axis=1)

official_match_columns = official_match.columns.tolist()
training_columns = official_df.columns.tolist()
missing_columns = set(training_columns) - set(official_match_columns)
missing_df = pd.DataFrame({col: False for col in missing_columns}, index=[0])
official_match = pd.concat([official_match, missing_df], axis=1)
# for col in missing_columns:
#     official_match[col] = False

# dropping name columns
official_match = official_match.drop(['Player1_name'], axis=1)
official_match = official_match.drop(['Player2_name'], axis=1)

import tensorflow as tf

# tennis_match = df_for_row.iloc[21]
tennis_match = official_match
tennis_match_tf = tf.convert_to_tensor(tennis_match, dtype=tf.float64)
# tennis_match_tf = tf.expand_dims(tennis_match_tf, axis=0)

y_pred_test = model.predict(tennis_match_tf)
y_pred_test = [int(i > .5) for i in y_pred_test]

if y_pred_test[0] == 0:
    print(f"Player {player_A} lost! Player {player_B} won!")
elif y_pred_test[0] == 1:
    print(f"Player {player_A} won! Player {player_B} lost!")
