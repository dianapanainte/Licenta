import csv
import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="student",
    host="localhost",
    port="5432"

)

cursor = conn.cursor()


def read_and_insert_into_db_from_csv_file():
    with open('atp_tennis.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        header = csv_reader.fieldnames
        for row in csv_reader:
            print(row)
            sql = "INSERT INTO tennis (Tournament, Date, ) VALUES (%s, %s)"
            values = ('value1', 'value2')
            cursor.execute(sql, values)
            conn.commit()


read_and_insert_into_db_from_csv_file()
cursor.execute("SELECT * FROM tennis")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
conn.close()
