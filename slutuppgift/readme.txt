--Dataflöde mellan systemen--

1. Användaren startar skriptet i detta fall (api_integration.py)
När skriptet körs så startas hela processen.
Systemet hämtar därmed nyhetsdata från externt API (NewsAPI) och bearbetar den data som samlats in och sedan skickar vidare till ett internt api (Lindstorm.nu)

2. Hämtning av data från externa API:t (NewsAPI) ---- funktion "fetch_data()"
En GET-förfrågan skickas till NewsAPI via en API-nyckeln som skickas i headers.
Därav returnerar API:t en JSON lista med nyhetsartikel ifall förfrågan lyckas returneras datan, annars skrivs ett felmeddelande och returnerar None.

3. Transformation av data ---- funktion "transform_data()"
Funktionen bearbetar nyhetsartiklarna och extraherar data som (title, author, description, content, publishedAt, url)
Just för att filtrera datan och skicka vidare de mest nödvändigaste.

4. Skickar data till interna API:t (Lindstorm.nu) ---- funktion "send_data_to_api()"
En POST-förfrågan skickas till det interna API:t via en API-nyckeln som skickas i headers.
Ifall status kod är 201 så har POST-förfrågan gått igenom och sparar datan i databas, om inte förfrågan lyckas visas felmeddelande.

--Systemkarta--
Bifogade png "systemkarta.png" på systemkartan.

--VG POÄNG--
2 VG-poäng: Jag har en Systemkarta + Dataflöde
1 VG-poäng: Jag skickar alla API-nycklar via headern istället för URL:en
1 VG-poäng: Jag har bakat in description och content med title i transform_data() och skickar med det till Interna APIet

"2 VG-poäng: För varje säkerhetsåtgärd som implementeras (av de vi gick igenom under lektion #5)"
Jag har dessa säkerhetsåtgärder som du gick igenom under lektion #5
    2 VG-poäng: API-key via Headern
    2 VG-poäng: Lagrar API-keysen via en .env fil
    2 VG-poäng: Felhantering vid API-anrop (try/expect): requests.exceptions.RequestException och response.raise_for_status()

Som jag tolkade det och räknat så bör jag få:
10 VG-poäng