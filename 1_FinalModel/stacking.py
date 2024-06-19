import NeuralNetwork.annWithValidation as annWithValidation
import NeuralNetwork.annWithTournament as annWithTournament
import Regresie_logistica_24_03_2024.LogisticRegression_3_0 as LogisticRegression
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from NeuralNetwork import features
import matplotlib.pyplot as plt
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD

LR, scaler, X_test_lr, X_new_lr = LogisticRegression.logistic_regression()

ann_val_pred = annWithValidation.model_ann_validation.predict(annWithValidation.X_test)
ann_tour_pred = annWithTournament.model_ann_tournament.predict(annWithTournament.X_test)
log_reg_pred = LR.predict(X_test_lr)

X_val_meta = np.column_stack((ann_val_pred, ann_tour_pred, log_reg_pred))
y_val_meta = annWithValidation.y_test
meta_model = Sequential([
    Dense(1, input_dim=X_val_meta.shape[1], activation='sigmoid')
])

meta_model.compile(optimizer=SGD(), loss='binary_crossentropy', metrics=['accuracy'])
history = meta_model.fit(X_val_meta, y_val_meta, epochs=50, verbose=1)

plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Training Accuracy')
plt.legend()
plt.show()

# ----------------------------------PREDICT ON TEST-------------------------
X_new = annWithValidation.X_val
X_new_tour = annWithTournament.X_val
ann_val_pred_new = annWithValidation.model_ann_validation.predict(X_new)
ann_tour_pred_new = annWithTournament.model_ann_tournament.predict(X_new_tour)
lr_pred_new = LR.predict(X_new_lr)

X_new_meta = np.column_stack((ann_val_pred_new, ann_tour_pred_new, lr_pred_new))
y_new_pred = annWithValidation.y_val
loss, accuracy = meta_model.evaluate(X_new_meta, y_new_pred)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')
