import json


def reformat_score(score):
    parts = score.split('-')
    formatted_parts = []
    for i in range(len(parts)):
        if i % 2 == 0 and i < len(parts) - 1:
            formatted_parts.append(f"{parts[i]}-{parts[i + 1]}")
    formatted_score = ', '.join(formatted_parts)
    return formatted_score


def process_json(read_file, output_file):
    with open(read_file, 'r') as file:
        data = json.load(file)

    for entry in data:
        if 'score' in entry:
            entry['score'] = reformat_score(entry['score'])

    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)


read_file = 'tournaments.json'
output_file = 'tournamentsFINAL.json'

process_json(read_file, output_file)
