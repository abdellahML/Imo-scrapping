from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import json

class ImportFromImmoweb:
    def import_from_url(self, how_many_pages: int):
        """Import data from immoweb"""

        existed = True
        i = 1
        list_of_url: [str] = []
        while(existed):
            """we are using while loop to stop if url doesn't existe because we have to change page to get all data available
            in immoweb. To do that, we have to change page value in the url"""

            url = 'https://www.immoweb.be/fr/recherche/maison/a-vendre?countries=BE&page='+str(i)+'&orderBy=relevance'

            """we have to use Selenium because we can't execute javascript with only BeatifulSoup"""
            driver = webdriver.Chrome()
            driver.implicitly_wait(30)
            driver.get(url)
            
            soup = BeautifulSoup(driver.page_source, 'lxml')

            driver.close()

            """Once we succeded to get page_source in html format then we will return each url of each property in a list"""
            for p in soup.find_all('li',attrs={"class" :"search-results__item"}):
                for a in p.find_all('a', attrs={"class" :"card__title-link"}):
                    #print(a.get('href'))
                    list_of_url.append(a.get('href'))

            i+=1
            """This if is just to stop when we want, because it could last for ever if we have a lot of pages"""
            if i == how_many_pages:
                existed = False
            try:
                url = 'https://www.immoweb.be/fr/recherche/maison/a-vendre?countries=BE&page='+str(i)+'&orderBy=relevance'
                driver = webdriver.Chrome("/usr/local/Caskroom/chromedriver/86.0.4240.22/chromedriver")
                driver.implicitly_wait(30)
                driver.get(url)
            except:
                existed = False
        return list_of_url

    def get_property_info(self, list_of_url):
        """This function is to get information from property for sale from a list of url given"""

        r = requests.get(list_of_url)
        soup = BeautifulSoup(r.content, 'lxml')
        for elem in soup.find_all('div', attrs={"class": "container-main-content"}):
            for a in elem.find_all('script'):
                a = str(a)
                start = a.find( '{' ) + len( '{' )
                end = a.rfind( '}' )
                json_text = '{'+ a[start:end]+ '}'
        property_dict = json.loads(json_text)
        return property_dict
    
    def create_list_from_dict(self, property_dict):
        """Will create a list of property"""

test = ImportFromImmoweb()
#test.import_from_url(2)
test.get_property_info('https://www.immoweb.be/fr/annonce/maison-bel-etage/a-vendre/hamoir-comblain-la-tour/4180/9028348?searchId=5fb51f34611fc')