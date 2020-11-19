from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import json

from Dataclass import Home

from threading import Thread
import copy

class ImportFromImmoweb:
    def import_from_url(self,from_pages, how_many_pages: int):
        """Import data from immoweb"""

        existed = True
        i = from_pages
        list_of_url: [str] = []
        while(existed):
            """we are using while loop to stop if url doesn't existe because we have to change page to get all data available
            in immoweb. To do that, we have to change page value in the url"""

            try:
                url = 'https://www.immoweb.be/fr/recherche/maison/a-vendre?countries=BE&page='+str(i)+'&orderBy=relevance'

                """we have to use Selenium because we can't execute javascript with only BeatifulSoup"""

                driver = webdriver.Chrome()
                driver.implicitly_wait(30)
                driver.get(url)
            except:
                existed = False
                continue
            soup = BeautifulSoup(driver.page_source, 'lxml')

            """Once we succeded to get page_source in html format then we will return each url of each property in a list"""
            for p in soup.find_all('li',attrs={"class" :"search-results__item"}):
                for a in p.find_all('a', attrs={"class" :"card__title-link"}):
                    #print(a.get('href'))
                    list_of_url.append(a.get('href'))

            i+=1
            """This if is just to stop when we want, because it could last for ever if we have a lot of pages"""
            if i == how_many_pages:
                existed = False
            driver.close()
        return list_of_url

    def get_property_info(self, list_of_url):
        """This function is to get information from property for sale from a list of url given"""

        property_list: list = []

        for url in list_of_url:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'lxml')
            for elem in soup.find_all('div', attrs={"class": "container-main-content"}):
                for a in elem.find_all('script'):
                    a = str(a)
                    start = a.find( '{' ) + len( '{' )
                    end = a.rfind( '}' )
                    json_text = '{'+ a[start:end]+ '}'
            property_dict = json.loads(json_text)
            property_list.append(property_dict)

        return property_list
    
    def create_list_from_dict(self, property_list):
        """Will create a list of property"""
        home_list: [Home] = []

        for property_dict in property_list:
            locality = property_dict["property"]["location"]["district"]
            home_type = property_dict["property"]["type"]
            subtype = property_dict["property"]["subtype"]
            price = property_dict["transaction"]["sale"]["price"]
            sale_type = property_dict["flags"]      #maybe there is a short-cut but for now
            type_of_sale = self.which_sale_type(sale_type)
            room = property_dict["property"]["bedroomCount"]
            area = property_dict["property"]["netHabitableSurface"]
            if property_dict["property"]["kitchen"] != None:
                isEquiped = property_dict["property"]["kitchen"]["type"]
            else:
                isEquiped = None
            equiped = self.check_if_existed(isEquiped,"NOT_INSTALLED")
            isFurnished = property_dict["transaction"]["sale"]["isFurnished"]
            furnished = self.check_if_existed(isFurnished, False)
            fire = property_dict["property"]["fireplaceExists"]
            open_fire = self.check_if_existed(fire, False)
            terrace = property_dict["property"]["hasTerrace"]
            if terrace:
                terrace_area = property_dict["property"]["terraceSurface"]
            else:
                terrace_area = None
            
            garden = property_dict["property"]["hasGarden"]
            if garden:
                garden_area = property_dict["property"]["gardenSurface"]
            else:
                garden_area = None
            
            if property_dict["property"]["land"] != None:
                surface_tot = property_dict["property"]["land"]["surface"]
            else:
                surface_tot = None
            if surface_tot != None:
                surface_of_land_area = area + surface_tot
            else:
                surface_of_land_area = area
            if property_dict["property"]["building"] != None:
                facades = property_dict["property"]["building"]["facadeCount"]
                state_of_building = property_dict["property"]["building"]["condition"]
            else:
                facades = None
                state_of_building = None
            swiming_pool = property_dict["property"]["hasSwimmingPool"]

            home = Home(locality, home_type, subtype, price, type_of_sale, room, area, equiped,
                        furnished, open_fire, terrace, terrace_area, garden, garden_area,
                        surface_of_land_area, facades, swiming_pool, state_of_building)
            home_list.append(home)
        return home_list

    def which_sale_type(self, sale_type):
        """I've choosed to do a function to do this because i can add something after"""
        
        if sale_type["isPublicSale"]:
            type_of_sale = "Public sale"
        elif sale_type["isNotarySale"]:
            type_of_sale = "Notary sale"
        elif sale_type["isLifeAnnuitySale"]:
            type_of_sale = "Life sale"
        elif sale_type["isNewRealEstateProject"]:
            type_of_sale = "New project"
        elif sale_type["isAnInteractiveSale"]:
            type_of_sale = "Interactive sale"
        else:
            type_of_sale = None
        return type_of_sale
    
    def check_if_existed(self, path, check = None):

        if path != check:
            value_to_return = True
        else:
            value_to_return = False
        return value_to_return

class MyThread(Thread):
    def __init__(self, to, until):
        Thread.__init__(self)
        self.to = to
        self.until = until
    def run(self):
        test = ImportFromImmoweb()
        urls = test.import_from_url(self.to, self.until)
        dictio = test.get_property_info(urls)
        home_list = test.create_list_from_dict(dictio)
        return home_list

final_list = []

thread = MyThread(1,2)
thread_2 = MyThread(3,4)
thread_3 = MyThread(5,6)
thread_4 = MyThread(7,8)
thread_5 = MyThread(9,10)
thread_6 = MyThread(11,12)
thread_7 = MyThread(13,14)
thread_8 = MyThread(15,16)
thread_9 = MyThread(17,18)
thread_10 = MyThread(19,20)
thread.start()
thread_2.start()
thread_3.start()
thread_4.start()
thread_5.start()
thread_6.start()
thread_7.start()
thread_8.start()
thread_9.start()
thread_10.start()
home_list = thread.run()
home_list_2 = thread_2.run()
home_list_3 = thread_3.run()
home_list_4 = thread_4.run()
home_list_5 = thread_5.run()
home_list_6 = thread_6.run()
home_list_7 = thread_7.run()
home_list_8 = thread_8.run()
home_list_9 = thread_9.run()
home_list_10 = thread_10.run()
final_list.extend(home_list)
final_list.extend(home_list_2)
final_list.extend(home_list_3)
final_list.extend(home_list_4)
final_list.extend(home_list_5)
final_list.extend(home_list_6)
final_list.extend(home_list_7)
final_list.extend(home_list_8)
final_list.extend(home_list_9)
final_list.extend(home_list_10)

print('done')