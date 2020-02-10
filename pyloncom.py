import sys
import pylonpacket
import logging
import serial
import time



class PylonCom:
    PORT = "/dev/ttyUSB0"
    BAUD = 115200
    
    def __init__(self):
        self.sp = serial.Serial(PylonCom.PORT,PylonCom.BAUD,timeout=0.5)

    def GetReply(self, request, reply_type):
        self.sp.write(request.GetAsciiBytes())
        line = bytearray()
        while True:
            c = self.sp.read(1)
            if c:
                line.extend(c)
                if c[0] == 0x0D:
                    break
            else:
                break
        logging.debug("Received sentence %s",line)
        preply = pylonpacket.PylonPacket.Parse(line, reply_type)
        return preply

    def close(self):
        self.sp.close()

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    pc = PylonCom()


    #for adr in range(0,255):
    #    ppIn = pylonpacket.PPGetVersionInfo()
    #    ppIn.ADR=adr
    #    ppOut=pc.GetReply(ppIn, pylonpacket.PPVersionInfo)
    #    if ppOut: print("Get protocol version reply:",ppOut)
    #return
    


    #ppIn=pylonpacket.PPGetManufacturerInfo()
    #print("Get manufacturer info:",ppIn)
    #ppOut=pc.GetReply(ppIn, pylonpacket.PPManufacturerInfo)
    #print("Get manufacturer info reply:",ppOut)

    ppIn = pylonpacket.PPGetSystemParameter()
    print("Get system parameter:",ppIn)
    ppOut = pc.GetReply(ppIn, pylonpacket.PPSystemParameter)
    print("Get system parameter reply:",ppOut)

    ppIn = pylonpacket.PPGetSeriesNumber()
    ppIn.Command = 0x02
    print("Get series number:",ppIn)
    ppOut = pc.GetReply(ppIn, pylonpacket.PPSeriesNumber)
    print("Get series number reply:",ppOut) #,ppOut.info.hex())

    while True:
      for adr in range(2,3):
        print("Conectiong to addr",adr)
        ppIn = pylonpacket.PPGetChargeManagementInformation()
        ppIn.Command = adr
        ppIn.ADR = adr
        #print("Get charge info:",ppIn)
        ppOut = pc.GetReply(ppIn, pylonpacket.PPChargeManagementInformation)
        print("Get charge info reply:",ppOut)
  
    #return

        ppIn = pylonpacket.PPGetAnalogValue()
        ppIn.Command = adr
        ppIn.ADR = adr
        #print("Get analog:",ppIn)
        ppOut = pc.GetReply(ppIn, pylonpacket.PPAnalogValue)
        print("Get analog reply:",ppOut)
      
      print("")
      time.sleep(2)

    #ppIn=pylonpacket.PPGetChargeManagementInformation()
    #ppIn.Command=0x02
    #print("Get charge info:",ppIn)
    #ppOut=pc.GetReply(ppIn, pylonpacket.PPChargeManagementInformation)
    #print("Get charge info reply:",ppOut)
      

    ppIn = pylonpacket.PPGetAlarmInformation()
    ppIn.Command = 0x02
    print("Get alarm info:",ppIn)
    ppOut = pc.GetReply(ppIn, pylonpacket.PPAlarmInformation)
    print("Get alarm info reply:",ppOut) #,ppOut.info.hex())

    
    ppIn = pylonpacket.PPTurnOff()
    ppIn.Command = 0x02
    print("Turn off:",ppIn)
    ppOut = pc.GetReply(ppIn, pylonpacket.PPTurnOffReply)
    print("Turn off reply:",ppOut)
    

if __name__ == "__main__":
    root = logging.getLogger()
    #root.setLevel(logging.DEBUG)
    main(sys.argv[1:])
