import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


# url = "https://www.wtatennis.com/players/314320/simona-halep#" + "matches"


def get_player_matches(url):
    try:
        service = Service()
        options = webdriver.Chrome()
        driver = webdriver.Chrome(service=service)
        driver.set_page_load_timeout(10)
        time.sleep(random.uniform(5, 10))
        driver.get(url)
        # if "404" in driver.title or "Page Not Found" in driver.page_source:
        #     print(f"Page {url} does not exist.")
        # else:
        #     print(f"Page {url} loaded successfully.")

        print(driver.title)
        time.sleep(random.uniform(5, 10))
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'player-matches__content'))
        )

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # data about the round, opponent, opponent rank, result, and score player-matches__tournament-header
        details_div = soup.find('div', class_='player-matches__content js-player-matches-content')
        # print(details_div)
        if details_div:
            matches = details_div.find_all('tr', class_='player-matches__match')
            tournaments = details_div.find_all('div', class_='player-matches__tournament')
            for match in matches:
                try:
                    round = match.find('div', class_='player-matches__match-round').text.strip()
                    first_name = match.find('span', class_='player-matches__match-opponent-first').text.strip()
                    last_name = match.find('span', class_='player-matches__match-opponent-last').text.strip()
                    opponent_rank = match.find('td', class_='player-matches__match-cell--opp-rank').text.strip()
                    result = match.find('td', class_='player-matches__match-cell--winloss').text.strip()
                    score = match.find('td', class_='player-matches__match-cell--score').text.strip()

                    # print(round)
                    # print(f"Opponent: {first_name + last_name}")
                    # print(f"Opponent rank: {opponent_rank}")
                    # print(f"Result: {result}")
                    # print(f"Score: {score}")
                    # print()
                except Exception as e:
                    print(f"Error: {e}")
            for tournament in tournaments:
                try:
                    tournament_name = tournament.find('a', class_='player-matches__tournament-title-link').text.strip()
                    location = tournament.find('span', class_='player-matches__tournament-location').text.strip()
                    date = tournament.find('span', class_='player-matches__tournament-date').text.strip()
                    before_surface = tournament.find('div', class_='player-matches__tournament-meta-item')
                    before_surface_text = before_surface.text.strip()

                    surface_div = before_surface.find_next('div', class_='player-matches__tournament-meta-item')
                    surface_text = surface_div.text.strip()

                    surface = "Not available"
                    if 'Surface' in before_surface_text:
                        surface = before_surface_text
                    if 'Surface' in surface_text:
                        surface = surface_text

                    # print(f"Surface: {surface}")
                    # print(f"Tournament: {tournament_name}")
                    # print(f"Location: {location}")
                    # print(f"Date: {date}")
                    # print()
                except Exception as e:
                    print(f"Error: {e}")
        else:
            print("Could not find the details section on the webpage.")
    except TimeoutException:
        print("Page load timed out.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()
