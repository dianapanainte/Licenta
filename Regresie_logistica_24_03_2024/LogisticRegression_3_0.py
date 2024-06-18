import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
import Features_3_0 as features
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
import joblib

pd.set_option('display.max_columns', None)


def one_hot_encoding(data):
    encoder = OneHotEncoder()
    surface_encoded = encoder.fit_transform(data[['Hand']])
    surface_encoded_df = pd.DataFrame(surface_encoded.toarray(), columns=encoder.get_feature_names_out(['Hand']))
    data.drop('Hand', axis=1, inplace=True)
    data = pd.concat([data, surface_encoded_df], axis=1)
    # -----------------------------------------------------------for opponent hand
    encoder = OneHotEncoder()
    surface_encoded = encoder.fit_transform(data[['Opponent_Hand']])
    surface_encoded_df = pd.DataFrame(surface_encoded.toarray(),
                                      columns=encoder.get_feature_names_out(['Opponent_Hand']))
    data.drop('Opponent_Hand', axis=1, inplace=True)
    data = pd.concat([data, surface_encoded_df], axis=1)
    return data


def logistic_regression():
    feature_cols = ['Difference_in_ranks', 'Different_hand', 'Age', 'Rank', 'Height', 'Wins_semester',
                    'Losses_semester',
                    "Wins_year", "Losses_year", "Wins_clay", "Wins_hard", "Wins_grass", "Losses_clay", "Losses_hard",
                    "Losses_grass", "Opponent_Age", "Opponent_Rank", "Opponent_Height", "Opponent_Wins_semester",
                    "Opponent_Losses_semester", "Opponent_Wins_year", "Opponent_Losses_year", "Opponent_Wins_clay",
                    "Opponent_Wins_hard", "Opponent_Wins_grass", "Opponent_Losses_clay", "Opponent_Losses_hard",
                    "Opponent_Losses_grass"]

    # Training data
    data_training = pd.DataFrame(features.training_data())
    data_training = one_hot_encoding(data_training)
    X_train = data_training[feature_cols]
    y_train = data_training.Outcome
    value_counts = y_train.value_counts()

    print("Value counts:")
    print(value_counts)

    # Testing data
    data_testing = pd.DataFrame(features.testing_data())
    data_testing = one_hot_encoding(data_testing)
    X_test = data_testing[feature_cols]  # Features
    y_test = data_testing.Outcome  # Target variable

    # Normalize data
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.fit_transform(X_test)

    logreg = LogisticRegression(random_state=16, solver='lbfgs', max_iter=10000)
    logreg.fit(X_train, y_train)
    y_pred = logreg.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: {:.2f}%".format(accuracy * 100))
    target_names = ['not winner', 'winner']
    print(classification_report(y_test, y_pred, target_names=target_names))

    #########################
    y_true = np.array(y_test)
    y_pred = np.array(y_pred)

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)

    # Plot confusion matrix as heatmap
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')

    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()
    plt.savefig('plots/confusion_matrix_features_3_0_2004-2016.png')
    return logreg, scaler


if __name__ == "__main__":
    model, scaler = logistic_regression()
    joblib.dump(model, 'logistic_regression_model.joblib')
    loaded_model = joblib.load('logistic_regression_model.joblib')

    new_data = np.array([38, 0, 32.9, 137, 175, 4, 2, 6, 12, 25, 22, 10, 19,
                36, 8, 27.4, 99, 160, 2, 4, 12, 6, 19, 36, 8, 25, 22, 10])
    new_data = scaler.fit_transform(np.reshape(new_data, (1, -1)))
    # predicted_classes = loaded_model.predict(np.reshape(new_data, (1, -1)))
    predicted_classes = loaded_model.predict(new_data)
    print("Predicted classes:", predicted_classes)



