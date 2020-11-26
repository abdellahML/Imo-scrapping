from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import re
import csv
import pandas as pd


houses=[]
#get the first main page
url='https://www.logic-immo.be/fr/vente/immo-a-vendre/circle-50.772740029958776:4.502423535156264_160085.90246203897,1,-------new_price-16776960-,---,---.html'
r = requests.get(url)
print(url, r.status_code)
soup = BeautifulSoup(r.content,'lxml')

#get the url of all main pages
all_url=[]
for nber in range(1,3):
    all_url.append(('https://www.logic-immo.be/fr/vente/immo-a-vendre/circle-50.772740029958776:4.502423535156264_160085.90246203897,' +str(nber) +',-------new_price-16776960-,---,---.html'))
#print(all_url)

#iteration to get informations from a few main pages
for elem in all_url:
    
    r = requests.get(elem)
    print(elem, r.status_code)
    soup = BeautifulSoup(r.content,'lxml')

    #get the link of the page of the specific proprety
    links=[]
    for elem in soup.find_all('div', attrs= {"class" :"property-description"}):
        
        for item in elem.find_all ('a'):
        
            links.append(item.get('href'))

    links_goods=[ 'https://www.logic-immo.be' + elem for elem in links if 'vente' in elem]
    #iteration to get all links of specific properties in the main page
    for elem in links_goods:

        # to get all informations of the propertise in a single main page
        #get the adress of the first propr. 
        url0= elem
        r0 = requests.get(elem)
        print(elem, r0.status_code)
        soup = BeautifulSoup(r0.content,'lxml')

        property_dict={}

        #get the locality (complete adress)
        adress= "Ask to get the adress"
        for elem in soup.find_all('div', attrs= {"class" :"c-details_content__block map"}):
            for item in elem.find_all('p'):
                if ('info' not in item.text and "demand" not in item.text ):
                    adress= item.get_text().replace(" ",'').replace('\n','').replace('Adresse:','')
        property_dict['adress']= adress
        #print(adress)
        #print(property_dict)

        #get the price
        for elem in soup.find_all('h1', attrs= {"class" :"c-details_title c-details_title--primary"}):
            for item in elem.find_all('span'):
                price= item.text.replace("\xa0",'').replace(" ",'')
        property_dict['price']= price
        #print (price)
        #print(property_dict)

        #get type of property of the first prop.

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
        property_dict['property type']= type_prop

        #print (type_prop)
        #print(property_dict)

        #get type of sale
        type_of_sale= 'normal sale'
        property_dict['type of sale']= type_of_sale
        #print(property_dict)

        #get nbre of rooms

        for elem in soup.find_all('li', attrs= {"class" :"c-details_img text-center nb_bedrooms"}):
            for item in elem.find_all('p'):
                rooms = [int(s) for s in item.text.split() if s.isdigit()]

        property_dict[' number of rooms']= rooms[0]
        #print(property_dict)


        #garden
        garden='No'
        for elem in soup.find_all('li', attrs= {"class" :"c-details_img text-center garden_area"}):
            for item in elem.find_all('p'):
                area= item.text.split()
                garden= "Yes/" + ' '+area[0] + area[1]
        property_dict[' garden']= garden
        #print(property_dict)
        #print(garden)

        #get area of plot land
        plot_land='No information'
        for elem in soup.find_all('li', attrs= {"class" :"c-details_img text-center plot_area"}):
            for item in elem.find_all('p'):
                land=item.text.split()
                plot_land= land[0]+' ' + land[1]
        property_dict[' surface area of the plot of land']= plot_land
        #print(property_dict)
        #print('land ' +plot_land)

        #get area(living), furnished,terrace, kitchen,
        # swimmingpool, states of the property, open fire
        area=''
        furnished='No'
        terrace='No'
        kitchen='No'
        swimmingpool='No'
        states="old property"
        fire='No informations'
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
        property_dict[' living area']= area
        property_dict[' furnished']= furnished
        property_dict[' terrace']= terrace
        property_dict[' fully equiped kitchen']= kitchen
        property_dict[' swimmingpool']= swimmingpool
        property_dict[' states of building']= states
        property_dict[' open fire']= fire

        #print(property_dict)                    
        #print(furnished)
        #print(terrace) 
        #print(kitchen) 
        #print(swimmingpool)      
        #print(states)
        houses.append(property_dict)
    #print(property_dict)
title=['adress', 'price','property type', 'type of sale', ' number of rooms', ' garden', ' surface area of the plot of land', ' living area', ' furnished', ' terrace', ' fully equiped kitchen', ' swimmingpool', ' states of building', ' open fire'
]
with open('Abdellah_results.csv', mode='a') as csv_file:
    fieldnames = title
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for item in houses:
        writer.writerow(item)

