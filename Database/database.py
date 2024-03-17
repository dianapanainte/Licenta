import csv
# import psycopg2
#
# conn = psycopg2.connect(
#     dbname="postgres",
#     user="postgres",
#     password="student",
#     host="localhost",
#     port="5432"
#
# )
#
# cursor = conn.cursor()


# def read_and_insert_into_db_from_csv_file():
#     with open('atp_tennis.csv', mode='r') as file:
#         csv_reader = csv.DictReader(file)
#         header = csv_reader.fieldnames
#         i = 0
#         for row in csv_reader:
#             if i == 10000:
#                 break
#             print(row)
#             sql = 'INSERT INTO public.tennis("Tournament", "Date", "Series", "Surface", "Round", "Best_of", "Player_1", "Player_2", "Winner", "Rank_1", "Rank_2", "Pts_1", "Pts_2", "Odd_1", "Odd_2", "Score")\
#                 VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
#             values = (row['Tournament'], row['Date'], row['Series'], row['Surface'], row['Round'], row['Best of'], row['Player_1'], row['Player_2'], row['Winner'], row['Rank_1'], row['Rank_2'], row['Pts_1'], row['Pts_2'], row['Odd_1'], row['Odd_2'], row['Score'])
#             cursor.execute(sql, values)
#             conn.commit()
#             i += 1


if __name__ == "__main__":
    # read_and_insert_into_db_from_csv_file()
    # cursor.execute("SELECT * FROM tennis")
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    #
    # cursor.close()
    # conn.close()
    # import pandas
    import pandas as pd

    col_names = ['Tournament', 'Date', 'Series', 'Court', 'Surface', 'Round', 'Best of', 'Player_1', 'label']
    # load dataset
    dataset = pd.read_csv("atp_tennis.csv", header=None, names=col_names)
    # split dataset in features and target variable
    feature_cols = ['pregnant', 'insulin', 'bmi', 'age', 'glucose', 'bp', 'pedigree']
    X = dataset[feature_cols]  # Features
    y = dataset.label  # Target variable