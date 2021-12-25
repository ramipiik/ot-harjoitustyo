# Testausdokumentti
Sovelluksen automaattinen yksikkö- ja integraatiotason testaus tapahtuu Pythonin unit test -kirjaston avulla. 

Testit voi ajaa komennolla:
```
poetry run invoke test
```

Testikattavuusraportin saa komennolla:
```
poetry run invoke coverage-report
```

Järjestelmätason testit suoritetaan käsin.

## Yksikkö- ja integraatiotestaus

Moduuli [content_test.py](
https://github.com/ramipiik/ot-harjoitustyo/blob/main/src/tests/content_test.py) testaa salkun sisältöön liittyviä sovelluslogiikka- sekä repositoriokerroksen toiminnallisuuksia. 

Moduuli [crypto_test.py](https://github.com/ramipiik/ot-harjoitustyo/blob/main/src/tests/crypto_test.py) testaa, että kaikki määritellyt kryptot löytyvät tietokannasta. 

Moduuli [portfolio_test.py](https://github.com/ramipiik/ot-harjoitustyo/blob/main/src/tests/portfolio_test.py) testaa salkkujen hallintaan liittyviä toiminnallisuuksia.

Moduuli [price_test.py](https://github.com/ramipiik/ot-harjoitustyo/blob/main/src/tests/price_test.py) testaa, että kryptojen hinnat löytyvät tietokannasta.

Moduuli [statistics_test.py](https://github.com/ramipiik/ot-harjoitustyo/blob/main/src/tests/statistics_test.py) sisältää portfolion sisällön ja kryptohintojen arvon muutosten laskentaan liittyvät testit.

Moduuli [user_test.py](https://github.com/ramipiik/ot-harjoitustyo/blob/main/src/tests/user_test.py) sisältää käyttäjänhallintaan liittyvät testit.

Käyttöliittymäkerrosta varten ei ole testejä.

Testikattavuus on 79%. Käyttöliittymäkerros sekä tiedostot [main.py](https://github.com/ramipiik/ot-harjoitustyo/blob/main/src/main.py) ja [config.py](https://github.com/ramipiik/ot-harjoitustyo/blob/main/src/config.py) on jätetty pois testeistä.  

![Test coverage](https://github.com/ramipiik/ot-harjoitustyo/blob/main/dokumentaatio/kuvat/Test-coverage.png)  
  
Testaamatta jääneet koodirivit liittyvät lähinnä poikkeustilanteiden käsittelyyn. Ydinprosessit sekä yleisimmät vääristä syötteistä johtuvat virheet on käsitelty testeissä.

## Järjestelmätestaus
Varsinaisia automaattisia järjestelmätason testejä ei ole. Manuaalisia testejä suoritettu lukematon määrä. Kaikki testit on suoritettu Linux-ympäristössä.

## Sovellukseen jääneet laatuongelmat
SQlite ei tällä hetkellä toimi yliopiston virtuaalityöasemalla vanhasta versiosta johtuen. En ehtinyt selvittää miten tämän olisi saanut ratkaistua.  

Kun sovellus käynnistetään poetryn kautta jostain syystä komentorivin backscape ei toimi kun syötteitä annetaan terminaalin kautta. Jos sovelluksen käynnistää ilman poetrya, niin backscape toimii.  
  
Tekstikäyttöliittymän rivinvaihdot eivät aina osu kohdalleen poetryn kautta. Ilman poetrya kaikki näyttää normaalilta. Tämä on lähinnä visuaalinen haitta. En keksinyt miten sen saisi korjattua. 
