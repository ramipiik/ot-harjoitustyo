# Arkkitehtuurikuvaus

## Rakenne
Sovellus on toteutettu kolmikerrosmallin mukaan, jossa tiedon tallennukseen, palvelulogiikkaan sekä käyttöliittymään liittyvät toiminnallisuudet ovat omilla kerroksillaan ao. kaavion mukaisesti.

* Repositories: Tiedon tallennukseen liittyvä koodi
* Services: Sovelluslogiikka. 
* UI: Tekstikäyttöliittymä ja graafinen käyttöliittymä
* Entities: Olio-ohjelmoinnin luokat

Testit ovat omassa erillisessä kansiossaan tests.  
  
![Pakkauskaavio](https://github.com/ramipiik/ot-harjoitustyo/blob/main/dokumentaatio/pakkauskaavio/pakkauskaavio.jpg)
  
## Käyttöliittymä

### Tekstikäyttöliittymä
Tiedostosta text_ui.py löytyvä tekstikäyttöliittymä on tällä hetkellä ohjelman pääkäyttöliittymä. Se jakautuu seuraaviin päänäkymiin/funktioihin:
* start_UI: Käyttäjän ensimmäinen näkymä. Käyttäjän valittavana olevat vaihtoehdot: Kirjaudu, luo uusi käyttäjä, lopeta
* login_UI: Näkymä sisäänkirjautumista varten. Pyytää käyttäjältä käyttäjänimen ja salasanan. Kutsuu tämän jälkeen palvelukerroksen login-palvelua.
* signup_UI: Näkymä uuden käyttäjän luomista varten. Pyytää käyttäjältä käyttäjänimen ja salasanan. Kutsuu tämän jälkeen palvelukerroksen signup-palvelua.
* create_porfolio_UI: Näkymä uuden sijoitussalkun luomiseksi. Pyytää käyttäjältä salkun nimen ja sijoitusfrekvenssin (päivittäin, viikottain, kuukausittain) ja kutsuu sen pohjalta palvelukerroksen create_portfolio-palvelua.
* logout_UI: Kirjaa käyttäjän ulos
* open_portfolio_UI: Listaa käyttäjän salkut ja kysyy käyttäjältä mikä niistä avataan. Kutsuu tämän perusteella palvelukerroksen get_content-palvelua. 
* action_UI: Listaa mahdolliset toimenpiteet avoimelle salkulle, jotka ovat: Osta, myy, seuraava jakso (=älä tee mitään). Valittu toimenpide kutsuu vastaavaa palvelukerroksen palvelua. Valittavana on myös sovelluksen lopetus, uloskirjautuminen sekä edelliseen näkymään palaaminen.
* sell_UI: Näkymän kryptovaluutan myymiseksi. Kysyy käyttäjältä myytävän krypton numeron sekä summan. Kutsuu näiden perusteella palvelukerroksen sell-palvelua.
* buy_UI: Näkymän kryptovaluutan ostamiseksi. Kysyy käyttäjältä ostettavan krypton numeron sekä summan. Kutsuu näiden perusteella palvelukerroksen buy-palvelua. 

Kaikki tulostukset tapahtuvat käyttöliittymäkerroksessa (lukuunottamatta tietokantakyselyiden virheilmoituksia, jotka itse koin selkeämmäksi jättää repositories-kerrokseen). Usein tarvittavat tulostukset on eriytetty omiksi funktioikseen. 

Tulostuksissa käytettävät värikoodit löytyvät tiedostosta styles.py.


### Graafinen käyttöliittymä
* login_view: Tällä hetkellä graafinen käyttöliittymä tarjoaa yhden näkymän, jonka kautta voi kirjautua sisään tai luoda uuden käyttäjän. Käyttäjän valinnan perusteella käyttöliittymä  kutsuu palvelukerroksen palvelua signup tai login. Tämän jälkeen kontrolli siirtyy tekstikäyttöliittymään.
* gui.py: Kontrolloi näytettävää näkymää
* (practise_view: Harjoittelua ja testailua varten)


## Sovelluslogiikka
Sovelluksen ydintietomallin muodostavat luokat User, Portfolio, ReferencePortfolio ja Content. Näihin liittyvät attribuutit ja metodit on kuvattu ao. kuvassa:
   
![Luokkakaavio](https://github.com/ramipiik/ot-harjoitustyo/blob/main/dokumentaatio/luokkakaavio/luokkakaavio.jpg)  
   
Palvelukerroksen content_services.py sisältää mm. seuraavat salkun hallintaan liittyvät palvelut (alla listattu olennaisimmat):
* buy: Krypton ostaminen
* sell: Krypton myyminen 
* get_content: Hakee salkun sekä referenssisalkkujen sisällön sekä päivän arvon, kryptojen kurssit sekä tilastot
* next_period: Siirtyy seuraavaan päivään/viikkoon/kuukauteen salkusta riippuen
* coordinate_reference_actions: Suorittaa referenssisalkkujen strategiat. Referenssistrategioita on kuusi kappaletta:
  * Do nothing: Ei tee mitään. Sijoituksen arvo lopussa = sijoituksen arvo alussa
  * All-in: Sijoittaa kaikki heti alussa tasaisesti jaettuna eri kohteiden välille. Ei tee mitään sen jälkeen.
  * Even: Sijoittaa tasasumman per aikayksikkö kaikkien kohteiden välillä.
  * Random: Arpoo joka jakso kolme satunnaista kohdetta ja sijoittaa niihin. 
  * Follow: Panostaa edellisen jakson isoimpaan nousijaan
  * Contrarian: Panostaa edellisen jakson isoimpaan laskijaan

Palvelukerroksen crypto_services.py sisältää funktion
* get_crypto_ids: palauttaa kaikkien kryptojen crypto_id:t.

Palvelukerroksen portfolio_services.py sisältää seuraavat funktiot:
* create_portfolio: Luo uuden salkun
* get_portfolios: Palauttaa käyttäjään liittyvät salkut

Palvelukerroksen price_services.py sisältää funktion
* get_rates: palauttaa halutun päivän kryptokurssit

Palvelukerroksen statistics_services.py-tiedoston olennaisimmat funktiot ovat:
* get_price_statistics: Laskee ja palauttaa kryptohintojen statistiikat. 
* get_portfolio_statistics: Laskee ja palauttaa kryptosalkun statistiikat. Käytetäään sekä käyttäjän että referenssisalkkujen laskemiseen.

Palvelukerroksen user_services.py-tiedoston olennaisimmat funktiot ovat:
* login: Käyttäjän kirjautuminen. Jos kirjautuminen onnistuu, palauttaa User-olion.
* signup: Uuden käyttäjän luominen. 


## Tietojen pysyväistallennus
Käytössä on SQLite-tietokanta: [Tietomalli](https://github.com/ramipiik/ot-harjoitustyo/blob/main/src/schema.sql).

Pakkaus repositories sisältää allaolevat toiminnallisuudet tiedon tallettamiseksi ja lukemiseksi tietokantaan.

Tiedoston content_repository.py olennaisimmat funktiot ovat:
* store_content_first_time: Tallettaa salkun sisällön tietokantaan ensimmäisen kerran
* store_content: Tallettaa salkun sisällön tietokantaan.
* read_portfolio_content: Lukee salkun sisällön tietokannasta
* read_portfolio_history: Lukee salkun historiallisen arvon kehityksen tietokannasta

Tiedoston crypto_repository.py olennaisimmat funktiot ovat:
* store_cryptos: Tallettaa kryptovaluutat tietokantaan. Tarvitaan tietokantaa alustettaessa.
* read_crypto_names_and_ids: Lukee ja palauttaa kryptojen nimet ja id:t tietokannasta

Tiedoston portfolio_repository.py olennaisimmat funktiot ovat:
* store_portfolio: Tallettaa uuden salkun tietokantaan
* store_reference_portfolios: Tallettaa uuden salkun referenssistrategioiden salkut tietokantaan.
* read_reference_portfolios: Lukee ja palauttaa käyttäjän salkun referenssisalkkujen id:t
* read_portfolios: Lukee ja palauttaa käyttälle kuuluvat salkut

Tiedoston price_repository.py olennaisimmat funktiot ovat:
* read_prices: Lukee ja palauttaa annetun päivän kryptokurssit
* read_prices_for_statistics: Lukee ja palauttaa historialliset kryptokurssit
* store_prices: Lukee kryptojen hinnat CSV-tiedostosta ja tallettaa ne tietokantaan. Käytetään uutta tietokantaa alustettaessa.
* read_volatility_data: Lukee edellisen vuoden kurssit jokaiselle päivälle volatiliteetin (=keskihajonnan) laskemiseksi

Tiedoston user_repository.py olennaisimmat funktiot ovat:
* verify_user: Käyttäjätunnuksen ja salasanan tarkistus sisääkirjauduttaessa
* store_user: Uuden käyttäjän tallennus
* delete_user: Poistaa käyttäjän tietokannasta


## Päätoiminnallisuudet
Sovelluksen päätoiminnallisuus on kryptoihin sijoittaminen ja salkun arvon kehityksen seuranta. Käydään tähän liittyen kaksi olennaista prosessia tarkemmin läpi, sillä oletuksella, että kaikki sujuu hyvin eli tule poikkeuksia. 


### Krypton ostaminen esimerkin avulla kuvattuna
Käyttäjällä rami on avattuna ramin_salkku.
rami kertoo käyttöliittymän kautta, että hän haluaa ostaa salkkuun kryptoa numero 1 sadalla eurolla.
1. Käyttöliittymä kutsuu palvelukerroksen buy-palvelua paremetreillä: (ramin_salkun_sisältö, krypto_1, 100€)
1. Palvelukerroksen buy-palvelu kutsuu ramin_salkku Content-olion buy-metodia parametreillä (krypto_1, 100€)
1. Jos salkussa on tarpeeksi rahaa ja ko. krypto on olemassa, Content-olio palauttaa True.
1. Palvelukerroksen buy-palvelu tallentaa päivitetyn Content-olion sisällön tietokantaan kutsumalla repository-kerroksen palvelua store_content parametrilla (ramin_salkun_sisältö)
1. Mikäli transaktio ei onnistu, palautuu käyttöliittymään tuple (False, virheilmoitus).
1. Jos transaktio onnistui, käyttöliittymä hakee salkun sisällön kutsumalla funktiota get_content ja tulostaa sen kutsumalla funktiota print_status(ramin_salkun_sisältö).


### Seuraavaan jaksoon siirtyminen esimerkin avulla yksinkertaistettuna kuvattuna
1. Käyttäjällä rami on avattuna ramin_salkku.
1. rami kertoo käyttöliittymän kautta, että hän haluaa siirtyä seuraavaan päivään.
1. Käyttöliittymä kutsuu palvelukerroksen coordinate_reference_actions palvelua parametrillä (ramin_salkun_sisältö)
   * coordinate_reference_actions kutsuu jokaiselle referenssistrategialle palvelua implement_reference_strategy,
   * joka laskee kullekin referenssistrategialle strategian mukisen toimenpiteen. 
   * Referenssistrategiodien tekemät transaktiot tallennetaan taulukkoon action_log, joka palautetaan takaisin käyttöliittymälle.
1. Seuraavaksi käyttöliittymä kutsuu palvelukerroksen next period palvelua parametrilla(ramin_salkun_sisältö).
   * Next period -palvelu kutsuu next day -funktiota 1/7/30 kertaa riippuen salkun päätöksentekofrekvenssistä (päivä, viikko, kuukausi).
   * Next day tallentaa salkun sisällön ja arvon jokaiselle päivälle kutsumalla repositorio-kerroksen funktiota store_content parametreillä (ramin_salkun_sisältö, kryptokurssit).
   * Salkun arvon voisi myös laskea lennosta aina tarvittaessa, mutta koin itse varmempana, että se tallennetaan erikseen tietokantaan jokaisen päivän kohdalla. Toimintavarmuuden lisäksi siinä on etuna, että statistiikan (esim. edellisen vuoden keskihajonta) laskeminen sujuu nopeasti, koska lähtöarvot voi hakea suoraan tietokannasta.
1. Käyttöliittymät hakee salkun sisällön ja arvon kutsumalla palvelukerroksen funktiota get_content ja tulostaa sisällön kutsumalla käyttöliittymäkerroksen funktiota print_status.


## Ohjelman rakenteeseen jääneet heikkoudet
* Valitettavasti vaikuttaa siltä, että en ehdi tehdä graafista käyttöliittymää valmiiksi kurssin puitteissa.
* Itselleni oli välillä vaikea hahmottaa milloin tietoa kannattaa käsitellä olioiden kautta ja milloin ei. Näin erityisesti sen jälkeen kun aloin tallentamaan tietoa relaatiotietokantaan, koska tietokannan rakenne ei ole sama kuin olioiden rakenne. Päädyin toteutukseen, jossa olioita ovat käyttäjä, salkun, salkun sisältö ja referenssisalkku. Kaikille käyttäjille yhteiset globaalit muuttujat kuten kryptojen hinnat eivät ole sidottuja olioihin. Tämä tuntuu periaatteessa järkevältä, mutta käytännössä tuntuu silti, että tieto liikkuu ohjelman sisällä hieman sekavasti välillä olion atribuuttina, välillä funktion parametrina ja välillä tietokannasta luettuna. Onkohan tähän object <-> relational database -ongelmaan jotain hyvää ajattelutapaa?
