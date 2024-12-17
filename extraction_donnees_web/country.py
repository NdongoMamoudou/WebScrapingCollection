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
    name = country.find(class_="country-name").text.strip()
    capital = country.find(class_="country-capital").text.strip()
    population = country.find(class_="country-population").text.strip()
    area = country.find(class_="country-area").text.strip()
   


    
    country_data.append([
        name , 
        capital, 
        population, 
        area
       
   ])



 
with  open("countries.csv" , "w" , encoding="utf-8") as file : 
    writer = csv.writer(file)
    writer.writerow(["Name" , "Capital" , "Population" , "Area"])

    for country in country_data : 
        writer.writerow(country)
