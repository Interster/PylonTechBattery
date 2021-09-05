import datetime
import time
from binascii import unhexlify
import serial

def twos_complement(hexstr,bits):
    # Verander die heksadesimale getal na 'n heelgetal met 'n teken oftewel 'n "signed integer"
    # In 'n n-greep twee komplement getallevoorstelling, het die grepe die waardes:
    # greep 0 = 2^0
    # bit 1 = 2^1
    # bit n-2 = -2^(n-2)
    # bit n-1 = -2n-1
    #
    # Maar greep n-1 het waarde 2^(n-1) wanneer dit geen teken het nie, dus is die getal 2^n te hoog.
    # Trek dus 2^n af indien greep n-1 'n waarde het

    try:
        value = int(hexstr,16)
            
        if value & (1 << (bits-1)):
            value -= 1 << bits
    
        return value
    except:
        value = 'fout'
        print('Leesfout van battery by twoscomplement - probeer weer')
        
        return value

def wysHeksString(insetstring):
    print('Heksadesimale ASCII waarde')
    print(insetstring)
    print('Heksadesimale string')
    getalinheks = bytearray.fromhex(insetstring).decode()
    print(getalinheks)
    print('Desimale string')
    getaluit = int(getalinheks, 16)
    print(getaluit)
    
    return getaluit

def uitsetGetalHeksString(insetstring):
    try:
        # Neem die insetstring van die battery ontvang en kry die ASCII waarde daarvan
        getalinheks = bytearray.fromhex(insetstring).decode()
        # getalinheks word nou omgeskakel na 'n desimale waarde wat gebruik kan word.
        uitsetgetal = int(getalinheks, 16)
    except:
        uitsetgetal = 'fout'
        print('Leesfout van battery by fromhex - probeer weer')

    return uitsetgetal

def uitsetGetalHeksStringSignInt(insetstring):
    try:
        # Neem die insetstring van die battery ontvang en kry die ASCII waarde daarvan
        getalinheks = bytearray.fromhex(insetstring).decode()
        # getalinheks word nou omgeskakel na 'n desimale waarde wat gebruik kan word.
        uitsetgetal = twos_complement(getalinheks, 16)
    except:
        uitsetgetal = 'fout'
        print('Leesfout van battery by fromhex - probeer weer')
    
    return uitsetgetal


def skryfLogLynBattery(leesvanbattery):
    a = leesvanbattery
    
    #Stroom in milliAmpere/100.  Dus vermenigvuldig met 100 en deel deur 1000 om Ampere te kry
    stroom = uitsetGetalHeksStringSignInt(a[202:210])
    
    #Spanning in milliVolt van hele battery
    spanning = uitsetGetalHeksString(a[210:218])
    #Oorblywende energie in battery
    energieOor = uitsetGetalHeksString(a[218:226])
    # Totale energie in battery
    energietotaal = uitsetGetalHeksString(a[230:238])
    # Siklusse
    siklusse = uitsetGetalHeksString(a[238:246])
    
    uitsetloglyn = str(stroom) + ',' + str(spanning) + ',' + str(energieOor) + ',' + str(energietotaal) + ',' + str(siklusse)
    
    
    #Stroom in milliAmpere/100.  Dus vermenigvuldig met 100 en deel deur 1000 om Ampere te kry
    stroom2 = uitsetGetalHeksStringSignInt(a[438:446])
    
    #Spanning in milliVolt van hele battery
    spanning2 = uitsetGetalHeksString(a[446:454])
    #Oorblywende energie in battery
    energieOor2 = uitsetGetalHeksString(a[454:462])
    # Totale energie in battery
    energietotaal2 = uitsetGetalHeksString(a[466:474])
    # Siklusse
    siklusse2 = uitsetGetalHeksString(a[474:482])
    
    
    uitsetloglyn = uitsetloglyn + str(stroom2) + ',' + str(spanning2) + ',' + str(energieOor2) + ',' + str(energietotaal2) + ',' + str(siklusse2)
    
    return uitsetloglyn

def ToetsSomTeksHeks(insetstring):
    toetssomgetal = ''
    
    for i in range(0,len(insetstring),2):
        toetssomgetal = toetssomgetal + chr(int(insetstring[i:i+2],16))
    
    return toetssomgetal

def berekenToetssom(seriestring):
    berekenstring = seriestring[2:-10]
    #print(berekenstring) 
    toetssomstring = seriestring[-10:-2]
    #print(toetssomstring)
    
    somtotaal = 0
    for i in range(0, len(berekenstring) - 1, 2):
        somtotaal = somtotaal + int(berekenstring[i:i + 2], 16)
        
    #print("Somtotaal: " + str(somtotaal))
    
    sommod = somtotaal % 65536
    
    somtotaalbin = bin(sommod)
    # Doen bisgewyse omgekeerde operasie op die binere string
    somtotaalbininvert = somtotaalbin[2:]
    # Maak dit string van 16 lengte
    somtotaalbininvert = (16 - len(somtotaalbininvert))*"0" + somtotaalbininvert
    
    
    somtotaalbininvert = somtotaalbininvert.replace("1","2")
    somtotaalbininvert = somtotaalbininvert.replace("0","1")
    somtotaalbininvert = somtotaalbininvert.replace("2","0")
        
    somtotaalinvert = int(somtotaalbininvert, 2)
    somtotaalinvert = somtotaalinvert + 1
    
    CHKSMvergelyk = ToetsSomTeksHeks(toetssomstring)
    #print('Toetssom is ' + CHKSMvergelyk)
    
    CHKSM = hex(somtotaalinvert)
    CHKSM = CHKSM[2:].upper()
    #print('Toetssom bereken ' + CHKSM)
    
    #print('Suksesvol:')
    #print(CHKSM == CHKSMvergelyk)
    
    return CHKSM == CHKSMvergelyk

