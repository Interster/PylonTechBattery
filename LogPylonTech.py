from PylonPara import *

# Log parameters
monsterfrekwensie = 30 # [sekondes]
totalesekondes = 2*60 #24*60*60 #2*60 #24*60*60 # [sekondes]

# Opdrag vanaf paragraaf 5 in seriepoort handleiding:  Lees analoog data
#bytestosend = '7E3230303134363432453030323031464433350D'
# Parallelle lees opdrag
bytestosend = '7E3230303134363432453030324646464430410D'

begintyd = datetime.datetime.now()

# Maak leer oop
leer = open('PylonTech_' + str(datetime.date.today()) + '.log', 'w')
leer.write('DatumTyd, Stroom 1 mA_100, Spanning 1 mV, Energie oor 1 mAh, Totale energie 1 mAh, Siklusse 1, Stroom 2 mA_100, Spanning 2 mV, Energie oor 2 mAh, Totale energie 2 mAh, Siklusse 2\n')

while (datetime.datetime.now() - begintyd).seconds < totalesekondes:
    # Stuur data 1200 baud.  Dit moet eers teen hierdie spoed gestuur word
    with serial.Serial('/dev/ttyUSB0', 1200, timeout=5.0) as ser:
        x = ser.write(unhexlify(bytestosend)) # Stuur opdrag na die battery
        try:
            uitstring = ser.read(1000)
            a = uitstring.hex()
        except:
            a = ''
    
    print('Uitset:')
    print(a)
    
    # Log data na leer
    if a == '':
        print('Leesfout van battery by hooflus - probeer weer')
    else:
        if 1==1: #berekenToetssom(a):
            skryfnaleer = str(datetime.datetime.now()) + ',' + skryfLogLynBattery(a)
            leer.write(skryfnaleer)
            leer.write('\n')
            print(skryfnaleer)
        else:
            print('Toetssom faal')
        
    time.sleep(monsterfrekwensie - 5)

leer.close()

