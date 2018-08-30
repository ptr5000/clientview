# ClientView kurssille Tsoha-18 (loppukesä)

## Alkuperäinen tavoite

Kyseessä on sovellus joka pohjautuu oikeaan tarpeeseen. Eräs legacy palvelu
poistuu käytöstä ja sillä on riippuvuuksia useisiin kirjastoihin ja palvelimiin. Sen ajaminen tuotantoserverien sammuttamisen jälkeen on todella vaikeaa ja ikävää (erityisesti esim. 10v päästä). Palvelu sisältää kymmenien taulujen lisäksi myös tietoja alihankkijoista (osoitetiedot, paikalliset VAT-koodit jne) sekä laskuja. Tämän sovelluksen idea on tarjota näkymä asiakasrekisteriin, tilauksiin, alihankkijoiden tietoihin ja järjestelmässä oleviin laskuihin mikäli esim. verottaja tarvitsee tarkempia tietoja joskus. 

CRUD näkymät tulevat tämän kurssin puitteissa alihankkijatiedolle, työtilaukselle, laskuille ja niiden vastaanottajille. Lisäksi tulee kirjautuminen ja käyttäjänhallinta jolla erotellaan lähinnä pääkäyttäjä ja alihankkija (laskuttaja). Kanta on puhtaasti tähän uuteen sovellukseen/kurssiin suunniteltu koska legacy kanta pitää sisällään myös paljon "turhaa" tietoa mitä voidaan esittää yksinkertaisemmin.

## Toteutunut projekti

Todellisuudessa sovellus on kurssia varten hieman erilainen kuin alunperin oli tarkoitus. Alkuperäinen ajatus oli liian yksinkertainen, koska
käytännössä esimerkiksi kirjautumista, rekisteröitymistä ym. ei olisi tarvittu. Yhteenvetoja ei myöskään oikeastaan tarvita joten ne on tehty kurssia varten erikseen. Lopputulos on kuitenkin pieni ja näppärä tilausten sekä laskujen hallinnointisovellus joka voidaan 
muuttaa alkuperäisen tavoitteen mukaiseksi pienellä vaivalla. 

Sovellus mahdollistaa tilausten teon tuotteista jotka ovat määritelty kantaan ennalta. Tämän pohjalta alihankkija joka tuotteet toimittaa,
voi nähdä tilauksen omalla tunnuksellaan ja lähettää automaattisesti generoidun laskun joka sitten näkyy Admin -tunnuksen
saapuneissa laskuissa. 

# [Demo](https://tsoha-clientview.herokuapp.com)

# Muut dokumentit

