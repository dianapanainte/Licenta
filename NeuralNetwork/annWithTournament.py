# VALIDATION, EARLY STOPPING, TOURNAMENT
from time import sleep

import numpy as np
import pandas as pd
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from keras import callbacks

from NeuralNetwork import featuresWithTournament
import matplotlib.pyplot as plt
import joblib


# USE THIS ANN, IT HAS VALIDATION, EARLY STOPPING AND IT IS FINE

def one_hot_encode_features(feature, data):
    encoder = OneHotEncoder(handle_unknown='ignore')
    surface_encoded = encoder.fit_transform(data[[feature]])
    surface_encoded_df = pd.DataFrame(surface_encoded.toarray(), columns=encoder.get_feature_names_out([feature]))
    data.drop(feature, axis=1, inplace=True)
    data = pd.concat([data, surface_encoded_df], axis=1)
    return encoder, data


# --------------------------PREPARE TRAIN SET AND TEST SET-----------------------------------
def one_hot_encoding_first_time(data):
    encoder, data = one_hot_encode_features('Player', data)
    joblib.dump(encoder, 'F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_player.joblib')
    encoder, data = one_hot_encode_features('Opponent', data)
    joblib.dump(encoder, 'F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_opponent.joblib')
    encoder, data = one_hot_encode_features('Hand', data)
    joblib.dump(encoder, 'F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_hand.joblib')
    encoder, data = one_hot_encode_features('Opponent_Hand', data)
    joblib.dump(encoder, 'F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_opponent_hand.joblib')
    encoder, data = one_hot_encode_features('Tournament', data)
    joblib.dump(encoder, 'F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_tournament.joblib')
    encoder, data = one_hot_encode_features('Surface', data)
    joblib.dump(encoder, 'F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_surface.joblib')
    encoder, data = one_hot_encode_features('Round', data)
    joblib.dump(encoder, 'F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_round.joblib')
    return data


