import requests
from bs4 import BeautifulSoup
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0'}
url = 'https://www.zimmo.be/fr/houthulst-8650/a-vendre/maison/9CPXM/?search=82d1fed181cf30aaa8408f90d99003d3&boosted=1'
page = requests.get(url, headers=headers)
'''print (page.text)'''

soup = BeautifulSoup(page.content, features = 'lxml')

price = soup.find_all('div', attrs={'class' :'col-xsm-8 info-value'})
print(price [0].text.strip())

rooms = soup.find_all('div', attrs={'class' :'col-xs-5 info-value'})
print(rooms [0].text.strip())