import keras
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import classification_report
import OtherTries.ModelTestingWithStatistics as mts

print(tf.__version__)
print(keras.__version__)


# load the model
model = keras.models.load_model("my_model.h5")
print("Model loaded successfully")
# print("Before generate_for_test_set")
# X_test, y_test = mts.generate_for_test_set(mts.y_test)
# print("After generate_for_test_set")
# # write the new X_test to a file
# X_test.to_csv("X_test.csv", index=False)
# y_test.to_csv("y_test.csv", index=False)

X_test = pd.read_csv("X_test.csv")
y_test = pd.read_csv("y_test.csv")
#drop player names
X_test = X_test.drop(['Player1_name', 'Player2_name', 'Player1_id',  'Player2_id'], axis=1)

X_test = tf.convert_to_tensor(X_test, dtype=tf.float64)
test_loss, test_acc = model.evaluate(X_test, y_test)

y_pred_test = model.predict(X_test)
y_pred_test = [int(i > .5) for i in y_pred_test]

print(classification_report(y_test, y_pred_test))
