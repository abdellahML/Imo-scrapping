# [Logic-Immo.be](https://www.logic-immo.be/fr/immobilier-belgique.html?gclid=Cj0KCQiAk53-BRD0ARIsAJuNhpsAy7SooC8fFCrIzBoWB8rTnytq8mCw4RPmCzgT7bTSRLlhtNPzI10aAmSFEALw_wcB) and [Immoweb.be](https://www.immoweb.be/fr?gclid=Cj0KCQiAk53-BRD0ARIsAJuNhpsyGuPvCroSEdTkJ32649Ag38X-v5XiioMPEVlNEo-85hcKr1T8JmwaAh_4EALw_wcB) data scraping

## About

First project of BeCode formation.
The goal is to collect data from different houses and flats ads.

## Search criteria

There is the different data extracted :
- Locality
- Type of property (House/apartment)
- Subtype of property (Bungalow, Chalet, Mansion, ...)
- Price
- Type of sale (Exclusion of life sales)
- Number of rooms
- Fully equipped kitchen (Yes/No)
- Furnished (Yes/No)
- Open fire (Yes/No)
- Terrace (Yes/No)
    If yes: Area
- Garden (Yes/No)
    If yes: Area
- Livable surface area
- Surface area of the plot of land
- Number of facades
- Swimming pool (Yes/No)
- State of the building (New, to be renovated, ...)

## File

database.csv (sep=",") is the result of this scraping.

This file is already filled with more than 10.000 data properties.

Abdellah_results.csv (sep=",") is another result for the scraping of logic-immo.

This file is already filled with more than 5.000 data properties.

## Why

A little exercise to consolidate our knowledges.

## When

It took us three days, from the 18th November 2020 to the 20th November 2020.

## Usage

You need to have **Python3**.
Different packages used :
- Beautifulsoup4
- Selenium
- re
- threading

For "www.immoweb.be" use the ebu function:
```python
from MainEbu import ebu

ebu()
```

For "www.logic-immo.be" use the melvin function:
```python
from Main_Melvin import melvin

melvin()
```

For "www.logic-immo.be" use Abdellah.py.

Just run the code.


**These functions will return 5.000 data each.**

## Team member

Abdellah El Ghilbzouri, Junior AI developer,

Andreas Margraff, Junior AI developer,

Ebubekir Kocadag, Junior AI developer,

Melvin Leroy, Junior AI developer.

## Things to do

- The program for "www.logic-immo.be" could use threads to be faster;
- For the program "www.immoweb.be" threading could be more effecient.
