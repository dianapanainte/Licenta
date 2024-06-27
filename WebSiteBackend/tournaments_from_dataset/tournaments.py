import csv
import json


def get_tournaments():
    csv_file = 'F:/GithubCloning/Licenta/WebSiteBackend/stats/csv_folder/data_tour_not_use.csv'
    tournaments = []
    surfaces = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if 'Fed Cup' not in row[3] and 'BJK Cup' not in row[3] and 'Hertogenbosch' not in row[3] and row[
                    3] not in tournaments:
                tournaments.append(row[3])
                surfaces.append(row[4])
    zipped = zip(tournaments, surfaces)
    zipped_list = list(zipped)
    print(zipped_list)

    data_dict = [{'tournament': item[0], 'surface': item[1]} for item in zipped_list]
    with open('tournaments.json', 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)
    print(json.dumps(data_dict, indent=4))

    return zipped_list


get_tournaments()
# for tournament in tournaments:
#     print(tournament)
