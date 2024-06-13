import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

service = Service()
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode if you don't need a GUI
driver = webdriver.Chrome(service=service, options=options)

# URL of the webpage
url = "https://www.wtatennis.com/players"

# Open the webpage
driver.get(url)


# Function to scroll down the page
def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Adjust sleep time as needed


# Initial scroll to load dynamic content
scroll_down(driver)

# Keep scrolling until no new content is loaded
while True:
    # Get current page height
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll down to the bottom
    scroll_down(driver)

    time.sleep(5)  # Adjust sleep time as needed

    # Wait to see if new content loads
    WebDriverWait(driver, 20).until(
        lambda driver: driver.execute_script("return document.body.scrollHeight") > last_height
    )

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break

# Get the page source and parse it with BeautifulSoup
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Find all <a> elements with a specific class and extract the href attributes
player_links = soup.find_all('a',
                             class_='player-thumbnail__inner player-thumbnail__inner--link')  # Adjust the class name as needed

# Print the href attributes
for link in player_links:
    href = link.get('href')
    if href:
        print(href)

# Close the WebDriver
driver.quit()
