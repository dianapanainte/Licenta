import json


def reformat_score(score):
    # Split the score by dashes
    parts = score.split('-')

    # Initialize a list to store properly formatted score parts
    formatted_parts = []

    # Process each part
    for i in range(len(parts)):
        if i % 2 == 0 and i < len(parts) - 1:
            # Combine adjacent parts with a dash
            formatted_parts.append(f"{parts[i]}-{parts[i + 1]}")

    # Join the formatted parts with a comma and space
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


# Path to your JSON file
read_file = 'tournaments.json'
output_file = 'tournamentsFINAL.json'

# Process the JSON file
process_json(read_file, output_file)
