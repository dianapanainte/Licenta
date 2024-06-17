import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

service = Service()
options = webdriver.Chrome()
driver = webdriver.Chrome(service=service)
url = "https://www.wtatennis.com/tournaments"
driver.get(url)
print(driver.title)
time.sleep(random.uniform(5, 10))


def load_all_tournaments():
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.HOME)

    # Initial height of the page
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom of the page
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

        # Wait for new content to load
        time.sleep(8)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        # Break the loop if no new content is loaded
        if new_height == last_height:
            break
        last_height = new_height


# Call the function to load all tournaments
load_all_tournaments()

# Get the page source and parse it with Beautiful Soup
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

tournaments = []
for tournament in soup.find_all('li', class_='tournament-list__item'):
    print(tournament)
    try:
        date = tournament.find('div', class_='tournament-thumbnail__date').text.strip()
        surface = tournament.find('div', class_='tournament-thumbnail__tags').text.strip()
        title = tournament.find('h3', class_='tournament-thumbnail__title').text.strip()
        location = tournament.find('span', class_='tournament-thumbnail__location').text.strip()
        tournaments.append({
            'date': date,
            'surface': surface,
            'title': title,
            'location': location
        })
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(1)

driver.quit()

print(f'Total tournaments found: {len(tournaments)}')
for tournament in tournaments:
    print(tournament)
