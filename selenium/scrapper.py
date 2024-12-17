from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

# URL du site
url = "https://ecole-ipssi.com/?utm_source=adwords&utm_medium=cpc&utm_campaign=Search_Marque_IPSSI&utm_content=&utm_term=ipssi&gad_source=1&gclid=CjwKCAiA34S7BhAtEiwACZzv4VnfqRPX3HHGaZnV-Eg3VxNeINDswlaH6ifX3-7HVFHIygOn23AKOxoCntkQAvD_BwE"


driver = webdriver.Chrome()

# Accéder à la page
driver.get(url)

# attendre pour charger
time.sleep(5)

# recuperer le contenue de la page 
html = driver.page_source

# Fermer le navigateur
driver.close()

# Analyser la page avec BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Extraire toutes les villes
villes = []

#  voir toute divs contenant la classe  => places-fig
place_elements = soup.find_all('div', class_='places-fig')

# Parcourir chaque élément trouvé
for place in place_elements:
    ville = place.find('span')
    if ville:
        villes.append(ville.get_text(strip=True))

print("Les villes récupérées :")
for ville in villes:
    print(ville)
