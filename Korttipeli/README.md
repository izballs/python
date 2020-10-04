# Python3 -Pokeripeli
--Tekijä | Juuso Yli-Sorvari | TITE16

## Pelin rakenne
Korttipeliin on tehty erikseen palvelin ja itse client puoli. Palvelin osuus tallentaa kaikki osumat (parit, 2 paria kolmoset jne…) MySQL tietokantaan ja palauttaa ne tarvittaessa. Palvelin myös tallentaa tietokantaan ennätykset, eli paljonko käyttäjä on saanut rahaa. Client puolella on käyttöliittymä missä itse pokeripeli pyörii.

## Käytetyt kirjastot palvelinpuolella
### Flask
* Kirjastoa käytetään RESTApin luomiseen. Flaskillä saamme otettua vastaan HTTP pyyntöjä, joiden avulla sitten tehdään oikeanlaiset MySQL haut tai lisäykset.
### Flask-Login
* Flaskin-Login kirjaston avulla voimme luoda RESTApin niin, että HTTP pyyntöjä ei voi lähettää muuta kuin tunnistautunut käyttäjä.
### PyMySQL
* PyMYSQL kirjastolla luodaan MySQL yhteys ulkoiselle palvelimelle. Kirjastoa käytetään myös itse kannan hakujen tekoon ja tietokannan päivittämiseen.

## Käytetyt kirjastot client-puolella
### PyQT5
* PyQT5 kirjasto sisältää kaiken käyttöliittymään liittyvän. Kirjastosta käytetään paljon erilaisia luokkia, jotka ovat tarpeellisia pelin toiminnan kannalta. Itsesovellus rakennetaan toimimaan QApplication luokan sisällä. Tämän sisään sitten luodaan esimerkiksi erilaisia QWidgettejä, jotka toimivat ruutuina joihin voimme luoda kontekstia kuten erilaisia nappeja QPushButtonillla tai tekstiä QLabelilla. Ohjelmassa käytetään myös erilaisia asetteluun tarkoitettuja ”Layout” luokkia. Näitä on esimerkiksi QGridLayout ja QHBoxLayout.
* Kirjastosta käytetään myös erilaisia graafisia ominaisuuksia kuten QPixmap luokkaa, joka käytännössä pitää sisällään vain asetetun kuvan ja kuvan arvot (korkeus, leveys). QGraphicsOpacityEffect luokalla on toteutettu pelin animaatiot, joissa kortit ilmestyy ruudulle ja poistuu ruudulta häivyttämällä.
### Random
* Random luokkaa käytetään itse korttipakan sekoittamiseen. Tämä tapahtuu käytännössä niin, että korttipakka on vain List luokan jäsen ja tämä lista korteista asetetaan sattumanvaraiseen järjestykseen random.shuffle metodilla.
### Collections
* Tätä luokkaa käyetään kun tarkastetaan onko käyttäjällä voittoja. Korteista haetaan arvot ja maat omiin listoihin ja nämä listat tarkistetaan Collections.Counter metodilla, joka palauttaa kuinka paljon samoja arvoja pöydällä esiintyy. Tätä tietoa hyväksikäyttäen tapahtuu sitten itse tarkastus operaatio.
### Requests
* Requests kirjastosta käytetään Session luokkaa. Tämän avulla voimme tehdä palvelimelle haku pyyntöjä ja lähettää RESTApiin päivitys pyyntöjä POST ja GET metodeilla. Tätä tarvitaan itse ennätyslistan hakuun ja ainakun pöytä on tarkastettu lähetetään myös tieto palvelimelle tuliko pari, kolmoset jne… Myös itse kirjautuminen palvelimelle suoritetaan Session luokalla, sillä se pitää yhteyden palvelimeen kokoajan elossa, jolloin uudelleen kirjautumista ei tarvita kesken pelin. 

## Itse luodut luokat
### Kortti(QPushButton)
* Kortti luokka perii QPushButtonin ja siihen on asetettuna kortin kuvan osoite, kortin arvo, maa, onko valittu vai ei ja näiden palautus metodit.
### Korttipakka()
* Korttipakka luokka pitää sisällään listan kaikista pakan korteista. Kun luokka käynnistyy ensimmäisen kerran se luo kaikki Kortti luokan muuttujat listaan. Se pitää sisällään myös korttipakan sekoitus metodin, korttienjako metodin ja korttienvaihto metodin.
### Poyta(QGridLayout)
* Pöytä luokka pitää sisällään itse graafisen käyttöliittymän siitä miltä sovellus ulkoisesti näyttää. Pöytä luokassa on määriteltynä 5 kortin paikat, voitonjako taulukon, panosnäkymän ja tarvittavat napit ennätyslistalle ja kortien jaolle. Luokka pitää myös sisällään metodit Laitakortti – Käytetään Korttipakka luokan sisällä kortin jakamiseen pöydälle. Valitse – Käytetään kortin valitsemiseen, joka antaa kortille arvoksi valittu. Nosta panosta ja Laske panosta – metodeilla määritellään panoksen suuruus. Panos on voi olla 0.20€, 0.40€, 0.60€, 0.80€, 1€, 2€. GetVaihdettavat – metodilla tarkastetaan kaikki pöydällä olevat kortit, haluaako käyttäjä vaihtaa kortteja vaiko eikö. Tarkasta pöytä – Tällä metodilla tarkastetaan, onko voittoja vai ei. JaaKortit – metodissa kutsutaan korttipakan samaista metodia, jossa jaetaan kortit ja samalla tehdään tarvittavat varmistukset, ettei esimerkiksi voi panosta enää muuttaa. Vaihda kortit – metodissa otetaan korteista poista klikkaus ominaisuus pois ja tehdään muut tarpeelliset operaatiot. Tyhjää pöytä – metodissa tyhjätään pöytäkorteista ja luodaan pakkaan kyseiset kortit uudelleen, jonka jälkeen pakka vielä sekoitetaan.

## Pelin käynnistäminen
* Korttipeli on käynnistettävä Python3:sella sillä PyQT5 ei ole Python2 yhteensopiva. Peli tarkastaa aivan aluksi löytyykö flask palvelinta paikallisesti (osoitteesta 127.0.0.1:5000), jos palvelin ei vastaa niin siirrytään käyttämään ulkoista palvelinta, joka sijaitsee minun omalla virtuaalipalvelimella osoiteessa izba.ovh:5000. Vielä jos käy niin, ettei ulkoinenkaan palvelin vastaa peli käynnistyy ilman verkko-ominaisuuksia.

## Pavelimen käynnistäminen
* Jotta palvelimen saa käyntiin on käytettävällä koneella oltava asennettuna flask. Tämä asentuu komennolla pip3 install flask. Flask itsessään tarvitsee vielä parametrit mitä python tiedostoa käytetään palvelinohjelman lataamiseen. Linux puolella tämä toteutetaan komennolla export FLASK_APP=”server.py”. Windows puolella taas jos kyseessä on CMD käytetään komentoa set FLASK_APP=”server.py”, mutta jos käytössä on PowerShell komento on $env:FLASK_APP=”server.py”. Kun parametri on asetettu voimme käynnistää palvelin ohjelmiston komennolla flask run. Tämä käynnistää palvelimen paikalliseen verkkoon toimivaksi. Koska palvelin toimii myös ulkoiselta palvelimelta python tiedoston loppuun on lisätty rivi app.run(host=”0.0.0.0”, port=”5000”), jonka jälkeen ohjelman voi käynnistää python3 server.py komennolla ja se toimii myös ulkoverkkoon päin.
