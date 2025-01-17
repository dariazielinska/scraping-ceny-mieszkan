import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Nagłówki, które imitują przeglądarkę
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Funkcja do scrapowania jednej strony
def scrape_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Błąd podczas ładowania strony {url}: {response.status_code}")
        return []

    # Parsowanie HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []

    # Przeszukiwanie strony, szukamy interesujących elementów
    for offer in soup.find_all('article', attrs={'data-cy': 'listing-item'}):
        title_tag = offer.find('p', attrs={'data-cy': 'listing-item-title'})
        title = title_tag.get_text(strip=True) if title_tag else 'Brak tytułu'

        location_tag = offer.find('p', class_='css-42r2ms eejmx80')
        location = location_tag.get_text(strip=True) if location_tag else 'Brak lokalizacji'

        price = offer.find('span', class_='css-2bt9f1 evk7nst0').get_text(strip=True)

        dl_tag = offer.find('dl', class_='css-12dsp7a e1clni9t1')
        if dl_tag:
            dd_tags = dl_tag.find_all('dd') 
            rooms = dd_tags[0].get_text(strip=True) if len(dd_tags) > 0 else 'Brak danych'
            area = dd_tags[1].get_text(strip=True) if len(dd_tags) > 1 else 'Brak danych'
            price_per_sqm = dd_tags[2].get_text(strip=True) if len(dd_tags) > 2 else 'Brak danych'
            floor = dd_tags[3].get_text(strip=True) if len(dd_tags) > 3 else 'Brak danych'
        else:
            rooms = 'Brak danych'
            area = 'Brak danych'
            price_per_sqm = 'Brak danych'
            floor = 'Brak danych'

        # Dodanie wyniku do listy
        data.append([title, location, price, area, rooms, price_per_sqm, floor])

    return data

# Zapisywanie do CSV
def save_to_csv(data, filename):
    # Jeśli plik istnieje, dane są dodawane; jeśli nie, tworzymy nowy plik
    df = pd.DataFrame(data, columns=['Title', 'Location', 'Price', 'Area', 'Rooms', 'Price per m2', 'Floor'])
    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        df.to_csv(f, sep=';', index=False, header=f.tell() == 0)  # Dodanie nagłówków tylko jeśli plik jest pusty

# Scrapowanie wielu stron
base_url = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/cala-polska?page="
output_file = "mieszkania_otodom.csv"

for page in range(1000, 1300):
    url = base_url + str(page)
    print(f"Scrapuję stronę: {url}")
    page_data = scrape_page(url)
    if not page_data:
        print(f"Brak danych na stronie: {url}, przerywam.")
        break
    save_to_csv(page_data, output_file)
    time.sleep(3)

print(f"Scraping zakończony. Dane zapisane do {output_file}.")
