import logging


class PylonPacket:
    
    def __init__(self):
        self.header = bytearray(6)
        self.info = bytearray()
        self.checksum = bytearray(2)
        self.VER=0x20
        self.ADR=0x02

    @property
    def VER(self):
        return self.header[0]

    @VER.setter
    def VER(self, value):
        self.header[0] = value

    @property
    def ADR(self):
        return self.header[1]

    @ADR.setter
    def ADR(self, value):
        self.header[1] = value

    @property
    def CID1(self):
        return self.header[2]

    @CID1.setter
    def CID1(self, value):
        self.header[2] = value

    @property
    def CID2(self):
        return self.header[3]

    @CID2.setter
    def CID2(self, value):
        self.header[3] = value

    @property
    def LENGTH(self):
        return (((self.header[4] & 0x0F) << 8) | self.header[5])

    @LENGTH.setter
    def LENGTH(self, value):
        if value>0xfff or value<0: raise OverflowError("Invalid length")
        sum = (value & 0x000F) + ((value >> 4) & 0x000F) + ((value >> 8 ) & 0x000F);
        sum = sum % 16;
        sum = ~sum;
        sum = sum + 1;
        val = (sum << 12) + value;
        self.header[5] = (val & 0xff)
        self.header[4] = (val>>8) & 0xff
    

    @property
    def INFO(self):
        return self.info

    @INFO.setter
    def INFO(self, value):
        self.info = value

    @property
    def CHKSUM(self):
        return self.checksum[0:2]

    @CHKSUM.setter
    def CHKSUM(self, value):
        self.checksum[0:2] = value

    def UpdateChecksum(self):
        sum=0
        for char in bytes(self.header).hex().upper():
            sum+=ord(char)
        for v in bytes(self.info).hex().upper():
            sum+=ord(v)
        sum=sum%65536
        sum=~sum
        sum=sum+1
        self.checksum[0]=(sum >>8) & 0xff
        self.checksum[1]=sum & 0xff


    def GetAsciiBytes(self):
        self.UpdateChecksum()
        ret=bytearray()
        ret.extend(self.header)
        ret.extend(self.info)
        ret.extend(self.checksum)
        rh='~'+ret.hex().upper()+"\r"
        logging.debug("Encoded sentence is %s",rh)
        return rh.encode()

    def Parse(ascii, packet_type):
        if (len(ascii)==0): return None
        #logging.debug("Value to decode is %s",ascii)
        if ascii[0] != 0x7E or ascii[-1] != 0x0D:
            raise ValueError("Invalid packet format")
        content=ascii[1:-1].decode()
        logging.debug("Content of packet: %s",content)
        bdata = bytes.fromhex(content)
        
        pret = packet_type()
        for i in range(0,len(pret.header)):
            pret.header[i] = bdata[i]
        if  pret.LENGTH>0:
            pret.info=bdata[6:-2]
            logging.debug("Info content is %s", pret.info.hex())
        else:
            pret.info=bytearray()
        pret.UpdateChecksum()
        if pret.checksum[0]!=bdata[-2] or pret.checksum[1]!=bdata[-1]:
            logging.error("Invalid checksum!")
            raise ValueError("Invalid checksum")
        pret.PostParse()
        return pret

    def PostParse(self):
        pass

    def GetInt2(self, idx):
        val=self.info[idx]<<8 | self.info[idx+1]
        return val

    def GetInt2Complement(self, idx):
        val=self.info[idx]<<8 | self.info[idx+1]
        if (val & 0x8000)==0x8000:
            val = val - 0x10000
        return val

    def __str__(self, **kwargs):
        return "VER: 0x%02x, ADR: 0x%02x, CID1: 0x%02x, CID2: 0x%02x, LENGTH: %s, len(INFO): %s, CHKSUM: 0x%02X%02X"%(self.VER,self.ADR,self.CID1,self.CID2,self.LENGTH,len(self.INFO),self.CHKSUM[0],self.CHKSUM[1])

