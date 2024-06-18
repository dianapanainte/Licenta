import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from GNN import database as gnn

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service)

driver.get('https://www.wtatennis.com/players')

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

no_results = []


def get_player_list():
    players = gnn.get_last_players()
    return players


players_list = get_player_list()

button_search = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'player-search__button'))
)
if button_search:
    print("Found the search button")
else:
    print("Could not find the search button")
button_search.click()


def search_player(player_name):
    search_bar = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'player-search__input'))
    )
    search_bar.clear()

    search_bar.send_keys(player_name)
    time.sleep(2)

    try:
        search_results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'players__list-item'))
        )
        print(f"Found {len(search_results)} search results for {player_name}")

        for result in search_results:
            return result.find_element(By.TAG_NAME, 'a').get_attribute('href')
    except Exception as e:
        print(f"No results found for {player_name}")
        no_results.append(player_name)
        return None
    finally:
        search_bar.clear()


def get_players_urls():
    urls = []
    player_names = []
    for player in players_list:
        player_url = search_player(player)
        if player_url:
            urls.append(player_url)
            player_names.append(player)
        else:
            print(f"Could not find {player}")
        print(f"{player}: {player_url}")
    return urls, player_names


urls, player_names = get_players_urls()

with open('no_results_2020-2023.txt', 'w') as file:
    for player in no_results:
        file.write(f"{player}\n")

with open('players_urls_2020-2023.txt', 'w') as file:
    for url in urls:
        file.write(f"{url}\n")

with open('player_names_2020-2023.txt', 'w') as file:
    for name in player_names:
        file.write(f"{name}\n")

driver.quit()
