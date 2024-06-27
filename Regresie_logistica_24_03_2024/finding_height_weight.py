import requests


def get_height_and_weight(player_name):
    search_url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&search={player_name}&language=en"
    search_response = requests.get(search_url)
    search_data = search_response.json()

    print(search_data)

    if 'search' in search_data:
        if search_data['search']:
            entity_id = search_data['search'][0]['id']

            entity_url = f"https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json"
            entity_response = requests.get(entity_url)
            entity_data = entity_response.json()

            claims = entity_data['entities'][entity_id].get('claims', {})
            height_claim = claims.get('P2048', [])
            weight_claim = claims.get('P2067', [])

            height = height_claim[0]['mainsnak']['datavalue']['value']['amount'] if height_claim else None
            weight = weight_claim[0]['mainsnak']['datavalue']['value']['amount'] if weight_claim else None

            return height, weight
        else:
            return None, None
    else:
        return None, None


player_name = "Carlos Alcaraz"
height, weight = get_height_and_weight(player_name)
if height and weight:
    print(f"Player: {player_name}")
    print(f"Height: {height} meters")
    print(f"Weight: {weight} kilograms")
else:
    print("Height or weight information not found.")