class PPGetVersionInfo(PylonPacket):
    def __init__(self):
        super().__init__()
        self.CID1=0x46
        self.CID2=0x4F

class PPVersionInfo(PylonPacket):
    pass

class PPGetManufacturerInfo(PylonPacket):
    def __init__(self):
        super().__init__()
        self.CID1=0x46
        self.CID2=0x51

class PPManufacturerInfo(PylonPacket):
    @property
    def DeviceName(self):
        return (self.info[0:10]).decode().strip()

    @property
    def SoftwareVersion(self):
        return self.info[10:13]

    @property
    def ManufacturerName(self):
        return (self.info[12:]).decode().strip()

    def __str__(self, **kwargs):
        #print(int(self.SoftwareVersion[1]))
        return super().__str__(**kwargs)+("\r\n>  DeviceName: %s, SoftwareVersion %s.%s, ManufacturerName: %s"%(self.DeviceName,'?','?',self.ManufacturerName))


class PPGetAnalogValue(PylonPacket):

    def __init__(self):
        super().__init__()
        self.info=bytearray(1)
        self.LENGTH=0x02
        self.CID1=0x46
        self.CID2=0x42
        

    @property
    def Command(self):
        return self.info[0]

    @Command.setter
    def Command(self, value):
        self.info[0] = value
    
    def __str__(self, **kwargs):
        return super().__str__(**kwargs)+(", Command: %s"%(self.Command))


class PPAnalogValue(PylonPacket):

    def __init__(self):
        super().__init__()
        self.voltages=[]
        self.temperatures=[]

    @property
    def CellsCount(self):
        return self.info[2]

    @property
    def CellVoltages(self):
        return self.voltages

    @property
    def TemperaturesCount(self):
        idx=(self.CellsCount*2)+3
        return self.info[idx]

    @property
    def Temperatures(self):
        return self.temperatures

    @property
    def TotalCurrent(self):
        return self.GetInt2Complement(-11)/10.0 

    @property
    def TotalVoltage(self):
        return self.GetInt2(-9)/1000.0 

    @property
    def RemainingCapacity(self):
        return self.GetInt2(-7)/1000.0 

    @property
    def Quantity(self):
        return self.info[-5]

    @property
    def TotalCapacity(self):
        return self.GetInt2(-4)/1000.0  

    @property
    def Cycles(self):
        return self.GetInt2(-2) 

    def PostParse(self):
        logging.debug("Post processing parsed data %s",self.info.hex())
        self.voltages=[]
        self.temperatures=[]
        for v in range(0,self.CellsCount):
            cv=self.GetInt2(3+(2*v))/1000.0
            logging.debug("Voltage ",v,cv)
            self.voltages.append(cv)
        
        idx=(self.CellsCount*2)+3
        for t in range(0,self.TemperaturesCount):
            tv=self.GetInt2Complement(idx+1+(2*t))
            tv=(tv-2731)/10.0
            logging.debug("Temperature %s: %s",v,tv)
            self.temperatures.append(tv)
    
    def __str__(self, **kwargs):
        ret=super().__str__(**kwargs)
        ret+=("\r\n>  CellsCount: %s, TemperaturesCount: %s"%(self.CellsCount, self.TemperaturesCount))
        ret+=("\r\n>  TotalCurrent: %.3f, TotalVoltage: %.3f, RemainingCapacity: %.3f, P: %.2f"%(self.TotalCurrent, self.TotalVoltage, self.RemainingCapacity,(self.TotalCurrent*self.TotalVoltage)))
        ret+=("\r\n>  Quantity: %s, TotalCapacity: %s, Cycles: %s"%(self.Quantity, self.TotalCapacity, self.Cycles))
        ret+=("\r\n>  CellVoltages: %s"%(self.CellVoltages))
        ret+=("\r\n>  Temperatures: %s"%(self.Temperatures))
        return ret

class PPGetSystemParameter(PylonPacket):
    def __init__(self):
        super().__init__()
        self.CID1=0x46
        self.CID2=0x47

