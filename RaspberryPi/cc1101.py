import spidev

class CC1101:
    #-------------Comand strobes--------------
    SRES = 0x30
    SFSTXON = 0x31
    SXOFF = 0x32
    SCAL = 0x33
    SRX = 0x34 
    STX = 0x35
    SIDLE = 0x36
    SWOR = 0x38 
    SPWD = 0x39
    SFRX = 0x3A
    SFTX = 0x3B
    SWORRST = 0x3C
    SNOP = 0x3D

    #-------------Configuration Registers Overview------------
    IOCFG2 = 0x00
    IOCFG1 = 0x01 
    IOCFG0 = 0x02
    FIFOTHR = 0x03 
    SYNC1 = 0x04 
    SYNC0 = 0x05 
    PKTLEN = 0x06
    PKTCTRL1 = 0x07
    PKTCTRL0 = 0x08
    ADDR = 0x09
    CHANNR = 0x0A
    FSCTRL1 = 0x0B
    FSCTRL0 = 0x0C
    FREQ2 = 0x0D
    FREQ1 = 0x0E
    FREQ0 = 0x0F 
    MDMCFG4 = 0x10 
    MDMCFG3 = 0x11 
    MDMCFG2 = 0x12
    MDMCFG1 = 0x13
    MDMCFG0 = 0x14
    DEVIATN = 0x15 
    MCSM2 = 0x16 
    MCSM1 = 0x17 
    MCSM0 = 0x18 
    FOCCFG = 0x19 
    BSCFG = 0x1A
    AGCTRL2 = 0x1B 
    AGCTRL1 = 0x1C
    AGCTRL0 = 0x1D
    WOREVT1 = 0x1E
    WOREVT0 = 0x1F 
    WORCTRL = 0x20
    FREND1 = 0x21
    FREND0 = 0x22
    FSCAL3 = 0x23 
    FSCAL2 = 0x24
    FSCAL1 = 0x25
    FSCAL0 = 0x26 
    RCCTRL1 = 0x27 
    RCCTRL0 = 0x28 
    FSTEST = 0x29
    PTEST = 0x2A
    AGCTEST = 0x2B
    TEST2 = 0x2C
    TEST1 = 0x2D
    TEST0 = 0x2E

    #-------------Status Registers Overview------------
    PARTNUM = 0xF1 
    VERSION = 0xF1
    FREQEST = 0xF2
    LQI = 0xF3
    RSSI = 0xF4
    MARCSTATE = 0xF5
    WORTIME1 = 0xF6
    WORTIME0 = 0xF7
    PKTSTATUS = 0xF8
    VCO_VC_DAC = 0xF9
    TXBYTES = 0xFA
    RXBYTES = 0xFB
    RCCTRL1_STATUS = 0xFC
    RCCTRL0_STATUS = 0xFD

    def __init__(self, bus = 0, device = 0, speed = 100000):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)   #connected to 0,0 because GPIO8 (24) is used
        self.spi.max_speed_hz = speed


    def selfTest(self):
        part_number = self.spi.xfer([0x80|0xF4,0x00])[1]
        return part_number




    def write_single_byte(self, address, data, prefix = 0x00):
        return self.spi.xfer([address|prefix, data])

    def write_burst_byte(self, address, data, prefix = 0x40):
        pass

    def read_single_byte(self, address, prefix = 0x80):
        return self.spi.xfer([address|prefix, 0x00])

    def read_burst_byte(self, address, data, prefix = 0xC0):
        pass




    def strobes_read(self, address, prefix = 0x80):
        return self.spi.xfer([address|prefix])

    def strobes_write(self, address, prefix = 0x00):
        return self.spi.xfer([address|prefix])




    def configuration(self, frequency): #będą tutaj takie zmienne jak częstotliwość moc itp
        pass

    def easy_configuration(self, version):   #tylko kilka wersji od razu gotowych, najlepiej by każda kolejna była lepsza np na większe odległosći i tłumienia
        pass

    def RSSI_value():
        pass




    def test(self):
        x = self.read_single_byte(self.RXBYTES)
        for i in range(len(x)):
            x[i] = '{0:08b}'.format(x[i])
        return x


    #4 funkcje read write, 