# Seriepoorte in linux en python

## Inleiding

Die RS-232 is die ouer seriepoort formaat en RS-485 is die meer moderne formaat (kan langer kabels ondersteun en meer toestelle as een op dieselfde kabel).



## Python serial

Open 'n poort in python:

Open port at “9600,8,N,1”, no timeout: 

```python
>>> import serial
>>> ser = serial.Serial('/dev/ttyUSB0')  # open serial port
>>> print(ser.name)         # check which port was really used
>>> ser.write(b'hello')     # write a string
>>> ser.close()             # close port
```
https://pythonhosted.org/pyserial/shortintro.html

## How To Check and Use Serial Ports Under Linux

Linux offers various tools. Linux uses ttySx for a serial port device name. For example, COM1 (DOS/Windows name) is ttyS0, COM2 is ttyS1 and so on. 



### Task: Display Detected System’s Serial Support

 Simply run dmesg command

 `$ dmesg | grep tty`

```bash
[   37.531286] serial8250: ttyS0 at I/O 0x3f8 (irq = 4) is a 16550A
[   37.531841] 00:0b: ttyS0 at I/O 0x3f8 (irq = 4) is a 16550A
[   37.532138] 0000:04:00.3: ttyS1 at I/O 0x1020 (irq = 18) is a 16550A
```
### setserial command

setserial is a program designed to set and/or report the configuration information associated with a serial port. This information includes what I/O port and IRQ a particular serial port is using, and whether or not the break key should be interpreted as the Secure Attention Key, and so on. Just type the following command: 

 `$ setserial -g /dev/ttyS[0123]`

 Output: 

```bash
/dev/ttyS0, UART: 16550A, Port: 0x03f8, IRQ: 4
/dev/ttyS1, UART: 16550A, Port: 0x1020, IRQ: 18
/dev/ttyS2, UART: unknown, Port: 0x03e8, IRQ: 4
/dev/ttyS3, UART: unknown, Port: 0x02e8, IRQ: 3
```
setserial with -g option help to find out what physical serial ports your Linux box has.