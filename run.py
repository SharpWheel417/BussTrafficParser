from bs4 import BeautifulSoup
import requests



page = requests.get('https://bustraffic.ru/findtrips/searchtrips/2853EE34A/1738/1786')

soup = BeautifulSoup(page.text, 'html.parser')

table = soup.find_all('div', class_='tabs__content active')

print(table[0].contents[3].contents[7].contents[13].contents[0])
