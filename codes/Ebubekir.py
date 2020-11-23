from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import json

from threading import Thread
import copy

class ImportFromImmoweb:
    def import_from_url(self,from_pages: int, how_many_pages: int) -> list:
        """Import data from immoweb"""

        existed: bool = True
        i: int = from_pages
        list_of_url: [str] = []
        while(existed):
            """we are using while loop to stop if url doesn't existe because we have to change page to get all data available
            in immoweb. To do that, we have to change page value in the url"""

            try:
                url = 'https://www.immoweb.be/fr/recherche/maison/a-vendre?countries=BE&page='+str(i)+'&orderBy=relevance'

                """we have to use Selenium because we can't execute javascript with only BeatifulSoup"""
                
                r = requests.get(url)
                
                """We are looking if the url exist or not, if yes then we execute with selenium, if not we stop th while loop"""
                if r.status_code == 200:

                    driver = webdriver.Chrome()
                    driver.implicitly_wait(30)
                    driver.get(url)
                else:
                    existed = False
                    continue
                
            except:
                existed = False
                continue

            soup = BeautifulSoup(driver.page_source, 'lxml')

            """Once we succeded to get page_source in html format then we will return each url of each property in a list"""
            for p in soup.find_all('li',attrs={"class" :"search-results__item"}):
                for a in p.find_all('a', attrs={"class" :"card__title-link"}):
                    list_of_url.append(a.get('href'))

            i+=1
            """This if is just to stop when we want, because it could last for ever if we have a lot of pages"""
            if i == how_many_pages:
                existed = False
            driver.close()
        return list_of_url

    def get_property_info(self, list_of_url: list) -> list:
        """This function is going to get information from property for sale from a list of url given"""

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
    
    def create_list_from_dict(self, property_list: list) -> list:
        """Will create a list of property"""
        home_list: [dict] = []

        for property_dict in property_list:
            locality = property_dict["property"]["location"]["district"]
            home_type = property_dict["property"]["type"]
            subtype = property_dict["property"]["subtype"]
            price = property_dict["transaction"]["sale"]["price"]
            sale_type = property_dict["flags"]      
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
            if surface_tot != None and area != None:
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

            """We are changing bool to int"""
            equiped = self.change_bool_to_int(equiped)
            furnished = self.change_bool_to_int(furnished)
            open_fire = self.change_bool_to_int(open_fire)
            terrace = self.change_bool_to_int(terrace)
            garden = self.change_bool_to_int(garden)
            swiming_pool = self.change_bool_to_int(swiming_pool)

            home = {"locality": locality, "home_type": home_type, "subtype": subtype,"price": price,
                    "type_of_sale": type_of_sale, "room": room,"area": area,"equipped": equiped,
                    "furnished": furnished, "open_fire": open_fire, "terrace": terrace, "terrace_area": terrace_area,
                    "garden": garden, "garden_area": garden_area, "surface_of_land_area": surface_of_land_area,
                    "facades": facades, "swimming_pool": swiming_pool, "state_of_building": state_of_building}
            home_list.append(home)
        return home_list

    def which_sale_type(self, sale_type: list) -> str:
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
    
    def check_if_existed(self, path, check = None) -> bool:
        """Check if 'path' existe and if it's value is equal to check, return True or False"""

        if path != check:
            value_to_return = True
        else:
            value_to_return = False
        return value_to_return
    
    def change_bool_to_int(self, value: bool) -> int:
        """We are changing bool to int"""
        if value == True:
            value = 1
        elif value == False:
            value = 0
        else:
            value = None
        return value

class MyThread(Thread):
    def __init__(self, to: int, until: int):
        Thread.__init__(self)
        self.to = to
        self.until = until
    def run(self) -> list:
        test = ImportFromImmoweb()
        urls = test.import_from_url(self.to, self.until)
        dictio = test.get_property_info(urls)
        home_list = test.create_list_from_dict(dictio)
        return home_list