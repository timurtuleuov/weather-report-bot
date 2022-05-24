import requests
from bs4 import BeautifulSoup

url = 'http://www.finmarket.ru/currency/rates/?id=10123'
page_of_dollars_and_euros = requests.get(url)
bs_dol_euro = BeautifulSoup(page_of_dollars_and_euros.text, 'lxml')
currency = bs_dol_euro.find_all('div', class_='value')

def get_dollar():
    dollar = currency[0].text[:6]
    return dollar

def get_euro():
    euro = currency[1].text[:6]
    return euro

url_of_rubles = 'https://mybuh.kz/nbrk/'
page_of_rubles = requests.get(url_of_rubles)
bs_rub = BeautifulSoup(page_of_rubles.text, 'lxml')

def get_ruble():
    ruble = bs_rub.find_all('td', class_='k')
    result = ruble[2].text.replace(' ', '')
    return result[1:5].replace('.', ',')
