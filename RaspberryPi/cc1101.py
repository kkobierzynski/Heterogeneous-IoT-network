from logging import warning
import spidev
import time

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
    AGCCTRL2 = 0x1B 
    AGCCTRL1 = 0x1C
    AGCCTRL0 = 0x1D
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
    PARTNUM = 0xF0
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

    TXFIFO = 0x3F
    RXFIFO = 0x3F
    PATABLE = 0x3E


    def __init__(self, bus = 0, device = 0, speed = 100000):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)   #connected to 0,0 because GPIO8 (24) is used
        self.spi.max_speed_hz = speed
        self.debug = False



    
    def decbinhex_write(self, dec, address, data):
        print("Register:",hex(address)," after write data ",data," answer: ",dec)
        for i in range(len(dec)):
            dec[i] = '{0:08b}'.format(dec[i])
        print("Register:",hex(address)," after write data ",data," answer: ",dec)
        for i in range(len(dec)):
            dec[i] = hex(int(dec[i], 2))
        print("Register:",hex(address)," after write data ",data," answer: ",dec)

    def decbinhex_read(self, dec, address):
        print("Register:",hex(address)," after reading answer: ",dec)
        for i in range(len(dec)):
            dec[i] = '{0:08b}'.format(dec[i])
        print("Register:",hex(address)," after reading answer: ",dec)
        for i in range(len(dec)):
            dec[i] = hex(int(dec[i], 2))
        print("Register:",hex(address)," after reading answer: ",dec)




    def write_single_byte(self, address, data, prefix = 0x00):
        return self.spi.xfer([address|prefix, data])

    def write_burst_byte(self, address, data, prefix = 0x40):
        address = address|prefix
        data.insert(0,address)
        return self.spi.xfer(data)

    def read_single_byte(self, address, prefix = 0x80):
        return self.spi.xfer([address|prefix, 0x00])

    def read_burst_byte(self, address, length, prefix = 0xC0):
        addresses = []
        for i in range(length):
            addresses.append((address + i*8)|prefix)
        return self.spi.xfer(addresses)[1:]




    def strobes_read(self, address, prefix = 0x80):
        return self.spi.xfer([address|prefix])

    def strobes_write(self, address, prefix = 0x00):
        return self.spi.xfer([address|prefix])

    def strobes_stx(self, prefix = 0x00):
        return self.spi.xfer([self.STX|prefix])

    def strobes_srx(self, prefix = 0x00):
        return self.spi.xfer([self.SRX|prefix])



    def configuration(self, frequency): #będą tutaj takie zmienne jak częstotliwość moc itp
        pass

    def easy_configuration(self, version):   #tylko kilka wersji od razu gotowych, najlepiej by każda kolejna była lepsza np na większe odległosći i tłumienia
        if version == 1:
            self.write_single_byte(self.IOCFG2, 0x29)
            self.write_single_byte(self.IOCFG1, 0x2E)
            self.write_single_byte(self.IOCFG0, 0x06)
            self.write_single_byte(self.FIFOTHR, 0x47)
            self.write_single_byte(self.SYNC1, 0xD3)
            self.write_single_byte(self.SYNC0, 0x91)
            self.write_single_byte(self.PKTLEN, 0xFF)
            self.write_single_byte(self.PKTCTRL1, 0x04)
            self.write_single_byte(self.PKTCTRL0, 0x05)
            self.write_single_byte(self.ADDR, 0x00)
            self.write_single_byte(self.CHANNR, 0x00)
            self.write_single_byte(self.FSCTRL1, 0x06)
            self.write_single_byte(self.FSCTRL0, 0x00)
            self.write_single_byte(self.FREQ2, 0x10)
            self.write_single_byte(self.FREQ1, 0xA7)
            self.write_single_byte(self.FREQ0, 0x62)
            self.write_single_byte(self.MDMCFG4, 0xF5)
            self.write_single_byte(self.MDMCFG3, 0x83)
            self.write_single_byte(self.MDMCFG2, 0x13)
            self.write_single_byte(self.MDMCFG1, 0x22)
            self.write_single_byte(self.MDMCFG0, 0xF8)
            self.write_single_byte(self.DEVIATN, 0x15)
            self.write_single_byte(self.MCSM2, 0x07)
            self.write_single_byte(self.MCSM1, 0x30)
            self.write_single_byte(self.MCSM0, 0x18)
            self.write_single_byte(self.FOCCFG, 0x16)
            self.write_single_byte(self.BSCFG, 0x6C)
            self.write_single_byte(self.AGCCTRL2, 0x03)
            self.write_single_byte(self.AGCCTRL1, 0x40)
            self.write_single_byte(self.AGCCTRL0, 0x91)
            self.write_single_byte(self.WOREVT1, 0x87)
            self.write_single_byte(self.WOREVT0, 0x6B)
            self.write_single_byte(self.WORCTRL, 0xFB)
            self.write_single_byte(self.FREND1, 0x56)
            self.write_single_byte(self.FREND0, 0x10)
            self.write_single_byte(self.FSCAL3, 0xE9)
            self.write_single_byte(self.FSCAL2, 0x2A)
            self.write_single_byte(self.FSCAL1, 0x00)
            self.write_single_byte(self.FSCAL0, 0x1F)
            self.write_single_byte(self.RCCTRL1, 0x41)
            self.write_single_byte(self.RCCTRL0, 0x00)
            self.write_single_byte(self.FSTEST, 0x59)
            self.write_single_byte(self.PTEST, 0x7F)
            self.write_single_byte(self.AGCTEST, 0x3F)
            self.write_single_byte(self.TEST2, 0x81)
            self.write_single_byte(self.TEST1, 0x35)
            self.write_single_byte(self.TEST0, 0x09)

    def frequency_433(self):
        self.write_single_byte(self.FREQ0, 0x62)
        self.write_single_byte(self.FREQ1, 0xA7)
        self.write_single_byte(self.FREQ2, 0x10)

    def frequency_868(self):
        self.write_single_byte(self.FREQ0, 0x76)
        self.write_single_byte(self.FREQ1, 0x62)
        self.write_single_byte(self.FREQ2, 0x21)

    def RSSI_value(self, RSSI):
            if RSSI >= 128:
                RSSI_dBm = (RSSI-256)/2 - 74
            elif RSSI < 128:
                RSSI_dBm = RSSI/2 - 74
            return RSSI_dBm



    def read_from_register_test(self):
        x = self.read_single_byte(self.ADDR)
        self.decbinhex_read(x, self.ADDR)
        return x
    
    def write_to_register_test(self):
        x = self.write_single_byte(self.TXFIFO, 0xFF)
        self.decbinhex_write(x, self.TXFIFO, 0xFF)
        return x

    def txbytes_status(self):
        x = self.read_single_byte(self.TXBYTES)[1]
        x = x & 0x7f
        return x

    def rxbytes_status(self):
        x = self.read_single_byte(self.RXBYTES)[1]
        x = x & 0x7f
        return x

    def pktlen(self):
        information = self.read_single_byte(self.PKTLEN)[1]
        return information

    def marcstate_status(self):         #Opisuje stan w jakim znajduje się w tym momencie moduł radiowy
        information = self.read_single_byte(self.MARCSTATE)[1]        #1 ponieważ chcemy tylko informacje z rejestru a nie chip status
        if self.debug == True:
            if information == 0:
                print("Actual state name - SLEEP")
            elif information == 1:
                print("Actual state name - IDLE")
            elif information == 2:
                print("Actual state name - XOFF")
            elif information == 3:
                print("Actual state name - VCOON_MC")
            elif information == 4:
                print("Actual state name - REGON_MC")
            elif information == 5:
                print("Actual state name - MANCAL")
            elif information == 6:
                print("Actual state name - VCOON")
            elif information == 7:
                print("Actual state name - REGON")
            elif information == 8:
                print("Actual state name - STARTCAL")
            elif information == 9:
                print("Actual state name - BWBOOST")
            elif information == 10:
                print("Actual state name - FS_LOCK")
            elif information == 11:
                print("Actual state name - IFADCON")
            elif information == 12:
                print("Actual state name - ENDCAL")
            elif information == 13:
                print("Actual state name - RX")
            elif information == 14:
                print("Actual state name - RX_END")
            elif information == 15:
                print("Actual state name - RX_RST")
            elif information == 16:
                print("Actual state name - TXRX_SWITCH")
            elif information == 17:
                print("Actual state name - RXFIFO_OVERFLOW")
            elif information == 18:
                print("Actual state name - FSTXON")
            elif information == 19:
                print("Actual state name - TX")
            elif information == 20:
                print("Actual state name - TX_END")
            elif information == 21:
                print("Actual state name - RXTX_SWITCH")
            elif information == 22:
                print("Actual state name - TXFIFO_UNDERFLOW")
            else:
                print("Wrong variable - unrecognizable state")

        return information



    def prepare(self):
        self.strobes_write(self.SRES)
        self.easy_configuration(1)

    def send_test(self):
        x = self.write_single_byte(self.TXFIFO, 0x69)

        if x[0] == 127:
            self.strobes_write(self.SFTX)
        self.strobes_write(self.STX)  
        

    def read_test(self):
        return self.read_single_byte(self.RXBYTES)

    def control_state(self, mode):      #Obsługa rejestru MCSM1
        information = self.read_single_byte(self.MCSM1)[1]  #Odczytanie wartości rejestru
        information_bin = '{0:08b}'.format(information)     #Zamiana z systemu dziesiątkowego na binarny
        information_char_bin = []
        mode_information = ""
        for sign in information_bin:    #Rozdzielenie odczytanej wartości na osobne znaki 
            information_char_bin.append(sign)
        if mode == "CCA_MODE":  #Odczytanie dwóch bitów odnoszących się do CCA_MODE
            for i in range(2,4):
                mode_information += information_char_bin[i]
            return mode_information
        elif mode == "RXOFF_MODE":    #Odczytanie dwóch bitów odnoszących się do RXOFF_MODE (mówi w jaki stan przejdzie moduł radiowy po odbiorze)
            for i in range(4,6):
                mode_information += information_char_bin[i]
            return mode_information
        elif mode == "TXOFF_MODE":    #Odczytanie dwóch bitów odnoszących się do TXOFF_MODE (mówi w jaki stan przejdzie moduł radiowy po wysłaniu)
            for i in range(6,8):
                mode_information += information_char_bin[i]
            return mode_information
        else:
            return "Wrong mode name"

    def packet_control(self, mode):
        pktctrl0 = self.read_single_byte(self.PKTCTRL0)[1]
        pktctrl1 = self.read_single_byte(self.PKTCTRL1)[1]
        pktctrl0_bin = '{0:08b}'.format(pktctrl0)
        pktctrl1_bin = '{0:08b}'.format(pktctrl1)
        pktctrl0_char_bin = []
        pktctrl1_char_bin = []
        mode_information = ""
        for sign in pktctrl0_bin:    #Rozdzielenie odczytanej wartości na osobne znaki 
            pktctrl0_char_bin.append(sign)
        for sign in pktctrl1_bin:
            pktctrl1_char_bin.append(sign)

        if mode == "WHITE_DATA":  #Odczytanie bitu odnoszących się do WHITE_DATA
            mode_information = pktctrl0_char_bin[1]
            return mode_information
        elif mode == "PKT_FORMAT":    #Odczytanie dwóch bitów odnoszących się do PKT_FORMAT 
            for i in range(2,4):
                mode_information += pktctrl0_char_bin[i]
            return mode_information
        elif mode == "CRC_EN":    #Odczytanie bitu odnoszącego się do CRC_EN (sprawdza czy włączona jest suma kontrolna, 0 wyłączona, 1 włączona)
            mode_information = pktctrl0_char_bin[5]
            return mode_information
        elif mode == "LENGTH_CONFIG":    #Odczytanie dwóch bitów odnoszących się do LENGTH_CONFIG (definiuje w jaki sposób sprawdza się długość pakietu, 00 Fixed packet length mode - info tylko w rejestrze, 01 variable packet lenght mode - info także w pakiecie, 10 infinite, 11 reserved)
            for i in range(6,8):
                mode_information += pktctrl0_char_bin[i]
            return mode_information
        elif mode == "PQT":    #Odczytanie trzech bitów odnoszących się do PQT
            for i in range(0,3):
                mode_information += pktctrl1_char_bin[i]
            return mode_information
        elif mode == "CRC_AUTOFLUSH":    #Odczytanie bitu odnoszącego się do CRC_AUTOFLUSH (Enable automatic flush of RX FIFO when CRC is not OK, pakiet może mieć max 64 bajty)
            mode_information = pktctrl1_char_bin[4]
            return mode_information
        elif mode == "APPEND_STATUS":    #Odczytanie bitu odnoszącego się do APPEND_STATUS (mówi czy do pakietu dodane będą na końcu dwa bajty odnoszące sie do jakości transmisji RSSI LQI CRC)
            mode_information = pktctrl1_char_bin[5]
            return mode_information
        elif mode == "ADR_CHK":    #Odczytanie dwóch bitów odnoszących się do ADR_CHK (definiuje w jaki sposób filtruje się pakiet, 00 bez sprawdzania adresu, 01 sprawdzanie adresu czyli brak broadcast, 10 sprawdzanie adresu i 0x00 broadcast, 11 Address check and 0 (0x00) and 255 (0xFF) broadcast)
            for i in range(6,8):
                mode_information += pktctrl1_char_bin[i]
            return mode_information
        else:
            return "Wrong mode name"


    def transmit(self, data): #dodać jeszcze możłiwość asci
        #print("transmit data")
        state = self.marcstate_status()
        length_mode = self.packet_control("LENGTH_CONFIG")
        data_length = len(data)
        packet_length = self.pktlen()
        packet_data = []
        #print(state)

        if state == 13 or state == 14 or state == 15:
            warning = "WARNING - RX state in transmit mode is not supported. Data transfer not completed !!!!!"
            self.strobes_write(self.SIDLE)
            state = self.marcstate_status()
            #print("state->",state)
            #print(warning)

        if length_mode == "00":    #Fixed packet length mode - info tylko w rejestrze
            error = "Error - length mode is not yet supported. Data transfer not completed !!!!!"
            return print(error)
        elif length_mode == "01":    #Variable packet length mode - info także w pakiecie
            if data_length>61 and self.packet_control("CRC_AUTOFLUSH")=="1":    #Dla bezpieczeństwa przyjęto 61 tak jak pisało w dokumentacji (63 - 2 bajty kontroli jakości), testy wykazały że działało do 62 bajtów danych tak ze po stronie odbiorczej w RXFIFO zajętych było 65 bajtów. Ograniczenie wynika z konieczności czyszczenia całęgo RXFIFO którym ma 64 bajty jezeli CRC wyjdzie niepoprawne
                error = "ERROR - Moduł radiowy działa w trybie CRC_AUTOFLUSH. Maksymalna dozwolona liczba przesłanych bajtów wynosi 61, przesłane dane mają ",data_length," bajty. Nie zrealizowano przesłania danych!!!!"
                return print(error)
            if data_length>packet_length and self.packet_control("CRC_AUTOFLUSH")=="0":   #Jeżeli długość danych przekracza maksymalną długość pakietu i CRC_AUTOFLUSH jest wyłączony
                error = "ERROR - Ilość bajtów danych przekracza maksymalny próg określony w rejestrze PKTLEN. Maksymalny rozmiar pakietu to ",packet_length," bajty. Pakiet ma rozmiar ",data_length,"bajtów. Nie zrealizowano przesłania danych!!!!"
                return print(error)
            packet_data.append(data_length)     #Adding necessary information about data length at the start of packet 
            if self.packet_control("ADR_CHK") != "00":  #Checking if it is necessary to add addres byte at the start of packet
                if data_length == packet_length:
                    error = "ERROR - No space for adding 1 address byte. Release one byte in data, change size data size in register PKTLEN or change PKTCTRL1.ADR_CHK to 00 - no address check. Data transfer not completed !!!!!"
                    return print(error)
                packet_data.append(self.read_single_byte(self.ADDR)[1])
                packet_data[0] = packet_data[0] + 1     #Increasing packet size by one, because of adding address
            packet_data.extend(data)
            #print(packet_data)
        elif length_mode == "10":   #Infinite packet length mode
            error = "ERROR - tryb nie jest jeszcze obsługiwalny, proszę wybrać Variable packet length mode lub Fixed packet length mode. Nie zrealizowano przesłąnia danych!!!!!"
            return print(error)
        else:
            error = "ERROR - błędna wartość rejestru PKTCTRL0.LENGTH_CONFIG. Nie zrealizowano przesłąnia danych!!!!!"
            return print(error)

        self.write_burst_byte(0x3F,packet_data)
        time.sleep(0.001)

        if state == 1:      #Checking if radio module is in IDLE state if yes it is necessary to change state to TX to send data saved in TXFIFO buffer
            txbytes = self.txbytes_status()
            #print("przed STX",txbytes)
            self.strobes_stx()
            time.sleep(1)
            txbytes = self.txbytes_status()
            #print("po STX",txbytes)
            state = self.marcstate_status()
            if state == 22:
                error = "Error - TXFIFO_UNDERFLOW detected. TX FIFO buffer flush was made and state was changed to IDLE. Data transfer not completed !!!!!"
                self.strobes_write(self.SFTX)
                return print(error)
            while txbytes != 0:     #waiting until all data from buffer is transmited 
                time.sleep(0.001)
                txbytes = self.txbytes_status()
                #print(txbytes)
            if txbytes == 0:
                success = "Data sent successfully !!!"
                #print(success)
                return
            else:
                error = "Error - Unknown error, some data may not have been sent"
                return print(error)
        elif state == 19 or state == 20 or state == 21:     #this state (when module is already in TX state) has not been tested, the code is based on assumptions after reading the documentation
            txbytes = self.txbytes_status()
            while txbytes != 0:     #waiting until all data from buffer is transmited 
                time.sleep(0.001)
                txbytes = self.txbytes_status()
            if txbytes == 0:
                success = "Data sent successfully !!!"
                return print(success)
            else:
                error = "Error - Unknown error, some data may not have been sent"
                return print(error)
        elif state == 22:
            error = "Error - TXFIFO_UNDERFLOW detected. TX FIFO buffer flush was made and state was changed to IDLE. Data transfer not completed !!!!!"
            self.strobes_write(self.SFTX)
            return print(error)
        else:
            error = "Error - the radio module took an unpredictable state value equal to ",state
            return print(error)



    def receive(self):
        state = self.marcstate_status()
        #print("przed",state)
        self.strobes_srx()
        time.sleep(4)
        rxbytes = self.rxbytes_status() 
        state = self.marcstate_status()
        if state == 13 and rxbytes != 43 and rxbytes != 0:
            #print("wszedłem!!")
            time.sleep(1)
            rxbytes = self.rxbytes_status() 
        length_mode = self.packet_control("LENGTH_CONFIG")
        append_status = self.packet_control("APPEND_STATUS")
        data = []
        #print("po",state)
        #print(rxbytes)
        if state == 17:
            error = "Error - RXFIFO_OVERFLOW detected. RX FIFO buffer flush was made and state was changed to IDLE. Data reception not completed !!!!! "
            self.strobes_write(self.SFRX)
            return print(error)
        if rxbytes != 0 and state != 17:
            if length_mode == "00":    #Fixed packet length mode - info tylko w rejestrze
                error = "Error - length mode is not yet supported. Data reception not completed !!!!!"
                return print(error)
            elif length_mode == "01":    #Variable packet length mode - info także w pakiecie
                data_length = self.read_single_byte(self.RXFIFO)[1]
                state = self.marcstate_status()
                #print("popo",state)
                #print(data_length)
                max_length = self.read_single_byte(self.PKTLEN)[1]
                if data_length > max_length:
                    error = "ERROR - Ilość bajtów danych przekracza maksymalny próg określony w rejestrze PKTLEN. Maksymalny rozmiar pakietu to ",max_length," bajty. Pakiet ma rozmiar ",data_length,"bajtów. Nie zrealizowano przesłania danych!!!!"
                    return print(error)
            elif length_mode == "10":   #Infinite packet length mode
                error = "ERROR - tryb nie jest jeszcze obsługiwalny, proszę wybrać Variable packet length mode lub Fixed packet length mode. Nie zrealizowano przesłąnia danych!!!!!"
                return print(error)
            else:
                error = "ERROR - błędna wartość rejestru PKTCTRL0.LENGTH_CONFIG. Nie zrealizowano przesłąnia danych!!!!!"
                return print(error)
            if self.packet_control("ADR_CHK") != "00":
                print("This state wasn't checked. Please make sure that address information isnt in payload, what can make some problems in data analysis")

            data.extend(self.read_burst_byte(self.RXFIFO, data_length+1))

            if append_status == "1":
                rssi = self.read_single_byte(self.RXFIFO)[1]
                rssi = self.RSSI_value(rssi)
                lqi_and_crc = self.read_single_byte(self.RXFIFO)[1]
                lqi = lqi_and_crc & 0x7f
                crc_ok = lqi_and_crc & 0x80
                #print("crc",crc_ok)
                data.append(rssi)
                data.append(lqi)
                data.append(crc_ok)
                #if crc_ok == 0:
                #    return print("CRC check not passed")

            #self.strobes_write(self.SIDLE)
            #time.sleep(0.0001)
            #self.strobes_write(self.SFRX)
            #time.sleep(0.0001)
            #self.strobes_srx()
            #time.sleep(0.0001)
            state = self.marcstate_status()
            #print(state)
            return data
        
        else:
            state = self.marcstate_status()
            #print(state)
            self.strobes_write(self.SIDLE)
            time.sleep(0.0001)
            self.strobes_write(self.SFRX)
            time.sleep(0.0001)
            pass




    #4 funkcje read write, 