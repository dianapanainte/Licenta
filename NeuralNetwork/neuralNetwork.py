import math
import time

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense

from NeuralNetwork import features

pd.set_option('display.max_columns', None)

start_time = time.time()


# ----------------------------------- DATA PREPROCESSING -----------------------------------


def one_hot_encoding(data):
    # One-hot encode the 'Hand' feature
    encoder = OneHotEncoder()
    surface_encoded = encoder.fit_transform(data[['Hand']])
    surface_encoded_df = pd.DataFrame(surface_encoded.toarray(), columns=encoder.get_feature_names_out(['Hand']))

    # Drop the original 'Hand' column
    data.drop('Hand', axis=1, inplace=True)

    # Concatenate the encoded features with the original data
    data = pd.concat([data, surface_encoded_df], axis=1)

    # -----------------------------------------------------------for opponent hand
    # One-hot encode the 'Opponent_Hand' feature
    encoder = OneHotEncoder()
    surface_encoded = encoder.fit_transform(data[['Opponent_Hand']])
    surface_encoded_df = pd.DataFrame(surface_encoded.toarray(),
                                      columns=encoder.get_feature_names_out(['Opponent_Hand']))

    # Drop the original 'Opponent_Hand' column
    data.drop('Opponent_Hand', axis=1, inplace=True)

    # Concatenate the encoded features with the original data
    data = pd.concat([data, surface_encoded_df], axis=1)
    return data


# --------------------------PREPARE TRAIN SET AND TEST SET-----------------------------------

feature_cols = ['Age', 'Rank', 'Height', 'Wins_semester', 'Losses_semester',
                "Wins_year", "Losses_year", "Wins_clay", "Wins_hard", "Wins_grass", "Losses_clay", "Losses_hard",
                "Losses_grass", "Opponent_Age", "Opponent_Rank", "Opponent_Height", "Opponent_Wins_semester",
                "Opponent_Losses_semester", "Opponent_Wins_year", "Opponent_Losses_year", "Opponent_Wins_clay",
                "Opponent_Wins_hard", "Opponent_Wins_grass", "Opponent_Losses_clay", "Opponent_Losses_hard",
                "Opponent_Losses_grass", "Hand_L", 'Hand_R', "Opponent_Hand_L", 'Opponent_Hand_R']
# Training data
data_training = pd.DataFrame(features.training_data())
data_training = one_hot_encoding(data_training)
X_train = data_training[feature_cols]  # Features
y_train = data_training.Outcome  # Target variable

# Testing data
data_testing = pd.DataFrame(features.testing_data())
data_testing = one_hot_encoding(data_testing)
X_test = data_testing[feature_cols]  # Features
y_test = data_testing.Outcome  # Target variable

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=16)


# ----------------------------------- NEURAL NETWORK -----------------------------------

# Normalize data
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Reshape input data
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

model = Sequential()
model.add(LSTM(units=256, activation='relu', return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(LSTM(units=128, return_sequences=True))
model.add(LSTM(units=128, return_sequences=True))
model.add(Dense(units=1))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=50, batch_size=64, verbose=2)

print(history.history.keys())
# summarize history for loss
plt.plot(history.history['loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.grid()
plt.savefig('LSTM-Loss.png')
plt.show()

# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.grid()
plt.savefig('LSTM-Accuracy.png')
plt.show()

# trainScore = model.evaluate(X_train, y_train, verbose=0)
# print('Train Score: %.2f MSE (%.2f RMSE)' % (trainScore, math.sqrt(trainScore)))
# testScore = model.evaluate(X_test, y_test, verbose=0)
# print('Test Score: %.2f MSE (%.2f RMSE)' % (testScore, math.sqrt(testScore)))
# print("Accuracy: {:.2f}%".format(accuracy * 100))

loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

# --execution time---------------------------------------------------
end_time = time.time()

execution_time = end_time - start_time
print("Execution time:", execution_time / 60, "minutes")
