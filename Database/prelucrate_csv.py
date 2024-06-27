import csv
import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="student",
    host="localhost",
    port="5432"

)


def delete_data_from_csv(file_name):
    with open(file_name, mode='w', newline='') as file:
        pass

    print("Data has been erased from", file_name)


def switch_score(original_score):
    parts = original_score.split()
    swapped_scores = []

    for part in parts:
        scores = part.split('-')
        swapped_score = '-'.join([scores[1], scores[0]])
        swapped_scores.append(swapped_score)

    final_score = ' '.join(swapped_scores)

    return final_score


def data_2_players(row):
    best_of = int(float(row['Best of']))

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM players WHERE name=%s", (row['Player_1'],))
    rows_player = cursor.fetchall()
    id_player = rows_player[0][0]

    cursor.execute("SELECT id FROM players WHERE name=%s", (row['Player_2'],))
    rows_opponent = cursor.fetchall()
    id_opponent = rows_opponent[0][0]

    if row['Court'] == 'Indoor':
        court = 0
    else:
        court = 1

    if row['Surface'] == 'Clay':
        surface = 0
    elif row['Surface'] == 'Hard':
        surface = 1
    else:
        surface = 2

    data = [id_player, id_opponent, court, surface, best_of,
            int(row['Rank_1']), int(row['Rank_2'])]
    if row['Player_1'] == row['Winner']:
        data.append(1)
    else:
        data.append(0)

    # player2_score = switch_score(row['Score'].rstrip())
    data1 = [id_opponent, id_player, court, surface, best_of,
             int(row['Rank_2']), int(row['Rank_1'])]
    if row['Player_2'] == row['Winner']:
        data1.append(1)
    else:
        data1.append(0)

    cursor.close()
    return data, data1


def read_and_prelucrate_from_csv_file():
    with open('atp_tennis.csv', mode='r') as file:
        with open('post_atp_tennis.csv', mode='w', newline='') as output_file:
            csv_writer = csv.writer(output_file)
            csv_reader = csv.DictReader(file)
            header = csv_reader.fieldnames
            output_header = ['Player', 'Opponent', 'Court', 'Surface', 'Best_of', 'Rank_player',
                             'Rank_opponent', 'Output_label']
            csv_writer.writerow(output_header)
            i = 0
            for row in csv_reader:
                # if i == 9:
                #     break
                i += 1
                # print(row)
                if i % 10000 == 0:
                    print("Am ajuns la:", i)
                data, data1 = data_2_players(row)
                csv_writer.writerow(data)
                csv_writer.writerow(data1)

    print("Data has been written to post_atp_tennis.csv")


def delete_from_db(cursor):
    sql = 'DELETE FROM public.players;'
    cursor.execute(sql)
    conn.commit()


def transform_player_into_int():
    with open('atp_tennis.csv', mode='r') as file:
        cursor = conn.cursor()
        delete_from_db(cursor)
        print("Deleted all previous players!")

        csv_reader = csv.DictReader(file)
        header = csv_reader.fieldnames
        i = 0
        nr_players = 0
        for row in csv_reader:
            # if i == 9:
            #     break
            i += 1
            print(row['Player_1'], row['Player_2'])
            player_name = row['Player_1']
            oppponent_name = row['Player_2']

            cursor.execute("SELECT name, id FROM players WHERE name=%s", (player_name,))
            rows_player = cursor.fetchall()
            if len(rows_player) == 0:
                print("Player not found!")
                sql = 'INSERT INTO public.players(name, id) VALUES(%s,%s);'
                values = (player_name, nr_players)
                nr_players += 1
                cursor.execute(sql, values)
                conn.commit()
            else:
                print("Player Found!")

            # !!!for opponent side!
            cursor.execute("SELECT name, id FROM players WHERE name=%s", (oppponent_name,))
            rows_opponent = cursor.fetchall()
            if len(rows_opponent) == 0:
                print("Opponent not found!")
                sql = 'INSERT INTO public.players(name, id) VALUES(%s,%s);'
                values = (oppponent_name, nr_players)
                nr_players += 1
                cursor.execute(sql, values)
                conn.commit()
            else:
                print("Opponent Found!")
    print("Added " + str(nr_players) + " players to database!")
    cursor.close()


if __name__ == "__main__":
    delete_data_from_csv('post_atp_tennis.csv')
    read_and_prelucrate_from_csv_file()
    # transform_player_into_int()
    conn.close()
