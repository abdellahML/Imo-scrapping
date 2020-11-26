from bs4 import BeautifulSoup
from threading import Thread
import re
import requests
import csv
from typing import List, Dict


def nbr_of_pages(first_url: str) -> int:
    """
    Calculate the number of pages in a search on the website "logic-immo"
    :param first_url: The url of the first page without its index.
    :return: An int with the number of pages.
    """
    url = first_url.format(1)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    nbr = 0
    for elem in soup.find_all("h1"):
        for number in elem.find_all("span"):
            nbr += int(number.get_text().replace(" ", ""))

    nbr_page = nbr // 16 + 1
    return nbr_page


def ad_urls(first_url: str, start_nbr: int = 1, nbr_page: int = 2) -> List:
    """
    Take all the urls from the ad of a search.
    :param first_url: Url from the first page without the "counter" for the pages.
    :param start_nbr: The index of the beginning page.
    :param nbr_page: The index of the last page. Can be obtained by nbr_of_pages.
    :return: All the urls for the search.
    """
    href = []

    for i in range(start_nbr, nbr_page):
        url = first_url.format(i)
        request = requests.get(url)
        soup_search = BeautifulSoup(request.content, "lxml")
        for div in soup_search.find_all("div", attrs={"class": "property-description"}):
            for elem in div.find_all("a"):
                href += [elem.get("href")]

    links_ad = ["https://www.logic-immo.be/" + elem for elem in href]

    return links_ad


def data_scrapping(links: list) -> List[Dict]:
    """
    Scrape data from every ad in links.
    :param links: A list of urls for all the ads.
    :return: A list with dictionaries with all the data from each ad.
    """
    data_storage = []
    for url_ad in links:
        r = requests.get(url_ad)
        soup = BeautifulSoup(r.content, "lxml")
        keys = ["home_type", "price", "room"]
        values = []

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
                values[i] = 0

        dictionary = dict(zip(keys, values))

        if dictionary.get("Surface jardin") is not None:
            dictionary["garden"] = 1

        data_storage += [dictionary]

    return data_storage


def managing_data(data: List[Dict]) -> List[Dict]:
    """
    Take the data and update it to be able to write it in the csv.
    :param data: A list of dict containing all the data.
    :return: All the data needed.
    """
    for dic in data:
        for i in range(9):
            if "Adresse" in dic.keys():
                dic["locality"] = dic.pop("Adresse")
            elif "Meublé" in dic.keys():
                dic["furnished"] = dic.pop("Meublé")
            elif "Terasse" in dic.keys():
                dic["terrace"] = dic.pop("Terasse")
            elif "Surface jardin" in dic.keys():
                dic["garden_area"] = dic.pop("Surface jardin")
            elif "Surface terrain" in dic.keys():
                dic["surface_of_land_area"] = dic.pop("Surface terrain")
            elif "Piscine" in dic.keys():
                dic["swimming_pool"] = dic.pop("Piscine")
            elif "Etat du bien" in dic.keys():
                dic["state_of_building"] = dic.pop("Etat du bien")

        keys = ["locality", "home_type", "subtype", "price", "type_of_sale", "room", "area", "equipped",
                "furnished", "open_fire", "terrace", "terrace_area", "garden", "garden_area",
                "surface_of_land_area", "facades", "swimming_pool", "state_of_building"]
        keys_list = []
        for i in dic.keys():
            if i in keys:
                pass
            else:
                keys_list += [i]

        for key in keys_list:
            del dic[key]

    return data


def writing_in_csv(file: str, data: List[Dict]):
    """
    Write data in a csv file.
    :param file: Path to the csv file.
    :param data: Data to be written.
    """
    with open(file, mode="a") as database:
        fieldnames = ["locality", "home_type", "subtype", "price", "type_of_sale", "room", "area", "equipped",
                      "furnished", "open_fire", "terrace", "terrace_area", "garden", "garden_area",
                      "surface_of_land_area", "facades", "swimming_pool", "state_of_building"]
        data_writer = csv.DictWriter(database, fieldnames=fieldnames)

        data_writer.writeheader()
        for i in data:
            data_writer.writerow(i)


"""
class ScrappingDataThread(Thread):
    def __init__(self, list_url: list):
        Thread.__init__(self)
        self.list_url = list_url

    def run(self):
        return_list = data_scrapping(self.list_url)
        return return_list


class RecoverUrlThread(Thread):
    def __init__(self, incomplete_url: str, minimum: int, maximum: int):
        Thread.__init__(self)
        self.incomplete_url = incomplete_url
        self.min = minimum
        self.max = maximum

    def run(self):
        print("start")
        return_list = ad_urls(self.incomplete_url, self.min, self.max)
        print("end")
        return return_list
"""
