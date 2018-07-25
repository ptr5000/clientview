# ClientView kurssille Tsoha-18 (loppukesä)

Kyseessä on sovellus joka pohjautuu oikeaan tarpeeseen. Eräs legacy palvelu
poistuu käytöstä ja sillä on riippuvuuksia useisiin kirjastoihin ja palvelimiin. Sen ajaminen tuotantoserverien sammuttamisen jälkeen on todella vaikeaa ja ikävää (erityisesti esim. 10v päästä). Palvelu sisältää kymmenien taulujen lisäksi myös tietoja alihankkijoista (osoitetiedot, paikalliset VAT-koodit jne) sekä laskuja. Tämän sovelluksen idea on tarjota näkymä asiakasrekisteriin, tilauksiin, alihankkijoiden tietoihin ja järjestelmässä oleviin laskuihin mikäli esim. verottaja tarvitsee tarkempia tietoja joskus. 

CRUD näkymät tulevat tämän kurssin puitteissa alihankkijatiedolle, työtilaukselle, laskuille ja niiden vastaanottajille. Lisäksi tulee kirjautuminen ja käyttäjänhallinta jolla erotellaan lähinnä pääkäyttäjä ja alihankkija (laskuttaja). Kanta on puhtaasti tähän uuteen sovellukseen/kurssiin suunniteltu koska legacy kanta pitää sisällään myös paljon "turhaa" tietoa mitä voidaan esittää yksinkertaisemmin.

# [Demo](https://tsoha-clientview.herokuapp.com)


- [Tietokantakaavio](https://raw.githubusercontent.com/ptr5000/clientview/master/docs/clientview.png)
- [Käyttäjätarinat](https://github.com/ptr5000/clientview/blob/master/docs/tarinat.md)


