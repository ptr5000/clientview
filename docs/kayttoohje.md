

# Asennusohje

Sovellus on yksinkertainen Python-sovellus joten asennus onnistuu
suoraviivaisesti näin:

1. Kloonaa https://github.com/ptr5000/clientview omalle koneellesi
2. cd clientview 
3. pip install -r requirements.txt
4. python3 run.py

# Käyttöohje

Sovelluksessa on kaksi erilaista käyttäjätunnustyyppiä. Admin -tunnuksella
hallitaan tilauksia ja laskujen vastaanottoa, muilla tunnuksilla
voidaan hallita omia tietoja ja lähettää laskuja tilauksista. 


## Uuden alihankkijan rekisteröityminen

### Uuden tunnuksen luominen

    1. Rekisteröidy palveluun uudella käyttäjätunnuksella
    2. Määrittele yrityksen tiedot 

    Tunnus on nyt valmis lähettämään laskuja. 

### Laskun lähettäminen

    1. Valitse vasemmalta näkymä "Send Invoices"
    2. Näet listan tilauksista (jos et näe tilauksia, tee ensiksi tilaus seuraamalla ohjeita kohdassa "Tilauksen tekeminen Admin -tunnuksella")
    3. Luo tilauksesta lasku valitsemalla "Create new invoice" ja paina laskun esikatselunäkymässä "Send invoice" -nappia. 

## Tilauksen tekeminen Admin -tunnuksella

### 1. Määrittele ensimmäinen kustannuspaikka

Valitse sivusta Settings -> Cost Centers ja lisää uusi kustannuspaikka. Kustannuspaikka
on käytännössä se yrityksen osa joka tilaa. Tämä osoitetieto näkyy myös laskulla.

### 2. Lisää ensimmäinen tuote

Valitse sivusta Settings -> Products ja lisää uusi tuote painamalla "Create new product" -nappulaa.
Määrittele tuotteelle nimi ja hinta. 

### 3. Tee ensimmäinen tilaus

Tässä vaiheessa kannassa pitäisi olla luotuna vähintään yksi alihankkija-tunnus em. ohjeiden
mukaisesti.

1. Valitse "Orders" -näkymä ja paina "Create new order" nappia. 
2. Valitse kustannnuspaikka (cost center) joka tekee tilauksen.
3. Valitse alihankkija jolta tilaus tehdään.
4. Valitse tilattavat tuotteet
5. Lähetä tilaus Submit -napista. 

Tilaus on nyt tarkasteltavissa valitun alihankkijan näkymässä josta lasku
voidaan lähettää. Kun alihankkija lähettää laskun, ilmestyy se adminin Inbox -näkymään.
