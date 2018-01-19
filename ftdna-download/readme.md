
ftdna-download.py

Komentoriviohjelma, jolla voi ladata tiedostoja automaattisesti Family Tree DNA:sta.

Käyttää Seleniumia (http://www.seleniumhq.org/) ohjaamaan selainta (esim. Chrome, Firefox). Myös vastaava webdriver (chromedriver tms) pitää asentaa.

Lataa ftdna-download.py johonkin hakemistoon. Webdriver-binääri (esim. chromedriver) tulee tallettaa samaan hakemistoon.

<pre>
usage: python2 ftdna-download.py [-h] [--kit KIT] [--all] [--ff] [--cb] [--37] 
                [--passwords PASSWORDS] [--driver DRIVER]
                [--downloads-folder DOWNLOADS_FOLDER] [--quiet]

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
  --quiet
</pre>

Selain tulee konfiguroida niin, että se tekee lataukset automaattisesti hakemistoon Downloads eikä kysy mihin talletetaan. 

Ohjelma lukee tiedostosta "passwords.txt" käytettävät tunnukset ja salasanat. Tiedostossa tulee olla yksi rivi per käyttäjä, muodossa

<pre>
  kitnum password
</pre>

Oletuksena ohjelma käynnistää Chrome-selaimen ja hakee tiedostot
  
<pre>  
nnnnnn_Family_Finder_Matches_yyyymmdd.csv
nnnnnn_Chromosome_Browser_Results__yyyymmdd.csv
nnnnnn_Autosomal_o37_Results_yyyymmdd.csv.gz
</pre>

Jos haluaa hakea vain jonkin näistä, voi antaa parametrin --ff, --cb tai --37, jolloin haetaan vain vastaava tiedosto.
Samoin jos haluaa vain jonkin kitin tiedostot, voi kit-numeron antaa parametrissa --kit

Ohjelma toimii vain Python 2:lla, sillä Selenium tukee vain sitä.