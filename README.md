# PylonTechBattery
Lees data van die PylonTech battery deur die seriepoort van rekenaar



Gebruik die volgende bronne om die battery intervlak te programmeer:

Hier is die Duitse forum waar die PDF intervlakke vandaan kom:

 [https://www.photovoltaikforum.com/thread/118958-pylontech-us2000b-daten-%C3%BCber-konsole-rs232-auslesen/?t=118958&start=10](https://www.photovoltaikforum.com/thread/118958-pylontech-us2000b-daten-über-konsole-rs232-auslesen/?t=118958&start=10) 

Hier is 'n gebruiker wat 'n python intervlak geskryf het:

 https://github.com/celsworth/lxp-pylon-utils 

 https://www.navitron.org.uk/forum/index.php?topic=30961.0 


Hier is gebruiker wat javascript intervlak geskryf het.
 https://github.com/geeks-r-us/solar-sis



Bronne vanaf Duitse forum

 https://www.photovoltaikforum.com/thread/130061-pylontech-us2000b-daten-protokolle-programme/ 

 [https://www.photovoltaikforum.com/thread/118958-pylontech-us2000b-daten-%C3%BCber-konsole-rs232-auslesen/?t=118958&start=10](https://www.photovoltaikforum.com/thread/118958-pylontech-us2000b-daten-über-konsole-rs232-auslesen/?t=118958&start=10) 



## Pylontech RS-232 formaat van seriepoort

Hier is die ASCII tabel.  Die Pylontech stuur data in Heksadesimale getalle, maar dit gebruik die heksadesimale waarde van die ASCII tabel.

![asciifull](asciifull.gif)

Voorbeeld uit paragraaf 5 van RS-232 handleiding van Pylontech battery:

Stuur volgende string HEX getalle na die battery:

`7E 32 30 30 31 34 36 34 32 45 30 30 32 30 31 46 44 33 35 0D`

Dit beteken
`7E` - begin van data

`32 30` - 20 in ASCII dit is die weergawe (VER)

`30 31` - 30 is 'n 0 in ASCII in heks en 31 is 'n 1 in heks in ASCII, dus 01 dit is die battery nommer of ADR veld

`34 36` - 34 is 'n 4 in ASCII in heks en 36 is 'n 6 in heks in ASCII, dus 46 en dit is die kode vir litium ioon batterye (CID1)

`34 32` - 42 dit is die kode vir analoog inligting vanaf battery (CID2)

`45 30 30 32` - LENGTH dit is die lengte van die data wat met 'n komplekse berekening bereken word

`30 31` - INFO Dit is die ASCII vir 01 wat beteken jy vra vir battery 1 se inligting

`46 44 33 35` - CHECKSUM  Dit is die toets som vir hierdie string data

`0D` - dit is die einde van die data oftewel "Carriage return"

Kry dan terug:

`7E 32 30 30 31 34 36 30 30 43 30 36 45 31 31 30 31 30
46 30 44 34 35 30 44 34 34 30 44 34 35 30 44 34 34 30 44 34 35 30 44 34
34 30 44 33 45 30 44 34 35 30 44 34 41 30 44 34 41 30 44 34 42 30 44 34
41 30 44 34 41 30 44 34 41 30 44 34 41 30 35 30 42 43 33 30 42 43 33 30
42 43 33 30 42 43 44 30 42 43 44 30 30 30 30 43 37 32 35 42 46 36 38 30
32 43 33 35 30 30 30 30 32 45 35 35 33 0D`

Die oorblywende energie in die battery word gegee deur:

`42 46 36 38`

in die string wat teruggestuur word hierbo.  Die volledige analise van die string hierbo word gegee in die Pylontech RS232 handleiding in paragraaf 5.

Die getalle hierbo is die heksadesimale waardes van die ASCII tabel.  Dus is `42`eintlik die string `B.`  Net so is die hele string dan:  `BF68`

Hierdie string is 'n heksadesimale getal wat nou teruggelei kan word na 'n desimale getal.  `BF68H` waar `H`  die heksadesimale getal beteken, is `49000`.  Hierdie getal is die waarde in mAh van die battery.  Dus om die orige energie in kWh te bereken word die volgende berekening gedoen:

$Energie = \frac{49000mAh}{1000} \times 48V = 2352W = 2.352kW$

Hierdie berekening neem aan dit is 'n 48V battery.

Dus is die lading persentasie (die "State of Charge" of SOC) gelyk aan:

$SOC = \frac{2.352W}{2400W} = 0.98 = 98\%$

Hierdie berekening neem aan dit is 'n 2.4kWh battery oftewel die Pylontech US2000.


## Voorbeeld berekeninge van die toetssom en lengte

Doen 'n voorbeeld berekening van die LENID en die CHKSU van die analoog opdrag.

### Voorbeeld uit protokol met 1 battery

Die volgende opdrag word na die battery gestuur:

`7E 32 30 30 31 34 36 34 32 45 30 30 32 30 31 46 44 33 35 0D`

Die belangrike items vir hierdie berekening is as volg:

`45 30 30 32` - LENGTH (lengte van die data)

`30 31` - INFO Dit is die ASCII vir 01 wat beteken jy vra vir battery 1 se inligting

`46 44 33 35` - CHECKSUM  Toetssom

Die protokol van die Pylontech battery noem in tabel A7 dat die lengte datagreep in 4 ASCII syfers verdeel word om die data te stuur.  Die lengte van die data word hier gegee as twee of 002 (30H 30H 32H).  Dus is die lengte van die data in die INFO kolom gelyk aan LENID/2 = 2/2 = 1 (sien tabel A1 in protokol).
Die LCHKSUM kan nou as volg bereken word vir die waarde van 002 (30H 30H 32H).
Verander eers hierdie getalle in binere waardes:  Dus word 002:  0000 0000 0010 in biner.
Die hele string is een getal.  Met ander woord die leidende nulle word weggegooi, maar die 3 groepe getalle werk as een.  As nog 'n voorbeeld, indien die getal 18 in desimaal in hierdie geval sal geskryf word as die binere getal:  10010, maar in die bostaande formaat van groepe van 4 karakters word dit geskryf as 0000 0001 0010.  En hierdie drie groepe word voorgestel deur kommunkasie wat heksadesimale getalle aanstuur.

Nou om die LCHKSUM vir die waarde van 002 te bereken neem jy die binere getall vir die 3 groepe wat die getal opmaak en tel hulle bymekaar:
    0000B + 0000B + 0010B = 0010B (B staan vir biner)
    
Neem nou die modulus van 16 (deel dit deur 16 en vat die res) wat 0010B bly.  Dit word dan bis gewys omgeruil wat dit 1101B maak.  Dan tel 1 by om dit 1110B te maak.  Skakel nou 1110B om na heksadesimaal en jy kry E in heksadesimaal (oftewel 14 in desimaal).  Hierdie waarde van E in die ASCII tabel is 45.

Dus word die waarde van LENID of LENGTH nou:
    
'45 30 30 32'



### Voorbeeld met paralelle battery

Dan doen die berekening oor vir die geval van 'n parallelle battery.
Die parallelle batery inligting word gevra in die INFO veld.
As jy vir FF in die INFO veld vra, kry jy alle inligting.
As jy vir 'n nommer soos bv. 02 vra, kry jy battery 2 se inligting.
Doen die LENID en CHKSUM berekening vir bogenoemede twee gevalle
en skryf die opdrag uit.
Toets dit dan. 
Wys hoe die berekening gedoen word.



### Battery instellings vir die Pylontech battery op die Axpert inverter

Die volgende instellings is gedoen vir die Axpert om die Pylontech battery in staat te stel om meer leeg te loop.  Dit stel die battery in staat om meer van die sonkrag te benut.  Dit verskil van die standaard Pylontech instellings vir die Axpert.  Dus moet dit gesien word as meer onveilig (die battery mag leegloop met hierdie instellings wat ongewens is).

Axpert Program nommer:

Program 02 - Stel na N*20A, N = aantal batterye

Program 05 - USE  

Program 12 - 46V  

Program 13 - 48V

Program 29 - 46V

Belangrike nota:  Met 'n stelsel waar daar baie panele is kan program 02 eerder na die volgende gestel word:  N*20A - 10A.  Dit is meer geskik want daar is ondervind dat die DC skakelaar uitklink a.g.v. baie groot stroomwaardes wat die battery nie kan absorbeer op kort kennisgewing nie.  Indien die laaistroom laer gestel word soos laasgenoemde, verdwyn die probleem.

### Task: Display Detected System’s Serial Support

 Simply run dmesg command

 `$ dmesg | grep tty`
