import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_birth_date(person_name):
    url = f"https://en.wikipedia.org/wiki/{person_name}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        info_table = soup.find('table', {'class': 'infobox'})

        if info_table:
            rows = info_table.find_all('tr')
            for row in rows:
                if 'Born' in row.text:
                    birth_date = row.find('span', {'class': 'bday'})
                    if birth_date:
                        return birth_date.text
            return "Birth date not found."
        else:
            return "Infobox not found."
    else:
        return "Page not found or access denied."


# person_name = "Novak Djokovic"
# birth_date = get_birth_date(person_name)
# print(f"The birth date of {person_name} is: {birth_date}")

def get_birthday(person_name):
    birth_date = get_birth_date(person_name)
    print(f"The birth date of {person_name} is: {birth_date}")


def calculate_age(birth_date, specific_date):
    birth_datetime = datetime.strptime(birth_date, "%Y-%m-%d")
    specific_datetime = datetime.strptime(specific_date, "%Y-%m-%d")
    age = specific_datetime.year - birth_datetime.year
    if (specific_datetime.month, specific_datetime.day) < (birth_datetime.month, birth_datetime.day):
        age -= 1
    return age


if __name__ == "__main__":
    specific_date = "2024-03-24"
    birth_date = "2003-01-29"
    age = calculate_age(birth_date, specific_date)
    print(f"The age of the person on {specific_date} is: {age} years")
