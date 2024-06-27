import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.linear_model import LogisticRegression


def logistic_regression():
    col_names = ['Player', 'Opponent', 'Court', 'Surface', 'Best_of', 'Rank_player', 'Rank_opponent',
                 'Output_label']
    date_columns = ['Date']
    data = pd.read_csv("post_atp_tennis.csv", header = 0, names=col_names)
    print(data.head())

    feature_cols = ['Player', 'Opponent', 'Court', 'Surface', 'Best_of', 'Rank_player',
                    'Rank_opponent']
    X = data[feature_cols]
    y = data.Output_label

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=16)

    logreg = LogisticRegression(random_state=16)

    logreg.fit(X_train, y_train)

    y_pred = logreg.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: {:.2f}%".format(accuracy * 100))

    # target_names = ['not winner', 'winner']
    print(classification_report(y_test, y_pred))
    # print(classification_report(y_test, y_pred, target_names=target_names))


if __name__ == "__main__":
    logistic_regression()
