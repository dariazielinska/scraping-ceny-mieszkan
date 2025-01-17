import pandas as pd
import re

# Przygotowanie danych
df = pd.read_csv("mieszkania_otodom.csv", delimiter=';')

# Czyszczenie kolumny Price
df = df[df['Price'] != 'Zapytaj o cenę']
df = df[~df['Price'].str.contains(r'€|\$', regex=True)]
df['Price'] = df['Price'].replace('zł', '', regex=True).str.replace(' ', '').str.replace(',', '.')
df['Price'] = df['Price'].str.replace(r'\xa0', '', regex=True)
df['Price'] = df['Price'].str.replace(' ', '', regex=True)
df['Price'] = df['Price'].astype(float).round(0).astype(int)

# Czyszczenie kolumny Area
df['Area'] = df['Area'].replace('m²', '', regex=True).astype(float)

# Czyszczenie kolumny Rooms 
df['Rooms'] = df['Rooms'].replace(r'10\+', '11', regex=True)
df['Rooms'] = df['Rooms'].replace(r'pokój|pokoje|pokoi', '', regex=True).astype(float)
df['Rooms'] = df['Rooms'].astype('Int64')

# Czyszczenie kolumny Price per m2
df['Price per m2'] = df['Price per m2'].replace(r'\xa0', '', regex=True)
df['Price per m2'] = df['Price per m2'].replace(' ', '', regex=True)
df['Price per m2'] = df['Price per m2'].replace('zł/m²', '', regex=True).astype(float).round(0).astype(int)

# Czyszczenie kolumny Floor
df = df[~df['Floor'].str.contains(r'poddasze|suterena', regex=True)]
df = df[df['Floor'] != 'Brak danych']
df['Floor'] = df['Floor'].replace(r'10\+', '11', regex=True)
df['Floor'] = df['Floor'].replace('parter', 0)
df['Floor'] = df['Floor'].replace(r'piętro', '', regex=True)
df['Floor'] = df['Floor'].astype(str) 
df['Floor'] = df['Floor'].replace(r'\D', '', regex=True)
df['Floor'] = df['Floor'].astype(int)

def extract_location_data(location):
    words = location.split()
    
    if len(words) >= 2:
        city_or_district = words[-2].replace(',', '')
        province = words[-1] 
    else:
        city_or_district, province = None, None

    return pd.Series([city_or_district, province])

df[['City_or_District', 'Province']] = df['Location'].apply(extract_location_data)

df = df.drop(columns=['Location'])


# Zapisz oczyszczone dane do nowego pliku CSV
df.to_csv('mieszkania_otodom_cleaned.csv', sep=';', index=False)

