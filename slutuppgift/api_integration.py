# api_integration.py - Mall för API-integration

import requests
import os
from dotenv import load_dotenv

# Ladda API-nycklar från .env-fil
load_dotenv()

#[DEL A] Hämta och förbered svarsdata.

# === 1. KONFIGURATION (https://newsapi.org/docs) ===
EXTERNAL_API_URL = "https://newsapi.org/v2/top-headlines"
EXTERNAL_API_KEY = os.getenv("EXTERNAL_API_KEY")# Hämtar API-nyckeln från .env och API Key skickas i headers
HEADERS = {
    "Authorization": f"Bearer {EXTERNAL_API_KEY}"  # [1 VG poäng] API-key skickas i headers
}

# === 2. FUNKTION FÖR ATT HÄMTA DATA FRÅN EXTERNAL API ===
def fetch_data(country="us"):
    params = {"country": country}
    try:
        response = requests.get(EXTERNAL_API_URL, headers=HEADERS, params=params)
        response.raise_for_status()
        print(f"API-anropet till NewsAPI utfärdades! Statuskod: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Fel vid API-anrop för NewsAPI: {e}")
        return None

# === 3. TRANSFORMERA DATA TILL RÄTT FORMAT ===
def transform_data(data):
    #[1 VG poäng] om ni skickar in "description" och "content", och returnera dessa i transformed_data.
    if not data or "articles" not in data: #Felhantering 
        return []

    return_data = []
    for article in data["articles"]:
        return_data.append({ #Hämtade även mer data än nödvändigt för att lära mig filtrera ut data i funktionen send_data_to_api()
            "title": article.get("title"),
            "author": article.get("author"),
            "description": article.get("description"),
            "content": article.get("content"), 
            "publishedAt": article.get("publishedAt"),
            "url": article.get("url")
        })
    return return_data

result = fetch_data()
transformed = transform_data(result)
print(transformed)






#------------DEL B------------

# === 4. FUNKTION FÖR ATT SKICKA DATA TILL INTERNT API ===
# KONFIGURATION (https://lindstorm.nu/register) ===
INTERNAL_API_URL = 'http://lindstorm.nu/api/uppgift/'
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY") #Hämtar API-nyckeln från .env och API Key skickas i headers

def send_data_to_api(transformed_data):
    headers = {
        "X-API-KEY": INTERNAL_API_KEY,
        "Content-Type": "application/json"
    }
        # Skicka transformed_data till API:t via en HTTP-förfrågan

    # Skicka POST-förfrågan till det interna API:t
    for article in transformed_data:  # Skicka varje artikel en och en
        data = {
            "title": article.get("title"),
            "description": article.get("description"),
            "content": article.get("content")
        }

        try:
            response = requests.post(INTERNAL_API_URL, headers=headers, json=data)
            response.raise_for_status()
            print(f"Artikel '{article['title']}' skickades framgångsrikt! Statuskod: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Fel vid skickande av artikel '{article['title']}'. Statuskod: {response.status_code}")
        response = requests.post(INTERNAL_API_URL, headers=headers, json=data)
    
    return response  # Returnera sista svaret

# === 5. KÖR INTEGRATIONEN ===

# Här behöver ni inte ändra något om ni inte vill [VG]
def run():
    # === Hämta data från en extern källa ===
    nyhetsdata = fetch_data()
    if not nyhetsdata:  # Om ingen data hämtas, avbryt funktionen
        print('Fel vid hämtning av data!')
        return
    
    # === Transformera den hämtade datan ===
    transformed_data = transform_data(nyhetsdata)
    if not transformed_data:  # Om transformationen misslyckas, avbryt funktionen
        print('Fel vid transformation av data!')
        return

    # === Skicka den transformerade datan till API:t ===
    sparad_data = send_data_to_api(transformed_data)

    # === Kontrollera om API-svaret är korrekt (statuskod 201 Created) ===
    if not sparad_data or sparad_data.status_code != 201:
        print(f'Fel vid API-anrop! Förväntade 201 men fick {sparad_data.status_code if sparad_data else "Okänd"}')
        return  # Avslutar funktionen om API-anropet misslyckas

    # === Om allt lyckades, bekräfta att processen är klar ===
    print('Data hämtad, transformerad och skickad vidare!')
    print('API Response:', sparad_data.text)  # Skriver ut API-responsens text för debugging

# === 6. EXEKVERA SCRIPTET ===
if __name__ == '__main__':
    run()