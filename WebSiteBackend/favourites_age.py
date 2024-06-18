import requests
from bs4 import BeautifulSoup
import time


# url = "https://www.wtatennis.com/players/314320/simona-halep" + "#overview"


def get_player_details(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        ranking_span = soup.find('span', class_='profile-header-image-col__rank-pos')
        if ranking_span:
            ranking = ranking_span.get("data-single")
        else:
            ranking = "Not available"
        print(f"Ranking: {ranking}")
        details_div = soup.find('div', class_='profile-header-info__details')
        if details_div:
            height_span = details_div.find('div', class_='profile-header-info__detail')
            if height_span:
                height = height_span.find_next('span',
                                               class_='profile-header-info__detail-height')
                if height:
                    height = height.text.strip()
                else:
                    height = "Not available"
            else:
                height = "Not available"

            hand_div = details_div.find('div', class_='profile-header-info__detail profile-header-info__handed')
            if hand_div:
                hand = hand_div.find_next('div',
                                          class_='profile-header-info__detail-stat--small')
                if hand:
                    hand = hand.text.strip()
                else:
                    hand = "Not available"
            else:
                hand = "Not available"

            birthday_div = details_div.find('div',
                                            class_='profile-header-info__detail-stat js-profile-header-info__age')
            if birthday_div:
                birthday = birthday_div.find_next('div',
                                                  class_='profile-header-info__detail-stat--small')
                if birthday:
                    birthday = birthday.text.strip()
                else:
                    birthday = "Not available"
            else:
                birthday = "Not available"
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
            return ranking, height, hand, birthday, country
        else:
            print("Could not find the details section on the webpage.")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
