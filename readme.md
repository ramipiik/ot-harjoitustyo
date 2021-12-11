# Sijoitussimulaattori
Sovelluksen avulla voi harjoitella kryptovaluuttoihin sijoittamista.

## Releases
- [Viikko 4](https://github.com/ramipiik/ot-harjoitustyo/releases/tag/viikko4)
- [Viikko 5](https://github.com/ramipiik/ot-harjoitustyo/releases/tag/viikko5)

## Dokumentaatio
- [Vaatimusmäärittely](https://github.com/ramipiik/ot-harjoitustyo/blob/main/dokumentaatio/vaatimusmaarittely.md)
- [Tuntikirjanpito](https://github.com/ramipiik/ot-harjoitustyo/blob/main/dokumentaatio/tuntikirjanpito.md)
- [Arkkitehtuurikuvaus](https://github.com/ramipiik/ot-harjoitustyo/blob/main/dokumentaatio/arkkitehtuuri.md)

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

