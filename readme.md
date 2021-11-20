# Sijoitussimulaattori
Sovelluksen avulla voi harjoitella kryptovaluuttoihin sijoittamista.

## Kysymys ohjaajalle
* Onnistun ajamaan sovellusta sekä omalla koneellani että yliopiston koneella ssh-yhteyden kautta.
* Virtuaalityöaseman https://vdi.helsinki.fi/ kautta käyttö ei kuitenkaan onnistu. Jostain syystä SQLite ei osaakaan kirjoittaa tietokantaan virtuaalityöaseman kautta. Itselläni ei ole oikeuksia päivittä SQliteä uudempaan versioon (sudo apt install sqlite3), enkä oikein keksi mikä muu siinä voisi olla ongelmana.
* Itselleni riittää erittäin hyvin, että sovellus toimii ssh-yhteyden kautta. Jos on kuitenkin pakollinen vaatimus, että sovellus toimii myös vdi:n kautta, niin tarvitsisin tähän neuvoja. Kiitos.

## Dokumentaatio
- [Vaatimusmäärittely](https://github.com/ramipiik/ot-harjoitustyo/blob/main/dokumentaatio/vaatimusmaarittely.md)
- [Tuntikirjanpito](https://github.com/ramipiik/ot-harjoitustyo/blob/main/dokumentaatio/tuntikirjanpito.md)

## Sovelluksen käynnistäminen
1. Kopioi repositorio komennolla:
```
git clone https://github.com/ramipiik/ot-harjoitustyo.git
```

2. Asenna Poetry ao. komennolla tai katso tarkemmat ohjeet [täältä](https://python-poetry.org/docs/#installation): 
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -
```

3. Halutessasi lisää poetry pathiin komennolla, missä 'xxx' on oma käyttäjätunnuksesi.
```
export PATH=/home/xxx/.local/bin:$PATH
```

4. Asenna riippuvuudet komennolla:
```
poetry install
```

5. Ensimmäisellä kerralla: Alusta SQlite-tietokanta ajamalla komento:
```
poetry run invoke initiate-db
```

6. Käynnistä sovellus ajamalla allaoleva komento:
```
poetry run invoke start
```
## Muut komennot

### Testit
Testit voi ajaa komennolla:
```
poetry run invoke test
```
### Testikattavuus
Testikattavuusraportin saa komennolla:
```
poetry run invoke coverage-report
```
### Linttaus
Linttauksen voi ajaa komennolla:
```
poetry run invoke lint
```

