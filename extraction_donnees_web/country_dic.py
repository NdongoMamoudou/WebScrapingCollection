import requests
from bs4 import BeautifulSoup
import csv

# Envoyer une requête GET à la page web
response = requests.get("https://www.scrapethissite.com/pages/simple/")

# Parser le contenu HTML de la réponse avec BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

country_data = []

# Boucle pour trouver et imprimer les pays
for country in soup.select(".country"):
    name_country = country.find(class_="country-name").text.strip()
    capital_country = country.find(class_="country-capital").text.strip()
    population_country = country.find(class_="country-population").text.strip()
    area_country = country.find(class_="country-area").text.strip()
   


    
    country_data.append({
        "name" : name_country , 
        "capital" : capital_country , 
        "population" : population_country, 
        "area" : area_country 
       
   })



 
with  open("countries_dic.csv" , "w" , encoding="utf-8") as file : 
    writer = csv.DictWriter(file , fieldnames=["name" , "capital" , "population" , "area"])
    writer.writeheader()
    for country in country_data : 
        writer.writerow(country)



