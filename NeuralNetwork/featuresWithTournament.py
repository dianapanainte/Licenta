import csv
from datetime import datetime, timedelta
import random

# Set a larger field size limit to avoid error
csv.field_size_limit(100000000)


def initialize_data():
    data = {
        "Player": [],
        "Opponent": [],
        "Date": [],
        "Tournament": [],
        "Surface": [],
        "Round": [],
        "Difference_in_ranks": [],
        "Different_hand": [],
        "Age": [],
        "Rank": [],
        "Hand": [],
        "Height": [],
        "Wins_semester": [],
        "Losses_semester": [],
        "Wins_year": [],
        "Losses_year": [],
        # "Wins_career": [], #TBD, when i add more years, not only 2023
        # "Losses_career": [],
        "Wins_clay": [],
        "Wins_hard": [],
        "Wins_grass": [],
        "Losses_clay": [],
        "Losses_hard": [],
        "Losses_grass": [],
        "Opponent_Age": [],
        "Opponent_Rank": [],
        "Opponent_Hand": [],
        "Opponent_Height": [],
        "Opponent_Wins_semester": [],
        "Opponent_Losses_semester": [],
        "Opponent_Wins_year": [],
        "Opponent_Losses_year": [],
        # "Wins_career": [], #TBD, when i add more years, not only 2023
        # "Losses_career": [],
        "Opponent_Wins_clay": [],
        "Opponent_Wins_hard": [],
        "Opponent_Wins_grass": [],
        "Opponent_Losses_clay": [],
        "Opponent_Losses_hard": [],
        "Opponent_Losses_grass": [],
        "Outcome": []
    }

    players = {}
    return data, players


def convert_to_date(date_str):
    return datetime.strptime(date_str, '%Y%m%d')


# check if a date falls within the last 6 months
def within_last_6_months(date_of_the_game):
    six_months_ago = convert_to_date("20141231") - timedelta(days=30 * 6)
    return date_of_the_game >= six_months_ago


def within_last_year(date):
    a_year_ago = convert_to_date("20141231") - timedelta(days=30 * 12)
    return date >= a_year_ago


def extract_from_row_for_player(row):
    date = row[5]
    semester = 0
    year = 0
    if within_last_6_months(convert_to_date(date)):
        semester = 1
    if within_last_year(convert_to_date(date)):
        year = 1
    return semester, year


def set_wins_losses(i, more_specific, data, players):
    if (data['Player'][i], more_specific) in players.keys():
        data[more_specific][i] = players[(data['Player'][i], more_specific)]
    else:
        data[more_specific][i] = 0


