import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam

from NeuralNetwork import features


# --------------------------PREPARE TRAIN SET AND TEST SET-----------------------------------
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
data_training = pd.DataFrame(features.training_data())
data_training = one_hot_encoding(data_training)
X_train = data_training[feature_cols]  # Features
y_train = data_training.Outcome  # Target variable

data_testing = pd.DataFrame(features.testing_data())
data_testing = one_hot_encoding(data_testing)
X_test = data_testing[feature_cols]  # Features
y_test = data_testing.Outcome  # Target variable


# ----------------------------------- NEURAL NETWORK -----------------------------------

scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=30, batch_size=32)

loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Training Accuracy')
plt.legend()

plt.show()
