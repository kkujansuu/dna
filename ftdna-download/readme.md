
ftdna-download.py

Komentoriviohjelma, jolla voi ladata tiedostoja automaattisesti Family Tree DNA:sta.

Käyttää Seleniumia (http://www.seleniumhq.org/, https://pypi.python.org/pypi/selenium) ohjaamaan selainta (esim. Chrome, Firefox, Opera, Internet Explorer). Myös vastaava webdriver (chromedriver tms) pitää asentaa.

<h4>Asennus:</h4>
Lataa ftdna-download.py johonkin hakemistoon. Webdriver-binääri (chromedriver, geckodriver, operadriver, IEDriverServer.exe) tulee tallettaa samaan hakemistoon.

<h4>Käyttö:</h4>
<pre>
sage: ftdna-download.py [-h] [--kit KIT] [--all] [--ff] [--cb] [--37]
                         [--passwords PASSWORDS] [--driver DRIVER]
                         [--downloads-folder DOWNLOADS_FOLDER]
                         [--browser {chrome,firefox,opera,ie}] [--quiet]

optional arguments:
  -h, --help            show this help message and exit
  --kit KIT
  --all
  --ff
  --cb
  --37
  --passwords PASSWORDS
  --driver DRIVER
  --downloads-folder DOWNLOADS_FOLDER
  --browser {chrome,firefox,opera,ie}
  --quiet

</pre>

Selain tulee konfiguroida niin, että se tekee lataukset automaattisesti hakemistoon Downloads eikä kysy mihin talletetaan. 

Ohjelma lukee tiedostosta "passwords.txt" käytettävät tunnukset ja salasanat. Tiedostossa tulee olla yksi rivi per käyttäjä, muodossa

<pre>
  kitnum password
</pre>

Oletuksena ohjelma käynnistää Chrome-selaimen ja hakee kaikille passwords.txt-tiedostossa mainituille käyttäjille tiedostot
  
<pre>  
nnnnnn_Family_Finder_Matches_yyyymmdd.csv
nnnnnn_Chromosome_Browser_Results__yyyymmdd.csv
nnnnnn_Autosomal_o37_Results_yyyymmdd.csv.gz
</pre>

Jos haluaa hakea vain jonkin näistä, voi antaa parametrin --ff, --cb tai --37, jolloin haetaan vain vastaava tiedosto.
Samoin jos haluaa vain jonkin kitin tiedostot, voi kit-numeron antaa parametrissa --kit

