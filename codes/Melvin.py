from bs4 import BeautifulSoup
import requests

url = "https://www.logic-immo.be/fr/vente/immo-a-vendre/circle-50.74770249855428%3A4." \
      "720582357383143_165217.42928163512,1,-------new_price-16776966-,---,---.html"

r = requests.get(url)
print(url, r.status_code)
soup = BeautifulSoup(r.content, "lxml")
links = []
for div in soup.find_all("div", attrs={"class" :"property-description"}):
      for elem in div.find_all("a"):
            links += [elem.get("href")]

links_ad = ["https://www.logic-immo.be/"+ elem for elem in links]
print(links_ad)
print(len(links_ad))