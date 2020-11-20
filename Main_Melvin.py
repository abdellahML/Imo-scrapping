from codes.MelvFunctions import ad_urls
from codes.MelvFunctions import data_scrapping
from codes.MelvFunctions import writing_in_csv
from codes.MelvFunctions import managing_data
from codes.MelvFunctions import nbr_of_pages


def melvin():
    url = "https://www.logic-immo.be/fr/vente/immo-a-vendre/circle-50.74770249855428%3A4." \
          "720582357383143_165217.42928163512,{},-------new_price-16776966-,---,---.html"
    nbr = nbr_of_pages(url)
    all_urls = ad_urls(url, 1, nbr)
    list_dict = data_scrapping(all_urls)
    list_dict = managing_data(list_dict)
    writing_in_csv("database.csv", list_dict)
