from binascii import unhexlify
import serial

bytestosend = '7E3230303134363432453030323031464433350D'

with serial.Serial('/dev/ttyUSB0', 1200, timeout=5.0) as ser:
    x = ser.write(unhexlify(bytestosend)) # Stuur opdrag na die battery
    uitstring = ser.read(1000)
    a = uitstring.hex()

print('Hier is uitset')
print(a)