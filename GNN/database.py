import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="student",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()


def insert_player(player_name, player_id):
    sql = 'INSERT INTO players_gnn("player_name", "player_id") VALUES(%s, %s);'
    values = (player_name, player_id)
    cursor.execute(sql, values)
    conn.commit()


def check_player(player_name):
    sql = 'SELECT player_id FROM players_gnn WHERE player_name = %s;'
    values = (player_name,)
    cursor.execute(sql, values)
    player = cursor.fetchone()
    if player is not None:
        return player[0]
    return None


if __name__ == "__main__":
    # read_and_insert_into_db_from_csv_file()
    # cursor.execute("SELECT * FROM tennis")
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    #
    # cursor.close()
    # conn.close()
    print("Hello world from database.py")