class PPSystemParameter(PylonPacket):
    @property
    def INFOFLAG(self):
        return self.info[0]

    @property
    def UnitCellVoltage(self):
        return self.GetInt2(1)/1000.0

    @property
    def UnitCellLowVoltage(self):
        return self.GetInt2(3)/1000.0

    @property
    def UnitCellUnderVoltage(self):
        return self.GetInt2(5)/1000.0

    #TODO: Doplnit dalsi neuzitecne property
    def __str__(self, **kwargs):
        return super().__str__(**kwargs)+("\r\n>  FLAG: %s, UnitCellVoltage: %s, UnitCellLowVoltage %s, UnitCellUnderVoltage: %s"%(bin(self.INFOFLAG), self.UnitCellVoltage,self.UnitCellLowVoltage,self.UnitCellUnderVoltage))


class PPGetAlarmInformation(PylonPacket):
    def __init__(self):
        super().__init__()
        self.CID1=0x46
        self.CID2=0x44
        self.info=bytearray(1)
        self.LENGTH=0x02
 
    @property
    def Command(self):
        return self.info[0]

    @Command.setter
    def Command(self, value):
        self.info[0] = value
    
    def __str__(self, **kwargs):
        return super().__str__(**kwargs)+(", Command: %s"%(self.Command))

class PPAlarmInformation(PylonPacket):
    pass


class PPGetChargeManagementInformation(PylonPacket):
    def __init__(self):
        super().__init__()
        self.CID1=0x46
        self.CID2=0x92
        self.info=bytearray(1)
        self.LENGTH=0x02
 
    @property
    def Command(self):
        return self.info[0]

    @Command.setter
    def Command(self, value):
        self.info[0] = value
    
    def __str__(self, **kwargs):
        return super().__str__(**kwargs)+(", Command: %s"%(self.Command))

class PPChargeManagementInformation(PylonPacket):

    @property
    def VoltageUpLimit(self):
        return self.GetInt2(1)/1000.0

    @property
    def VoltageDownLimit(self):
        return self.GetInt2(3)/1000.0

    @property
    def MaxChargeCurrent(self):
        return self.GetInt2Complement(5)/1.0

    @property
    def MaxDischargeCurrent(self):
        return self.GetInt2Complement(7)/1.0

    @property
    def Status(self):
        return self.info[9]

    def __str__(self, **kwargs):
        print(self.info.hex())
        return super().__str__(**kwargs)+("\r\n>  VoltageUpLimit: %s, VoltageDownLimit: %s, MaxChargeCurrent: %s, MaxDischargeCurrent: %s, Status: %s"%(self.VoltageUpLimit,self.VoltageDownLimit,self.MaxChargeCurrent,self.MaxDischargeCurrent,self.Status))



class PPGetSeriesNumber(PylonPacket):
    def __init__(self):
        super().__init__()
        self.CID1=0x46
        self.CID2=0x93
        self.info=bytearray(1)
        self.LENGTH=0x02
 
    @property
    def Command(self):
        return self.info[0]

    @Command.setter
    def Command(self, value):
        self.info[0] = value
    
    def __str__(self, **kwargs):
        return super().__str__(**kwargs)+(", Command: %s"%(self.Command))

class PPSeriesNumber(PylonPacket):
    
    @property
    def SeriesNumber(self):
        return self.info[1:].decode()


    def __str__(self, **kwargs):
        return super().__str__(**kwargs)+("\r\n> Series Number: %s"%(self.SeriesNumber))

class PPTurnOff(PylonPacket):
    def __init__(self):
        super().__init__()
        self.CID1=0x46
        self.CID2=0x95
        self.info=bytearray(1)
        self.LENGTH=0x02
 
    @property
    def Command(self):
        return self.info[0]

    @Command.setter
    def Command(self, value):
        self.info[0] = value

    def __str__(self, **kwargs):
        return super().__str__(**kwargs)+(", Command: %s"%(self.Command))


class PPTurnOffReply(PylonPacket):
    pass