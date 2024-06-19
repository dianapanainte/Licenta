import json
import re


def clean_name(name):
    match = re.match(r"\('([^']*)',\)", name)
    return match.group(1) if match else name


def clean_and_concatenate_json_files(file1_path, file2_path, output_file_path):
    try:
        with open(file1_path, 'r') as file1:
            data1 = json.load(file1)

        with open(file2_path, 'r') as file2:
            data2 = json.load(file2)

        if isinstance(data1, list) and isinstance(data2, list):
            for entry in data1:
                if 'name' in entry:
                    entry['name'] = clean_name(entry['name'])
            for entry in data2:
                if 'name' in entry:
                    entry['name'] = clean_name(entry['name'])

            concatenated_data = data1 + data2
        else:
            raise ValueError("Both JSON files must contain lists.")

        with open(output_file_path, 'w') as output_file:
            json.dump(concatenated_data, output_file, indent=4)

        print(f"Successfully cleaned and concatenated JSON files into {output_file_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except ValueError as e:
        print(f"Error: {e}")


file1_path = 'all_tournaments.json'
file2_path = 'tournaments_5.json'
output_file_path = 'tournaments.json'

clean_and_concatenate_json_files(file1_path, file2_path, output_file_path)