- [Tietokantakaavio](https://raw.githubusercontent.com/ptr5000/clientview/master/docs/clientview.png)
- [Käyttäjätarinat](https://github.com/ptr5000/clientview/blob/master/docs/tarinat.md)
- [Asennus- ja käyttöohje](https://github.com/ptr5000/clientview/blob/master/docs/kayttoohje.md)

# Testitunnukset

Sovellukseen luodaan automaattisesti seuraavat testitunnukset. Kaikkien salasana on '1':

    admin - admin tunnuksella voi hallita tuotteita ja vastaanottaa laskuja
    testco - testco firman laskutustunnus
    acme - acme firman laskutustunnus

## Sovelluksen rajoitteet ja puuttuvat ominaisuudet

Sovellus hieman oikoo tuotteen hinnan suhteen niin, että se määritellään 
tilaajan toimesta. Todellisuudessa olisi hyvä, että alihankkijat voisivat määritellä tuotteelle hinnan jonka perusteella sitten laskettaisiin ostotarjous tai vaihtoehtoisesti valittaisiin halvin toimittaja tarjouskilpailussa. 
Nyt yksinkertaistuksen vuoksi alihankkija valitaan suoraan eikä tarjous lähde "kaikille". Oletamme siis, että
alihankkijan kanssa on sovittu tilaus jo etukäteen esim. puhelimessa ja järjestelmä on enemmänkin vain ns. dokumentaation 
tekemiseen (PO:n ja laskun).


## Tietokanta

Tietokanta on kuvattu [kaaviossa](https://raw.githubusercontent.com/ptr5000/clientview/master/docs/clientview.png) tarkemmin.

[CREATE TABLE ja CREATE INDEX -lauseet](https://raw.githubusercontent.com/ptr5000/clientview/master/docs/sql.txt) 


### BaseAddress

Kysymyksiä vertaisarvioinnissa herätti odotetusti osoitetietojen levittely ympäri tauluja. Relaatiohenkisesti
ne voisi toki laittaa yhteen Address tauluun (mietinkin tätä vaihtoehtoa) ja viitata sitten siihen. 

Tässä vain ei ole mitään syytä siihen. Kyselyt yksinkertaistuvat kun osoitetietoja ei tarvitse hakea erikseen ja BaseAddress
abstraktoi asian mukavasti pois silmistä. Tämän lisäksi koodi yksinkertaistuu merkittävästi, esimerkiksi
model_formien tekeminen on helppoa. Pääsyy osoitetietojen useampaan kohtaan on kutienkin se, että halutaan 
pitää laskuihin liittyvä historiatieto tallessa. Tämä toki onnistuisi address -taululla mutta se ei olisi
suoraan selvää esimerkiksi toiselle koodaajalle joka saattaisi myöhemmin vahingossa muokata väärää riviä. 
Intuitiivisesti on selvää, että kun päivättyyn laskuun liittyy osoitetiedot invoice_sender -taulussa, ne tosiaan 
liittyvät juuri siihen kyseiseen päivättyyn laskuun. 

### Yhteenvetokyselyt

Tarina: "Pääkäyttäjän pitää pystyä hakemaan laskunäkymästä (valitsemalla alihankkijan nimen) myös kaikki alihankkijan tiedot, laskujen yhteissumma sekä käyttäjätunnuksen jolta alihankkija laskuttaa."

        SELECT  subcontractor.company_name, subcontractor.street, 
                subcontractor.city, subcontractor.state, 
                subcontractor.country, subcontractor.zip_code,
                account.username, SUM(invoice.amount)
                FROM subcontractor, invoice, account 
                WHERE subcontractor.id=:subcontractor_id 
                    AND invoice.subcontractor_id = subcontractor.id 
                    AND account.id = subcontractor.user_id 
                GROUP BY subcontractor.company_name, subcontractor.street, 
                            subcontractor.city, subcontractor.state,subcontractor.country, 
                            subcontractor.zip_code,account.username

Tarina "Pääkäyttäjän tulee pystyä hakemaan ketkä alihankkijat ovat myyneet mitäkin tuotetta (ja kuinka paljon yhteensä) jotta
voidaan selata helposti ketkä tuotetta toimittavat. Vastaa kysymykseen "ketkä toimittajat toimittavat tuotetta x"

        SELECT  subcontractor.id, 
                subcontractor.company_name, 
                SUM(product.price) 
                FROM product_order, orderinfo, product, subcontractor
                WHERE product_order.product_id = :product_id AND
                      product_order.order_id = orderinfo.id AND
                      product.id = product_order.product_id AND
                      subcontractor.id = orderinfo.subcontractor_id
                GROUP BY subcontractor.id

Koodista löytyy lisääkin myös ORM:lla tehtyjä yhteenvetoja. 

## Omat kokemukset

En ole aikaisemmin tehnyt SQLAlchemyllä tai Flaskilla. Django tosin on tuttu aika pitkältä ajalta. Tuntui vähän
turhauttavalta, kun Flaskista ei löytynyt kaikkea kivaa ja hyödyllistä mitä Djangosta löytyy. Mutta toisaalta,
palikoita voi vaihtaa ja lisätä oman harkinnan mukaan. Djangolla on ikävä tapa muuttaa aika paljonkin rakenteita, poistaa ja
siirrellä moduuleita ympäriinsä joten ehkä tällä tavalla saisi stabiilimman ympäristön. Sovelluksen rakennus oli kuitenkin
yhtä helppoa kuin Djangollakin. 