def read_csv(csv_file, data, players):
    i = 0
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[1] == '' or row[2] == '' or row[25] == '' or row[5] == '' or row[10] == '' or row[11] == '' or row[12] == '' or row[14] == '' or row[45] == '' or row[
                18] == '' or row[19] == '' or row[20] == '' or row[22] == '' or row[47] == '':
                continue
            # i += 1
            # if i == 2:
            #     break
            random_choose = random.randint(0, 1)
            if random_choose == 0:
                data["Date"].append(row[5])
                data["Tournament"].append(row[1])
                data["Surface"].append(row[2])
                data["Round"].append(row[25])
                data["Player"].append(row[10])
                data["Hand"].append(row[11])
                data['Height'].append(row[12])
                data['Difference_in_ranks'].append(abs(int(float(row[45])) - int(float(row[47]))))
                data['Different_hand'].append(0 if row[11] == row[19] else 1)
                data["Age"].append(row[14])
                data["Rank"].append(row[45])
                data["Opponent"].append(row[18])
                data["Opponent_Hand"].append(row[19])
                data['Opponent_Height'].append(row[20])
                data["Opponent_Age"].append(row[22])
                data["Opponent_Rank"].append(row[47])
                data["Outcome"].append(1)
                # -----
                data['Wins_semester'].append(0)
                data['Losses_semester'].append(0)
                data['Wins_year'].append(0)
                data['Losses_year'].append(0)
                data['Wins_hard'].append(0)
                data['Losses_hard'].append(0)
                data['Wins_clay'].append(0)
                data['Losses_clay'].append(0)
                data['Wins_grass'].append(0)
                data['Losses_grass'].append(0)
                # ------
                data['Opponent_Wins_semester'].append(0)
                data['Opponent_Losses_semester'].append(0)
                data['Opponent_Wins_year'].append(0)
                data['Opponent_Losses_year'].append(0)
                data['Opponent_Wins_hard'].append(0)
                data['Opponent_Losses_hard'].append(0)
                data['Opponent_Wins_clay'].append(0)
                data['Opponent_Losses_clay'].append(0)
                data['Opponent_Wins_grass'].append(0)
                data['Opponent_Losses_grass'].append(0)

                player_semester, player_year = extract_from_row_for_player(row)
                if (row[10], 'Wins_semester') not in players.keys():
                    if player_semester == 1:
                        players[(row[10], 'Wins_semester')] = 1
                    else:
                        players[(row[10], 'Wins_semester')] = 0
                else:
                    players[(row[10], 'Wins_semester')] += player_semester

                if (row[10], 'Wins_year') not in players.keys():
                    if player_year == 1:
                        players[(row[10], 'Wins_year')] = 1
                    else:
                        players[(row[10], 'Wins_year')] = 0
                else:
                    players[(row[10], 'Wins_year')] += player_year

                if row[2] == 'Hard':
                    if (row[10], 'Wins_hard') not in players.keys():
                        players[(row[10], 'Wins_hard')] = 1
                    else:
                        players[(row[10], 'Wins_hard')] += 1
                elif row[2] == 'Clay':
                    if (row[10], 'Wins_clay') not in players.keys():
                        players[(row[10], 'Wins_clay')] = 1
                    else:
                        players[(row[10], 'Wins_clay')] += 1
                elif row[2] == 'Grass':
                    if (row[10], 'Wins_grass') not in players.keys():
                        players[(row[10], 'Wins_grass')] = 1
                    else:
                        players[(row[10], 'Wins_grass')] += 1
                # ----------------------------------------------
                opponent_semester, opponent_year = extract_from_row_for_player(row)
                if (row[10], 'Opponent_Losses_semester') not in players.keys():
                    if opponent_semester == 1:
                        players[(row[10], 'Opponent_Losses_semester')] = 1
                    else:
                        players[(row[10], 'Opponent_Losses_semester')] = 0
                else:
                    players[(row[10], 'Opponent_Losses_semester')] += opponent_semester

                if (row[10], 'Opponent_Losses_year') not in players.keys():
                    if opponent_year == 1:
                        players[(row[10], 'Opponent_Losses_year')] = 1
                    else:
                        players[(row[10], 'Opponent_Losses_year')] = 0
                else:
                    players[(row[10], 'Opponent_Losses_year')] += opponent_year

                if row[2] == 'Hard':
                    if (row[10], 'Opponent_Losses_hard') not in players.keys():
                        players[(row[10], 'Opponent_Losses_hard')] = 1
                    else:
                        players[(row[10], 'Opponent_Losses_hard')] += 1
                elif row[2] == 'Clay':
                    if (row[10], 'Opponent_Losses_clay') not in players.keys():
                        players[(row[10], 'Opponent_Losses_clay')] = 1
                    else:
                        players[(row[10], 'Opponent_Losses_clay')] += 1
                elif row[2] == 'Grass':
                    if (row[10], 'Opponent_Losses_grass') not in players.keys():
                        players[(row[10], 'Opponent_Losses_grass')] = 1
                    else:
                        players[(row[10], 'Opponent_Losses_grass')] += 1
            # -----------------------------------------------
            elif random_choose == 1:
                data["Tournament"].append(row[1])
                data["Surface"].append(row[2])
                data["Round"].append(row[25])
                data["Date"].append(row[5])
                data["Player"].append(row[18])
                data["Hand"].append(row[19])
                data['Height'].append(row[20])
                data['Difference_in_ranks'].append(abs(int(float(row[45])) - int(float(row[47]))))
                data['Different_hand'].append(0 if row[19] == row[11] else 1)
                data["Age"].append(row[22])
                data["Rank"].append(row[47])
                data["Opponent"].append(row[10])
                data["Opponent_Hand"].append(row[11])
                data['Opponent_Height'].append(row[12])
                data["Opponent_Age"].append(row[14])
                data["Opponent_Rank"].append(row[45])
                data["Outcome"].append(0)

                # -------
                data['Wins_semester'].append(0)
                data['Losses_semester'].append(0)
                data['Wins_year'].append(0)
                data['Losses_year'].append(0)
                data['Wins_hard'].append(0)
                data['Losses_hard'].append(0)
                data['Wins_clay'].append(0)
                data['Losses_clay'].append(0)
                data['Wins_grass'].append(0)
                data['Losses_grass'].append(0)
                # ------
                data['Opponent_Wins_semester'].append(0)
                data['Opponent_Losses_semester'].append(0)
                data['Opponent_Wins_year'].append(0)
                data['Opponent_Losses_year'].append(0)
                data['Opponent_Wins_hard'].append(0)
                data['Opponent_Losses_hard'].append(0)
                data['Opponent_Wins_clay'].append(0)
                data['Opponent_Losses_clay'].append(0)
                data['Opponent_Wins_grass'].append(0)
                data['Opponent_Losses_grass'].append(0)

                opponent_semester, opponent_year = extract_from_row_for_player(row)
                if (row[18], 'Losses_semester') not in players.keys():
                    if opponent_semester == 1:
                        players[(row[18], 'Losses_semester')] = 1
                    else:
                        players[(row[18], 'Losses_semester')] = 0
                else:
                    players[(row[18], 'Losses_semester')] += opponent_semester

                if (row[18], 'Losses_year') not in players.keys():
                    if opponent_year == 1:
                        players[(row[18], 'Losses_year')] = 1
                    else:
                        players[(row[18], 'Losses_year')] = 0
                else:
                    players[(row[18], 'Losses_year')] += opponent_year

                if row[2] == 'Hard':
                    if (row[18], 'Losses_hard') not in players.keys():
                        players[(row[18], 'Losses_hard')] = 1
                    else:
                        players[(row[18], 'Losses_hard')] += 1
                elif row[2] == 'Clay':
                    if (row[18], 'Losses_clay') not in players.keys():
                        players[(row[18], 'Losses_clay')] = 1
                    else:
                        players[(row[18], 'Losses_clay')] += 1
                elif row[2] == 'Grass':
                    if (row[18], 'Losses_grass') not in players.keys():
                        players[(row[18], 'Losses_grass')] = 1
                    else:
                        players[(row[18], 'Losses_grass')] += 1
                    # -------------------------------------
                player_semester, player_year = extract_from_row_for_player(row)
                if (row[18], 'Opponent_Wins_semester') not in players.keys():
                    if player_semester == 1:
                        players[(row[18], 'Opponent_Wins_semester')] = 1
                    else:
                        players[(row[18], 'Opponent_Wins_semester')] = 0
                else:
                    players[(row[18], 'Opponent_Wins_semester')] += player_semester

                if (row[18], 'Opponent_Wins_year') not in players.keys():
                    if player_year == 1:
                        players[(row[18], 'Opponent_Wins_year')] = 1
                    else:
                        players[(row[18], 'Opponent_Wins_year')] = 0
                else:
                    players[(row[18], 'Opponent_Wins_year')] += player_year

                if row[2] == 'Hard':
                    if (row[18], 'Opponent_Wins_hard') not in players.keys():
                        players[(row[18], 'Opponent_Wins_hard')] = 1
                    else:
                        players[(row[18], 'Opponent_Wins_hard')] += 1
                elif row[2] == 'Clay':
                    if (row[18], 'Opponent_Wins_clay') not in players.keys():
                        players[(row[18], 'Opponent_Wins_clay')] = 1
                    else:
                        players[(row[18], 'Opponent_Wins_clay')] += 1
                elif row[2] == 'Grass':
                    if (row[18], 'Opponent_Wins_grass') not in players.keys():
                        players[(row[18], 'Opponent_Wins_grass')] = 1
                    else:
                        players[(row[18], 'Opponent_Wins_grass')] += 1
                # -----------------------------------
    for i in range(len(data['Player'])):
        set_wins_losses(i, 'Wins_semester', data, players)
        set_wins_losses(i, 'Losses_semester', data, players)
        set_wins_losses(i, 'Wins_year', data, players)
        set_wins_losses(i, 'Losses_year', data, players)
        set_wins_losses(i, 'Wins_hard', data, players)
        set_wins_losses(i, 'Losses_hard', data, players)
        set_wins_losses(i, 'Wins_clay', data, players)
        set_wins_losses(i, 'Losses_clay', data, players)
        set_wins_losses(i, 'Wins_grass', data, players)
        set_wins_losses(i, 'Losses_grass', data, players)
        # --------------------------------------opponent
        set_wins_losses(i, 'Opponent_Wins_semester', data, players)
        set_wins_losses(i, 'Opponent_Losses_semester', data, players)
        set_wins_losses(i, 'Opponent_Wins_year', data, players)
        set_wins_losses(i, 'Opponent_Losses_year', data, players)
        set_wins_losses(i, 'Opponent_Wins_hard', data, players)
        set_wins_losses(i, 'Opponent_Losses_hard', data, players)
        set_wins_losses(i, 'Opponent_Wins_clay', data, players)
        set_wins_losses(i, 'Opponent_Losses_clay', data, players)
        set_wins_losses(i, 'Opponent_Wins_grass', data, players)
        set_wins_losses(i, 'Opponent_Losses_grass', data, players)


