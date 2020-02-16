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

![asciifull](/home/niel/gitclonetemp/PylonTechBattery/asciifull.gif)

Voorbeeld uit paragraaf 5 van RS-232 handleiding van Pylontech battery:

Stuur volgende string HEX getalle na die battery:

`7E 32 30 30 31 34 36 34 32 45 30 30 32 30 31 46 44 33 35 0D`

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

### Task: Display Detected System’s Serial Support

 Simply run dmesg command

 `$ dmesg | grep tty`