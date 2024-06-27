import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


# url = "https://www.wtatennis.com/players/314320/simona-halep" + "#matches"
# url = "https://www.wtatennis.com/players/326408/iga-swiatek" + "#matches"
# url = "https://www.wtatennis.com/players/230220/venus-williams" + "#matches"
# url = "https://www.wtatennis.com/players/314584/kiki-bertens" + "#matches"


def get_player_matches(url):
    try:
        data = []
        service = Service()
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(10)
        # time.sleep(random.uniform(5, 10))
        driver.get(url)
        if "404" in driver.title or "Page Not Found" in driver.page_source:
            print(f"Page {url} does not exist.")
        else:
            print(f"Page {url} loaded successfully.")

        print(driver.title)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'player-matches__content'))
        )
        # time.sleep(random.uniform(5, 10))

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # data about the round, opponent, opponent rank, result, and score player-matches__tournament-header
        details_div = soup.find('div', class_='player-matches__content')
        # print(details_div)
        if details_div:
            matches = details_div.find_all('tr', class_='player-matches__match')
            tournaments = details_div.find_all('div', class_='player-matches__tournament')
            if not matches or not tournaments:
                print("No matches found.")
                return None
            for match, tournament in zip(matches, tournaments):
                try:
                    round = match.find('div', class_='player-matches__match-round')
                    round = round.text.strip() if round else "Not available"
                    first_name = match.find('span', class_='player-matches__match-opponent-first')
                    first_name = first_name.text.strip() if first_name else "Not available"
                    last_name = match.find('span', class_='player-matches__match-opponent-last')
                    last_name = last_name.text.strip() if last_name else "Not available"
                    opponent_rank = match.find('td', class_='player-matches__match-cell--opp-rank')
                    opponent_rank = opponent_rank.text.strip() if opponent_rank else "Not available"
                    result = match.find('td', class_='player-matches__match-cell--winloss')
                    result = result.text.strip() if result else "Not available"
                    score = match.find('td', class_='player-matches__match-cell--score')
                    score = score.text.strip() if score else "Not available"

                    # print(round)
                    # print(f"Opponent: {first_name + " " + last_name}")
                    # print(f"Opponent rank: {opponent_rank}")
                    # print(f"Result: {result}")
                    # print(f"Score: {score}")

                    tournament_name = tournament.find('a', class_='player-matches__tournament-title-link')
                    tournament_name = tournament_name.text.strip() if tournament_name else "Not available"
                    location = tournament.find('span', class_='player-matches__tournament-location')
                    location = location.text.strip() if location else "Not available"
                    date = tournament.find('span', class_='player-matches__tournament-date')
                    date = date.text.strip() if date else "Not available"
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
                    return_match = {
                        'round': round,
                        'opponent_player': first_name + " " + last_name,
                        'opponent_rank': opponent_rank,
                        'result': result,
                        'score': score,
                        'tournament': tournament_name,
                        'location': location,
                        'date': date,
                        'surface': surface
                    }
                    data.append(return_match)
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
        return data

# data = get_player_matches(url)
# print(data)
