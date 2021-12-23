# Käyttöohje
Löydät viimeisimmän releasen [täältä](https://github.com/ramipiik/ot-harjoitustyo/releases). Lataa tiedostot klikkaamalla Assets-otsikon alla olevaa linkkiä "_Source code (zip)_"

## Ohjelman käynnistäminen
1. Asenna Poetry ao. komennolla tai katso tarkemmat ohjeet [täältä](https://python-poetry.org/docs/#installation): 
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -
```

2. Asenna riippuvuudet komennolla:
```
poetry install
```

3. Ensimmäisellä kerralla: Alusta SQlite-tietokanta ajamalla komento:
```
poetry run invoke initiate-db
```

4. Käynnistä sovellus tekstikäyttöliittymässä ajamalla komento:
```
poetry run invoke start
```

5. Tai käynnistä sovellus graafisessa käyttöliittymässä ajamalla komento:
```
poetry run invoke start-gui

## Kirjautuminen
Sovellus käynnistyy kirjautumisnäkymään. Voit luoda uuden käyttäjän tai kirjautua sisään olemassaolevalla käyttäjällä. Jos valitsit graafisen käyttöliittymän, käyttö jatkuu tekstikäyttöliittymässä.  

![kirjautumisnäkymä](https://github.com/ramipiik/ot-harjoitustyo/blob/main/dokumentaatio/kuvat/Kirjautumisn%C3%A4kym%C3%A4.png).  

## Peruskäyttö
Avaa haluamasi salkku syöttämällä salkun numero. Tai luo uusi salkku valitsemalla 'C'. Uuden salkun alkupääoma on miljoona euroa.  
  
![Valitse salkku](https://github.com/ramipiik/ot-harjoitustyo/blob/main/dokumentaatio/kuvat/Valitse%20salkku.png)
  
Uuden salkun luonti tapahtuu antamalla salkulle nimi sekä määrittällä haluatko tehdä sijoituspäätöksiä päivittäin, viikottain vai kuukausittain.  
  
![Uusi salkku](https://github.com/ramipiik/ot-harjoitustyo/blob/main/dokumentaatio/kuvat/Uusi%20salkku.png)  
  
Saat näkyviin salkkunäkymän, joka näyttää
* salkun sisällön
* Referenssistrategiat ja oman salkkusi listattuna paremmuusjärjestykseen salkun arvojen perusteella
* Kryptovaluuttojen päivän kurssit  
  
![Salkkunäkymä](https://github.com/ramipiik/ot-harjoitustyo/blob/main/dokumentaatio/kuvat/Salkkun%C3%A4kym%C3%A4.png)  
  
Seuraavaksi voit valita haluamasi toimenpiteen seuraavista vaihtoehdoista:
* B: Osta kryptoja
* S: Myy kryptoja. Lyhyeksi myynti on sallittua eli kryptovaluutan määrä voi olla negatiivinen.
* N: Siirry seuraavaan ajanjaksoon
* P: Palaa takaisin salkkulistaukseen
* X: Kirjaudu ulos
* Q: Lopeta
  
![Toimenpide](https://github.com/ramipiik/ot-harjoitustyo/blob/main/dokumentaatio/kuvat/Toimenpide.png)  
  
Krypton ostaminen ja myyminen tapahtuvat syöttämällä halutun valuutan numero sekä summa euroissa. Ostaminen ei onnistu, jos käteinen ei riitä.    

![Osto](https://github.com/ramipiik/ot-harjoitustyo/blob/main/dokumentaatio/kuvat/Osto.png)  
  
## Muuta
Kryptovaluutat ja hinnat ovat todellisia. Sijoituskausi alkaa 1.6.2020 tilanteesta. Hintadataa on tallennettu 9.11.2021 asti.