def one_hot_encoding_second_time(data):
    encoder = joblib.load('F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_player.joblib')
    all_possible_columns = encoder.get_feature_names_out(['Player'])
    data_encoded = encoder.fit_transform(data[['Player']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=encoder.get_feature_names_out(['Player']))
    data.drop('Player', axis=1, inplace=True)
    for col in all_possible_columns:
        if col not in data_encoded_df.columns:
            data_encoded_df[col] = 0
    data = pd.concat([data, data_encoded_df], axis=1)

    encoder = joblib.load('F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_opponent.joblib')
    all_possible_columns = encoder.get_feature_names_out(['Opponent'])
    # print(f"ALL POSSIBLE COLUMNS 1: {all_possible_columns.shape[0]}")
    data_encoded = encoder.fit_transform(data[['Opponent']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=encoder.get_feature_names_out(['Opponent']))
    data.drop('Opponent', axis=1, inplace=True)
    for col in all_possible_columns:
        if col not in data_encoded_df.columns:
            data_encoded_df[col] = 0
    data = pd.concat([data, data_encoded_df], axis=1)

    encoder = joblib.load('F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_hand.joblib')
    all_possible_columns = encoder.get_feature_names_out(['Hand'])
    # print(f"ALL POSSIBLE COLUMNS 2: {all_possible_columns.shape[0]}")
    data_encoded = encoder.fit_transform(data[['Hand']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=encoder.get_feature_names_out(['Hand']))
    data.drop('Hand', axis=1, inplace=True)
    for col in all_possible_columns:
        if col not in data_encoded_df.columns:
            data_encoded_df[col] = 0
    data = pd.concat([data, data_encoded_df], axis=1)

    encoder = joblib.load('F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_opponent_hand.joblib')
    all_possible_columns = encoder.get_feature_names_out(['Opponent_Hand'])
    # print(f"ALL POSSIBLE COLUMNS 3: {all_possible_columns.shape[0]}")
    data_encoded = encoder.fit_transform(data[['Opponent_Hand']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=encoder.get_feature_names_out(
                                       ['Opponent_Hand']))
    data.drop('Opponent_Hand', axis=1, inplace=True)
    for col in all_possible_columns:
        if col not in data_encoded_df.columns:
            data_encoded_df[col] = 0
    data = pd.concat([data, data_encoded_df], axis=1)

    encoder = joblib.load('F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_tournament.joblib')
    all_possible_columns = encoder.get_feature_names_out(['Tournament'])
    # print(f"ALL POSSIBLE COLUMNS 4: {all_possible_columns.shape[0]}")
    data_encoded = encoder.fit_transform(data[['Tournament']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=encoder.get_feature_names_out(['Tournament']))
    data.drop('Tournament', axis=1, inplace=True)
    for col in all_possible_columns:
        if col not in data_encoded_df.columns:
            data_encoded_df[col] = 0
    data = pd.concat([data, data_encoded_df], axis=1)

    encoder = joblib.load('F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_surface.joblib')
    all_possible_columns = encoder.get_feature_names_out(['Surface'])
    # print(f"ALL POSSIBLE COLUMNS 5: {all_possible_columns.shape[0]}")
    data_encoded = encoder.fit_transform(data[['Surface']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=encoder.get_feature_names_out(['Surface']))
    data.drop('Surface', axis=1, inplace=True)
    for col in all_possible_columns:
        if col not in data_encoded_df.columns:
            data_encoded_df[col] = 0
    data = pd.concat([data, data_encoded_df], axis=1)

    encoder = joblib.load('F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_round.joblib')
    all_possible_columns = encoder.get_feature_names_out(['Round'])
    # print(f"ALL POSSIBLE COLUMNS 6: {all_possible_columns.shape[0]}")
    data_encoded = encoder.fit_transform(data[['Round']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=encoder.get_feature_names_out(['Round']))
    data.drop('Round', axis=1, inplace=True)
    for col in all_possible_columns:
        if col not in data_encoded_df.columns:
            data_encoded_df[col] = 0
    data = pd.concat([data, data_encoded_df], axis=1)
    return data


# --------------------------PREPARE TRAIN SET AND TEST SET-----------------------------------

# feature_cols = ['Age', 'Rank', 'Height', 'Wins_semester', 'Losses_semester',
#                 "Wins_year", "Losses_year", "Wins_clay", "Wins_hard", "Wins_grass", "Losses_clay", "Losses_hard",
#                 "Losses_grass", "Opponent_Age", "Opponent_Rank", "Opponent_Height", "Opponent_Wins_semester",
#                 "Opponent_Losses_semester", "Opponent_Wins_year", "Opponent_Losses_year", "Opponent_Wins_clay",
#                 "Opponent_Wins_hard", "Opponent_Wins_grass", "Opponent_Losses_clay", "Opponent_Losses_hard",
#                 "Opponent_Losses_grass", "Hand_L", 'Hand_R', "Opponent_Hand_L", 'Opponent_Hand_R']

# print(featuresWithTournament.training_data())
# all_data = pd.read_csv('F:/GithubCloning/Licenta/WebSiteBackend/stats/csv_folder/data_tour_not_use.csv')
# all_data = one_hot_encoding_first_time(all_data)
# scaler = MinMaxScaler()
# all_data = scaler.fit_transform(all_data)
# joblib.dump(scaler, 'F:/GithubCloning/Licenta/FinalModel/scalers/ann_2_scaler.joblib')
# print("DOnE!!")
# sleep(10)

data_training = pd.DataFrame(featuresWithTournament.training_data())
# data_training.drop('Player', axis=1, inplace=True)
# data_training.drop('Opponent', axis=1, inplace=True)
data_training.drop('Date', axis=1, inplace=True)
data_training = one_hot_encoding_second_time(data_training)
X_train = data_training.iloc[:, :-1]
y_train = data_training.Outcome
print(f"JUST AFTER ENCODING {X_train.shape[1]}")

data_validation = pd.DataFrame(featuresWithTournament.validation_data())
data_validation = one_hot_encoding_second_time(data_validation)
# data_validation.drop('Player', axis=1, inplace=True)
# data_validation.drop('Opponent', axis=1, inplace=True)
data_validation.drop('Date', axis=1, inplace=True)
X_val = data_validation.iloc[:, :-1]
print(f"JUST AFTER ENCODING {X_val.shape[1]}")
y_val = data_validation.Outcome

for val in X_val:
    if val not in X_train:
        print(val)

data_testing = pd.DataFrame(featuresWithTournament.testing_data())
data_testing = one_hot_encoding_second_time(data_testing)
# data_testing.drop('Player', axis=1, inplace=True)
# data_testing.drop('Opponent', axis=1, inplace=True)
data_testing.drop('Date', axis=1, inplace=True)
X_test = data_testing.iloc[:, :-1]
y_test = data_testing.Outcome

# ----------------------------------- NEURAL NETWORK -----------------------------------

scaler = joblib.load('F:/GithubCloning/Licenta/FinalModel/scalers/ann_2_scaler.joblib')
X_train = scaler.fit_transform(X_train)
X_val = scaler.fit_transform(X_val)
X_test = scaler.fit_transform(X_test)


# X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
# X_val = X_val.reshape((X_val.shape[0], X_val.shape[1], 1))
# X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

print(X_train.shape[1])
model_ann_tournament = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.5),
    Dense(64, activation='relu'),
    # Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model_ann_tournament.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

earlystopping = callbacks.EarlyStopping(monitor="val_loss",
                                        mode="min",
                                        verbose=1,
                                        patience=10,
                                        restore_best_weights=True)
print(X_val.shape[1])
history = model_ann_tournament.fit(X_train, y_train, epochs=30, batch_size=32, validation_data=(X_val, y_val),
                                   callbacks=[earlystopping])
# history = model.fit(X_train, y_train, epochs=35, batch_size=32, validation_data=(X_val, y_val))

# loss, accuracy = model_ann_tournament.evaluate(X_test, y_test)
# print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')
model_ann_tournament.save('F:/GithubCloning/Licenta/FinalModel/models/ann_tournament.h5')
# ----------------------------------- PLOT -----------------------------------
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
# plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
# plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Training Accuracy')
plt.legend()

plt.tight_layout()
plt.show()
