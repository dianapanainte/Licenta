import requests
from bs4 import BeautifulSoup

url = "https://www.wtatennis.com/players/314320/simona-halep#overview"
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    details_div = soup.find('div', class_='profile-header-info__details')
    if details_div:
        height_span = details_div.find('div', class_='profile-header-info__detail')
        height = height_span.find_next('span',
                                       class_='profile-header-info__detail-height').text.strip() if height_span else "Not available"

        hand_div = details_div.find('div', class_='profile-header-info__detail profile-header-info__handed')
        hand = hand_div.find_next('div',
                                  class_='profile-header-info__detail-stat--small').text.strip() if hand_div else "Not available"

        birthday_div = details_div.find('div', class_='profile-header-info__detail-stat js-profile-header-info__age')
        birthday = birthday_div.find_next('div',
                                       class_='profile-header-info__detail-stat--small').text.strip() if birthday_div else "Not available"

        all_divs = details_div.find_all('div')
        if all_divs:
            country_div = all_divs[-2]
            country = country_div.find_next('div',
                                            class_='profile-header-info__detail-stat--small').text.strip() if country_div else "Not available"
        else:
            country = "Not available"

        print(f"Height: {height}")
        print(f"Hand: {hand}")
        print(f"Date of birth: {birthday}")
        print(f"Country: {country}")
    else:
        print("Could not find the details section on the webpage.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