def training_data():
    # !!!when adding/deleting more years from the csv files, make sure to update the function from above ^^^^^
    data, players = initialize_data()
    read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/wta_matches_2004.csv', data, players)
    read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/wta_matches_2005.csv', data, players)
    read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/wta_matches_2006.csv', data, players)
    read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/wta_matches_2007.csv', data, players)
    read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/wta_matches_2008.csv', data, players)
    read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/wta_matches_2009.csv', data, players)
    read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/wta_matches_2010.csv', data, players)
    read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/wta_matches_2011.csv', data, players)
    read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/wta_matches_2012.csv', data, players)
    read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/wta_matches_2013.csv', data, players)
    read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/wta_matches_2014.csv', data, players)

    csv_output = 'F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/data_tour.csv'
    with open(csv_output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())

        writer.writeheader()

        for i in range(len(data['Player'])):
            row = {key: data[key][i] for key in data.keys()}
            writer.writerow(row)

    print("CSV file has been created successfully.")
    return data


def validation_data():
    data_validation, players_validation = initialize_data()
    read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/wta_matches_2015.csv', data_validation, players_validation)
    read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/wta_matches_2016.csv', data_validation, players_validation)
    return data_validation


def testing_data():
    data_test, players_test = initialize_data()
    read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/wta_matches_2017.csv', data_test, players_test)
    read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/wta_matches_2018.csv', data_test, players_test)
    read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/wta_matches_2019.csv', data_test, players_test)
    return data_test


if __name__ == '__main__':
    training_data()
