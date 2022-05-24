import requests
from bs4 import BeautifulSoup
from random import randint
url_jokes = 'https://www.anekdot.ru/'
page_jokes = requests.get(url_jokes)
def get_jokes():
    bs_jokes = BeautifulSoup(page_jokes.text, 'lxml')
    num = randint(0,45)
    jokes = bs_jokes.find_all('div', class_='text')
    return jokes[num].text
