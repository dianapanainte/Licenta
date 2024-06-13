# import tensorflow
import tensorflow as tf
from sklearn.metrics import classification_report
from tensorflow.keras import Sequential
from tensorflow.keras import Input
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Dense

import ModelTestingWithStatistics as mts

# use keras API
model = tf.keras.Sequential()

X_train = mts.X_train
y_train = mts.y_train
# determine the number of input features
X_train = X_train.drop(['Player1_id'], axis=1)
X_train = X_train.drop(['Player1_name'], axis=1)
X_train = X_train.drop(['Player2_id'], axis=1)
X_train = X_train.drop(['Player2_name'], axis=1)
n_features = X_train.shape[1]
# define model
model.add(Input(shape=(n_features,)))
model.add(Dense(100, activation='relu', kernel_initializer='he_normal'))
model.add(Dropout(0.4))
model.add(Dense(100, activation='relu', kernel_initializer='he_normal'))
model.add(Dropout(0.6))
model.add(Dense(50, activation='relu', kernel_initializer='he_normal'))
model.add(Dropout(0.6))
model.add(Dense(1, activation='sigmoid'))

print("Model summary")
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# added by me
X_train = tf.convert_to_tensor(X_train, dtype=tf.float64)
#
model.fit(X_train, y_train, epochs=50, batch_size=128)
model.save("./my_model_2.h5")
print("Model saved successfully")