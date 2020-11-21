from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import re




#get the first main page
url='https://www.logic-immo.be/fr/vente/immo-a-vendre/circle-50.772740029958776:4.502423535156264_160085.90246203897,1,-------new_price-16776960-,---,---.html'
r = requests.get(url)
print(url, r.status_code)
soup = BeautifulSoup(r.content,'lxml')

#get the number of pages based on nbre of properties
properties=''
pages=0
for elem in soup.find_all('div', attrs= {"class" :"result-header"}): 
    for item in elem.find_all ('span'):
        properties = int(item.get_text().replace(" ", ""))
        
        pages= properties//16
print(properties)
print(pages)

#get the price
for elem in soup.find_all('div', attrs= {"class" :"col-xs-6 col-sm-6 col-md-6 col-lg-6"}): 
    for item in elem.find_all ('p'):
        price = item.text
print (price)
       

#get the link of the page of the specific proprety
links=[]
for elem in soup.find_all('div', attrs= {"class" :"property-description"}):
    
    for item in elem.find_all ('a'):
       
        links.append(item.get('href'))

links_goods=[ 'https://www.logic-immo.be' + elem for elem in links if 'vente' in elem]

#get the adress of the first propr. 
url0= links_goods[0]
r0 = requests.get(url0)
print(url0, r0.status_code)
soup = BeautifulSoup(r0.content,'lxml')

adress=""
for elem in soup.find_all('div', attrs= {"class" :"c-details_content__block map"}):
    for item in elem.find_all('p'):
        adress= item.text
print(adress)

#get type of property of the first prop.

type_prop= ""
for elem in soup.find('h1', attrs= {"class" :"c-details_title c-details_title--primary"}):
    if "Maison" in elem:
        type_prop ='Maison'
    elif 'Studio' in elem:
        type_prop = 'Studio'
    elif 'Appartement' in elem:
        type_prop = 'Appartement'
    elif 'Immeuble' in elem:
        type_prop= 'Immeuble'
    else:
        type_prop ='Maison'

print (type_prop)

#get type of sale
type_of_sale= 'normal sale'

#get nbre of rooms
rooms=''
for elem in soup.find_all('li', attrs= {"class" :"c-details_img text-center nb_bedrooms"}):
    for item in elem.find_all('p'):
        rooms= item.text



#garden
garden='No'
for elem in soup.find_all('li', attrs= {"class" :"c-details_img text-center garden_area"}):
    for item in elem.find_all('p'):
        garden= "Yes/" + item.text
print(garden)

#get area of plot land
plot_land='No information'
for elem in soup.find_all('li', attrs= {"class" :"c-details_img text-center plot_area"}):
    for item in elem.find_all('p'):
        plot_land= item.text
print('land' +plot_land)

#get area(living), furnished,terrace, kitchen,
# swimmingpool, states of the property
area=''
furnished='No'
terrace='No'
kitchen='No'
swimmingpool='No'
states="old property"
for elem in soup.find_all('div', attrs= {"class" :"col-sm-6"}):
    for item in elem.find_all('li'):
        for span in item.find_all('span'):
            if 'Surface habitable' in item.text:
                area = span.text
            if 'Meublé' in item.text:
                for span2 in span.find_all('span', attrs ={'class':'glyphicon glyphicon-remove'}):
                    furnished='No'
                for span2 in span.find_all('span', attrs ={'class':'glyphicon glyphicon-ok'}):
                    furnished= 'Yes'
            if 'Terrasse' in item.text:
                for span2 in span.find_all('span', attrs ={'class':'glyphicon glyphicon-remove'}):
                    terrace='No'
                for span2 in span.find_all('span', attrs ={'class':'glyphicon glyphicon-ok'}):
                    terrace= 'Yes'
            if 'Cuisine' in item.text:
                for span2 in span.find_all('span', attrs ={'class':'glyphicon glyphicon-remove'}):
                    kitchen='No'
                for span2 in span.find_all('span', attrs ={'class':'glyphicon glyphicon-ok'}):
                    kitchen= 'Yes'  
            if 'Etat du bien' in item.text:
                if 'Bien neuf' in span.text:
                    states='New'
                      
print(furnished)
print(terrace) 
print(kitchen) 
print(swimmingpool)      
print(states)
        
    















