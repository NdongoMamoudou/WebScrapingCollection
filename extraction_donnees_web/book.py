import requests
from bs4 import BeautifulSoup
import re
import csv

# Dictionnaire pour mapper les scores des livres
star_mapping = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

book_data = [] 

def get_total_pages(url):
    # Envoyer une requête à la page d'accueil

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Trouver la pagination
    pagination = soup.find("ul", class_="pager")
    last_page = 1  

    # Extraire le dernier numéro de page
    if pagination:
        pages = pagination.find_all("li", class_="current")
        if pages:
            last_page_text = pages[-1].text.strip()
            if 'of' in last_page_text:  
                last_page = int(last_page_text.split()[-1])
            else:
                last_page = int(last_page_text)
    return last_page



def books(url):
    # Envoyer une requête à la page d'accueil
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Parcourir pour trouver les livres sur la page
    for product in soup.select(".product_pod"):
        titre = product.find("h3").find("a")["title"]
        star_class = product.find("p", class_="star-rating")["class"][1]
        score = star_mapping.get(star_class, "Non spécifié")
        prix = product.find(class_="price_color").text.strip()

        # URL complet du livre
        book_url = "https://books.toscrape.com" + "/catalogue" + product.find("h3").find("a")["href"][9:]

        # Accéder au détail du livre
        book_response = requests.get(book_url)
        book_soup = BeautifulSoup(book_response.text, "html.parser")

        # Récupérer la description depuis la balise meta
        description_meta = book_soup.find("meta", {"name": "description"})
        description = description_meta["content"].strip() if description_meta else "Description non disponible"

        # Récupérer les informations sur le stock
        stock_info = book_soup.find("p", class_="instock availability")
        stock_text = stock_info.get_text(strip=True) if stock_info else "Stock non disponible"

        # Nombre de livre  disponibles
        stock_match = re.search(r'\((\d+)\s+available\)', stock_text)
        stock = int(stock_match.group(1)) if stock_match else 0

        # Ajouter les informations du livre à la liste
        book_data.append({
            "titre": titre,
            "score": score,
            "prix": prix,
            "stock": stock,
            "description": description
        })

print()






def save_to_csv():
    # Ouvrir le fichier CSV et écrire les données
    with open("book.csv", "w", encoding="utf-8", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["titre", "score", "prix", "stock", "description"])
        writer.writeheader()
        for book in book_data:
            writer.writerow(book)

def scrape_all_books(base_url):
    # Récupérer le nombre total de pages
    total_pages = get_total_pages(base_url)
    print(f"Nombre total de pages à scraper : {total_pages}")
    
    # Boucler sur toutes les pages et scrapper chaque page
    for page_number in range(1, total_pages + 1):
        page_url = f"{base_url}/catalogue/page-{page_number}.html"
        print(f"Scraping la page {page_number} sur {total_pages}: {page_url}")
        books(page_url)

# Exemple d'appel à la fonction pour commencer le scraping
scrape_all_books("https://books.toscrape.com")

# Sauvegarder les données dans le fichier CSV
save_to_csv()
