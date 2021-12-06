# Vaatimusmäärittely
## Sovelluksen tarkoitus
 * Sovelluksen avulla pystyy harjoittelemaan ja simuloimaan eri kryptovaluuttoihin sijoittamista historiallista dataa vasten.
 * Mukana olevat kryptovaluutat tarkentuvat projektin aikana. En tiedä tässä vaiheessa kuinka helposti riittävän pitkä aikasarja kustakin sijoituskohteesta on löydettävissä ilmaiseksi.
 
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
* TEHTY: Pelin lopettaesa pelitilanne tallennetaan ja kirjautumisen jälkeen peliä voi seuraavalla kerralla jatkaa samasta kohdasta. 
* Sovellus laskee muutama yksinkertaista referenssisijoitusstrategiaa, joita vastaan käyttäjä kilpailee. Alustavia ajatuksia alla. Kaikkia en varmaan ehdi toteuttaa tämän kurssin puitteissa.
  * Do nothing: Älä tee mitään. Sijoituksen arvo lopussa = sijoituksen arvo alussa
  * All-in: Sijoita kaikki heti alussa tasaisesti jaettuna eri kohteiden välille. Älä tee mitään sen jälkeen.
  * Even: Sijoita tasasumma per aikayksikkö valittujen kohteiden välillä.
  * Random: Satunnainen strategia (heitä noppaa ja tee sijoituspäätös sen mukaisesti)
  * Follow: Panosta edellisen jakson isoimpaan nousijaan
  * Contrarian: Panosta edellisen jakson isoimpaan laskijaan


## Käyttöliittymäluonnos
 * [Käyttöliittymäluonnos](https://github.com/ramipiik/ot-harjoitustyo/blob/main/dokumentaatio/K%C3%A4ytt%C3%B6liittym%C3%A4luonnos.pdf)
 * TEHTY: Tekstikäyttöliittymä

## Jatkokehitysideoita
* Visio on mallintaa ja testata oikeasti (mahdollisesti) hyödyllisiä sijoitustrategioita/algoritmeja (Markovin ketju, portfolioteoria, machine learning -algoritmeja, jne ) ja verrata niiden saamia tuottoja keskenään eri sijoituskohteiden ja aikajänteiden välillä ja tehdä tämän pohjalta sijoitusbotti, joka tekee oikeita sijoituspäätöksiä/suosituksia.
* Aihe on varsin laaja. Tavoitteenna on tämän kurssin aikana tehdä pohjatyö, jota voin myöhemmin (esim. gradun tai muiden kurssien puitteissa tai omana vapaa-ajan projektina) kehittää ja laajentaa eteenpäin erityisesti älykkäämpien sijoitusalgoritmien ja koneoppimisen osalta. 
