# Vaatimusmäärittely
## Sovelluksen tarkoitus
 * Sovelluksen avulla pystyy harjoittelemaan ja simuloimaan eri kryptovaluuttoihin sijoittamista historiallista dataa vasten.
 
## Käyttäjät
* TEHTY: Ensi vaiheessa ei ole muita rooleja kuin normikäyttäjä 
* TEHTY: (Uudet sijoituskohteet ja strategiat tallennetaan suoraan tietokantaan tai luodaan koodissa.)

### Ennen kirjautumista
* TEHTY: Sovellus vaatii kirjautumista
* TEHTY: Ennen kirjautumista vaihtehdot ovat: 1) Kirjaudu tai 2) Luo käyttäjätunnus

## Kirjautumisen jälkeen
* TEHTY: Käyttäjä saa alussa miljoona euroa, jotka hän voi sijoittaa haluamallaan tavalla.
* TEHTY: Käyttäjä voi valita haluaako tehdä sijoituspäätöksiä kerran päivässä, kuukaudessa vai vuodessa. (Tämä tarkentuu datan saatavuuden mukaan.)
* TEHTY: Käyttäjä voi valita haluamansa sijoitusjakson pituuden (x kuukautta/vuotta).
* TEHTY: Käyttäjä voi valita haluamansa sijoituskohteet 
* TEHTY: Lopetettaessa pelitilanne tallennetaan ja kirjautumisen jälkeen peliä voi seuraavalla kerralla jatkaa samasta kohdasta. 
* TEHTY: Sovellus sisältää ao. referenssisijoitusstrategiat, joita vastaan käyttäjä kilpailee.
  * TEHTY: Do nothing: Älä tee mitään. Sijoituksen arvo lopussa = sijoituksen arvo alussa
  * TEHTY: All-in: Sijoita kaikki heti alussa tasaisesti jaettuna eri kohteiden välille. Älä tee mitään sen jälkeen.
  * TEHTY: Even: Sijoita tasasumma per aikayksikkö valittujen kohteiden välillä.
  * TEHTY: Random: Satunnainen strategia (heitä noppaa ja tee sijoituspäätös sen mukaisesti)
  * TEHTY: Follow: Panosta edellisen jakson isoimpaan nousijaan
  * TEHTY: Contrarian: Panosta edellisen jakson isoimpaan laskijaan


## Käyttöliittymäluonnos
 * TEHTY: Tekstikäyttöliittymä
 * ALOITETTU: [Graafinen käyttöliittymä](https://github.com/ramipiik/ot-harjoitustyo/blob/main/dokumentaatio/K%C3%A4ytt%C3%B6liittym%C3%A4luonnos.pdf)
 

## Jatkokehitysideoita
* Tavoitteena on tämän kurssin aikana tehdä pohjatyö, jota voin myöhemmin (esim. gradun tai muiden kurssien puitteissa tai omana vapaa-ajan projektina) kehittää ja laajentaa eteenpäin erityisesti älykkäämpien sijoitusalgoritmien ja koneoppimisen osalta. 
* Visio on mallintaa ja testata oikeasti (mahdollisesti) hyödyllisiä sijoitustrategioita/algoritmeja (Markovin ketju, portfolioteoria, machine learning -algoritmeja, jne ) ja verrata niiden saamia tuottoja keskenään eri sijoituskohteiden ja aikajänteiden välillä ja tehdä tämän pohjalta sijoitusbotti, joka tekee oikeita sijoituspäätöksiä/suosituksia.
* Tee seuraavat toimenpiteet, jotta käyttäjä ei pysty opettelemaan hintakehitystä ulkoa:
  * Valitse salkulle satunnainen aloituspäivä ("day0" tai "epoch"). 
  * Normalisoi kryptojen arvot siten, että kaikki alkavat samasta arvosta (esim. 100)
  * Anonomysoi ja arvo eri nimet kullekin kryptolle (A, B, C jne)
* Laajenna graafista käyttöliittymää. Erityisesti graafien pitäisi auttaa hintakehityksen havainnollistamisessa.
