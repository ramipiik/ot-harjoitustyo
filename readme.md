# Ohjelmistotekniikan harjoitustyö

## Sovelluksen käynnistäminen
* Kopioi repositorio komennolla:
```
git clone https://github.com/ramipiik/ot-harjoitustyo.git
```

* Asenna Poetry ao. komennolla tai katso tarkemmat ohjeet [täältä](https://python-poetry.org/docs/#installation): 
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -
```

* Lisää poetry pathiin komennolla, missä 'xxx' on oma käyttäjätunnuksesi.
```
export PATH=/home/xxx/.local/bin:$PATH
```

*Kysymys ohjaajalle: Omalla koneellani voin lisätä yo. rivin tiedostoon ~/.bashrc, jolloin sitä ei tarvitse lisätä joka kerta erikseen.
Miten voin tehdä saman yliopiston serverillä?*

* Asenna riippuvuudet komennolla:
```
poetry install
```

* Käynnistä sovellus ajamalla allaoleva komento **src** -kansiossa:
```
poetry run invoke start
```

## Tehtävät viikko 1
[gitlog.txt](https://github.com/ramipiik/ot-harjoitustyo/blob/main/laskarit/viikko1/gitlog.txt)    
[komentorivi.txt](https://github.com/ramipiik/ot-harjoitustyo/blob/main/laskarit/viikko1/komentorivi.txt)  

## Tehtävät viikko 2
[coverage report.png](https://github.com/ramipiik/ot-harjoitustyo/blob/main/laskarit/viikko2/Coverage%20report.png)

## Tehtävät viikko 3
[luokkakaavio.jpg](https://github.com/ramipiik/ot-harjoitustyo/blob/main/laskarit/viikko3/Luokkakaavio.jpg)  
[sekvenssikaavio3.png](https://github.com/ramipiik/ot-harjoitustyo/blob/main/laskarit/viikko3/Sekvenssikaavio%203.png)  
[sekvenssikaavio4.png](https://github.com/ramipiik/ot-harjoitustyo/blob/main/laskarit/viikko3/Sekvenssikaavio4.png)
