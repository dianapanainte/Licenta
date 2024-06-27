import pandas as pd
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
import features
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.linear_model import LogisticRegression

pd.set_option('display.max_columns', None)

data = pd.DataFrame(features.data)

encoder = OneHotEncoder()
surface_encoded = encoder.fit_transform(data[['Hand']])
surface_encoded_df = pd.DataFrame(surface_encoded.toarray(), columns=encoder.get_feature_names_out(['Hand']))
data.drop('Hand', axis=1, inplace=True)
data = pd.concat([data, surface_encoded_df], axis=1)

# -----------------------------------------------------------for opponent hand
encoder = OneHotEncoder()
surface_encoded = encoder.fit_transform(data[['Opponent_Hand']])
surface_encoded_df = pd.DataFrame(surface_encoded.toarray(), columns=encoder.get_feature_names_out(['Opponent_Hand']))
data.drop('Opponent_Hand', axis=1, inplace=True)
data = pd.concat([data, surface_encoded_df], axis=1)

print(data)


def logistic_regression():
    # col_names = ['Player', 'Opponent', 'Date', 'Age', 'Rank', 'Hand', 'Height',
    #              'Wins_semester', 'Losses_semester', "Wins_year", "Losses_year",
    #              "Wins_clay", "Wins_hard", "Wins_grass", "Losses_clay", "Losses_hard", "Losses_grass", "Opponent_Age",
    #              "Opponent_Rank", "Opponent_Hand", "Opponent_Height", "Opponent_Wins_semester",
    #              "Opponent_Losses_semester", "Opponent_Wins_year", "Opponent_Losses_year", "Opponent_Wins_clay",
    #              "Opponent_Wins_hard", "Opponent_Wins_grass", "Opponent_Losses_clay", "Opponent_Losses_hard",
    #              "Opponent_Losses_grass", "Outcome"]
    # data = pd.read_csv("csv_folder/data_ver_0_0.csv_folder", header=0, names=col_names)
    # print(data.head())

    feature_cols = ['Difference_in_ranks', 'Different_hand', 'Age', 'Rank', 'Height', 'Wins_semester', 'Losses_semester',
                    "Wins_year", "Losses_year", "Wins_career", "Losses_career", "Wins_clay", "Wins_hard", "Wins_grass", "Losses_clay", "Losses_hard",
                    "Losses_grass", "Opponent_Age", "Opponent_Rank", "Opponent_Height", "Opponent_Wins_semester",
                    "Opponent_Losses_semester", "Opponent_Wins_year", "Opponent_Losses_year", "Opponent_Wins_career", "Opponent_Losses_career", "Opponent_Wins_clay",
                    "Opponent_Wins_hard", "Opponent_Wins_grass", "Opponent_Losses_clay", "Opponent_Losses_hard",
                    "Opponent_Losses_grass", "Hand_L", 'Hand_R', "Opponent_Hand_L", 'Opponent_Hand_R']
    X = data[feature_cols]
    y = data.Outcome

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=16)

    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    logreg = LogisticRegression(random_state=16, solver='lbfgs', max_iter=10000)

    logreg.fit(X_train, y_train)

    y_pred = logreg.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: {:.2f}%".format(accuracy * 100))

    # target_names = ['not winner', 'winner']
    print(classification_report(y_test, y_pred))

    # print(classification_report(y_test, y_pred, target_names=target_names))


if __name__ == "__main__":
    logistic_regression()
