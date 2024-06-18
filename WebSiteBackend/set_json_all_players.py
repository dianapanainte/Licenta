import json
import favourites_age as fa
import matches as ma
import time

# players_urls, player_names = ps.get_players_urls()
final_players_data = []
tournaments_data = []
no_matches = []
with open('players_urls_2020-2023.txt', 'r') as file:
    players_urls = file.readlines()
    players_urls = [url.strip() for url in players_urls]

with open('player_names_2020-2023.txt', 'r') as file:
    player_names = file.readlines()
    player_names = [name.strip() for name in player_names]

for i in range(len(players_urls)):
    player_url = players_urls[i]
    player_name = player_names[i]
    print(f"Processing {player_url}")
    try:
        ranking, height, hand, birthday, country = fa.get_player_details(player_url + "#overview")
        final_players_data.append({
            'name': player_name,
            'ranking': ranking,
            'height': height,
            'hand': hand,
            'date_of_birth': birthday,
            'country': country
        })
    except Exception as e:
        print(f"Error: {e}")
        final_players_data.append({
            'name': player_name,
            'ranking': "Not available",
            'height': "Not available",
            'hand': "Not available",
            'date_of_birth': "Not available",
            'country': "Not available"
        })
        no_matches.append(player_name)
        continue
    print(f"Finished processing {player_name}")
    print(f"Ranking: {ranking}, Height: {height}, Hand: {hand}, Birthday: {birthday}, Country: {country}")


with open('players_2020-2023.json', 'w') as file:
    json.dump(final_players_data, file, indent=4)

# evry plaer's matches, this takes a while

for i in range(len(players_urls)):
    player_url = players_urls[i]
    player_name = player_names[i]
    print(f"Processing {player_url}")

    player_matches_url = player_url + "#matches"
    player_matches = ma.get_player_matches(player_matches_url)
    finaL_match = []
    if not player_matches:
        print(f"No matches found for {player_name}")
        no_matches.append(player_name)
        continue
    for match in player_matches:
        try:
            tournaments_data.append({
                'player': player_name,
                'date': match['date'],
                'name': match['name'],
                'opponent_player': match['opponent_player'],
                'opponent_rank': match['opponent_rank'],
                'location': match['location'],
                'surface': match['surface'],
                'round': match['round'],
                'score': match['score'],
                'result': match['result']
            })
            finaL_match = {
                'date': match['date'],
                'name': match['name'],
                'opponent_player': match['opponent_player'],
                'opponent_rank': match['opponent_rank'],
                'location': match['location'],
                'surface': match['surface'],
                'round': match['round'],
                'score': match['score'],
                'result': match['result']
            }
        except Exception as e:
            print(f"Error: {e}")
    print(f"Finished processing {player_name}")
    print(
        f"Date: :'{finaL_match['date']}', Name: '{finaL_match['name']}', Opponent Player: '{finaL_match['opponent_player']}', Opponent Rank: '{finaL_match['opponent_rank']}', Location: '{finaL_match['location']}', Surface: '{finaL_match['surface']}', Round: '{finaL_match['round']}', Score: '{finaL_match['score']}', Result: '{finaL_match['result']}'")
    time.sleep(1)


with open('tournaments_2020-2023.json', 'w') as file:
    json.dump(tournaments_data, file, indent=4)

with open('players_with_no_recent_matches.txt', 'w') as file:
    for player in no_matches:
        file.write(f"{player}\n")
