from bs4 import BeautifulSoup
import requests
import re


import Dataclass


data_storage_list = []
for i in range(1,5):
    url = "https://www.logic-immo.be/fr/vente/immo-a-vendre/circle-50.74770249855428%3A4." \
      "720582357383143_165217.42928163512,{},-------new_price-16776966-,---,---.html".format(i)

    r = requests.get(url)
    print(url, r.status_code)
    soup = BeautifulSoup(r.content, "lxml")
    links = []
    for div in soup.find_all("div", attrs={"class": "property-description"}):
        for elem in div.find_all("a"):
            links += [elem.get("href")]

    links_ad = ["https://www.logic-immo.be/" + elem for elem in links]

    for url_ad in links_ad:
        r = requests.get(url_ad)
        print(url_ad, r.status_code)
        soup = BeautifulSoup(r.content, "lxml")
        keys = ["home_type", "number_room", "price"]
        values = []

        data_storage = Dataclass.Home()

        for title in soup.find_all("h1"):
            new_text_string = title.get_text()
            splitted = re.findall("[\w\-]+", new_text_string)
            values = values + [splitted[0]] + [splitted[-2] + splitted[-1]]
            if "chambre" in splitted:
                index = splitted.index("chambre")
                values += [splitted[index - 1]]
            else:
                values += [None]

        for menu in soup.find_all("ul", attrs={"class": "c-details_dropdown__container dropdown-menu"}):
            for text in menu.find_all("li"):
                new_text_string = text.get_text()
                splitted = new_text_string.split(":")
                keys += [splitted[0]]
                values += [splitted[1]]

        for i, value in enumerate(values):
            if value == " ":
                values[i] = None

        dictio = dict(zip(keys, values))

        if dictio.get("Surface jardin") is not None:
            dictio["jardin"] = 1

        data_storage.locality = dictio.get("Adresse")
        data_storage.home_type = dictio.get("home_type")
        data_storage.subtype = dictio.get("")
        data_storage.price = dictio.get("price")
        data_storage.type_of_sale = dictio.get("")
        data_storage.room = dictio.get("number_room")
        data_storage.area = dictio.get("")
        data_storage.equipped = dictio.get("")
        data_storage.furnished = dictio.get("Meublé")
        data_storage.open_fire = dictio.get("")
        data_storage.terrace = dictio.get("Terrasse")
        data_storage.terrace_area = dictio.get("")
        data_storage.garden = dictio.get("jardin")
        data_storage.garden_area = dictio.get("Surface jardin")
        data_storage.surface_of_land_area = dictio.get("Surface terrain")
        data_storage.facades = dictio.get("")
        data_storage.swimming_pool = dictio.get("Piscine")
        data_storage.state_of_building = dictio.get("Etat du bien")

        data_storage_list += [data_storage]

print(data_storage_list)
