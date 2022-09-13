from cc1101 import CC1101
import time
import json

#----------------Measurements variables-----------
data0_sum = 0
data1_sum = 0
number = 0
measurements = 60
crc0_count = 0
crc0_433_count = 0
crc0_868_count = 0
nopacket_count = 0
nopacket_433_count = 0
nopacket_868_count = 0
measurement_finish = False
freq_433_num_measure = 0
freq_868_num_measure = 0
#-------------------------------------------------
current_time = 0
freq = 433
data_connect_info = [0,1,2,3,4,5]
change_to_433 = [4,4,4,4,4,4]
change_to_868 = [8,8,8,8,8,8]
data_freq_conn_test = [1,1,1,1,1,1]

rssi_condition = []
crc_condition = 0
flag_crc_condition = False
nopkt_condition = 0
flag_nopkt_condition = False
flag_rssi_condition = False
freq_conn_test = False
freq_conn_test_info = False
freq_conn_test_counter = 0
nopkt_condition_conn_test = 0
no_condition_check_counter = 0
no_condition_check = False
check_conditions = True

data = {"Data":{},
        "Radio_connection":{},
        }

radio_module = CC1101()
radio_module.prepare()


while True:
    start_time = time.time()

    received_data = radio_module.receive()
    #print(received_data)
    #f = open("400_800_10_0pop_att.txt", "a")
    if received_data != None:   #pokombinować bo jezeli np będzie jakiś błąd to wejdzie tutaj bo nie bedzie wartości None powodując błędy
        temperature = received_data[0] - 100
        humidity = received_data[1]
        antena_name = ""
        #print(received_data)
        for x in range(10,20):
            if received_data[x] != 0:
                antena_name = antena_name + chr(received_data[x])
        antena_name = str(antena_name)

        server_ip = ""
        for x in range(20,24):
            server_ip = server_ip + str(received_data[x])
            if x < 23:
                server_ip = server_ip + "."

        rssi = received_data[-3]
        lqi = received_data[-2]
        crc = received_data[-1]
        #print(crc)

        serial_name = ""
        for x in range(24,40):
            if received_data[x] != 0:
                serial_name = serial_name + chr(received_data[x])
        serial_name = str(serial_name)

        data["Data"]["Temperature"] = temperature
        data["Data"]["Humidity"] = humidity
        data["Radio_connection"]["Antena_name"] = antena_name
        data["Radio_connection"]["Server_ip"] = server_ip
        data["Radio_connection"]["RSSI"] = rssi
        data["Radio_connection"]["LQI"] = lqi
        data["Radio_connection"]["Frequency"] = freq
        data["SensorID"] = serial_name
        data["Source"] = "Radio"

        json_radio_data = json.dumps(data)
        print(json_radio_data)


        #------------RSSI_CONDITION--------------
        if check_conditions:
            rssi_condition.append(rssi)
            if len(rssi_condition) == 6:
                rssi_condition = rssi_condition[1:]
            if len(rssi_condition) == 5:
                rssi_sum = 0
                for x in rssi_condition:
                    rssi_sum = rssi_sum + x
                average = rssi_sum/5
                #print("elo average", average)
                if average > -50 or average < -105:
                    flag_rssi_condition = True
                else:
                    flag_rssi_condition = False
        #---------------------------------------

        #------------NOCRC_CONDITION--------------
        if check_conditions:
            if crc == 0:
                if crc_condition > -10:
                    crc_condition = crc_condition - 1
                if crc_condition == -10:
                    flag_crc_condition = True
                    crc_condition = 0
            elif crc == 128:
                if crc_condition < 10:
                    crc_condition = crc_condition + 1
                if crc_condition == 10:
                    flag_crc_condition = False
                    crc_condition = 0

    #-----------------Measurement-----------------------------  
        #data23 = [rssi,lqi]
        #if crc == 128:
            #if number<measurements:

                #string = str(data23[0])+", "+str(data23[1])+", "+str(freq)+"\n"
                #f.write(string)
                #data0_sum = data0_sum + data23[0]
                #data1_sum = data1_sum + data23[1]
                #if freq == 433:
                    #freq_433_num_measure = freq_433_num_measure + 1
                #if freq == 868:
                    #freq_868_num_measure = freq_868_num_measure + 1
                #if number == measurements-1:
                    #string1 = "Podsumowanie:"+str(data0_sum/measurements)+", "+str(data1_sum/measurements)+", crc0->"+str(crc0_count)+", no_packet->"+str(nopacket_count-1)+", 433->"+str(freq_433_num_measure)+", 868->"+str(freq_868_num_measure)+", nocrc_433->"+str(crc0_433_count)+", nocrc_868->"+str(crc0_868_count)+", nopkt_433->"+str(nopacket_433_count)+", nopkt_868->"+str(nopacket_868_count)+"\n"
                    #f.write(string1)
                    #f.close()
                    #measurement_finish = True
            #number = number + 1
        #else:
            #crc0_count = crc0_count + 1
            #if freq == 433:
                #crc0_433_count = crc0_433_count + 1
            #if freq == 868:
                #crc0_868_count = crc0_868_count + 1
            #string2 = "no_crc, freq = "+str(freq)+"\n"
            #f.write(string2)
            #print("crc0count",crc0_count)
    else:
        pass
        #nopacket_count = nopacket_count + 1
        #if freq == 433:
            #nopacket_433_count = nopacket_433_count + 1
        #if freq == 868:
            #nopacket_868_count = nopacket_868_count + 1
        #string3 = "no_pkt, freq = "+str(freq)+"\n"
        #f.write(string3)
        #print("npktcount",nopacket_count)
    #if measurement_finish:
        #print("MEASUREMENT IS COMPLETE")
    #-------------------------------------------------------------


    #------------NOPKT_CONDITION--------------
    if received_data == None and check_conditions:
        #print("nopkt_condition")
        nopkt_condition = nopkt_condition + 1
        if nopkt_condition == 5:
            flag_nopkt_condition = True
            #print(flag_nopkt_condition)
    else:
        nopkt_condition = 0
        flag_nopkt_condition = False

    #sprawdzamy czy otrzymujemy po zmianie wiadomości jezeli nie zmień częstotliwość serwera na starą i zakarz sprawdzania warunków przez określony czas (zmiana okazała się złą decyzją)
    if freq_conn_test == True:
        if received_data == None:
            nopkt_condition_conn_test = nopkt_condition_conn_test + 1
            if nopkt_condition_conn_test == 5:
                no_condition_check = True
                flag_nopkt_condition = False
                if freq == 433:
                    radio_module.frequency_868()
                    freq = 868
                elif freq == 868:
                    radio_module.frequency_433()
                    freq = 433
        else:
            freq_conn_test = False
            nopkt_condition_conn_test = 0

    #wysyłamy do klienta informacje by sprawdzić czy po przełączeniu częstotliwości nadal się słyszymy, bardzo ważna wiadomość dlatego wysyłana 3 krotnie, jezeli klient jej nie otrzyma zmieni częstotliwość na starą
    if freq_conn_test_info:
        freq_conn_test_counter = freq_conn_test_counter + 1
        if freq_conn_test_counter < 4:
            radio_module.transmit(data_freq_conn_test)
            time.sleep(0.5)
            radio_module.transmit(data_freq_conn_test)
        else:
            freq_conn_test_info = False
            freq_conn_test_counter = 0


    if flag_rssi_condition or flag_crc_condition:
        rssi_condition = []
        average = 0
        flag_rssi_condition = False
        crc_condition = 0
        flag_crc_condition = False
        if freq == 433:
            radio_module.transmit(change_to_868)
            time.sleep(0.5) # na wypadek gdyby nadanie było podczas gdy klient jest w stanie nadawania
            radio_module.transmit(change_to_868)
            radio_module.frequency_868()
            freq = 868
            freq_conn_test = True
            freq_conn_test_info = True
        elif freq == 868:
            radio_module.transmit(change_to_433)
            time.sleep(0.5) # na wypadek gdyby nadanie było podczas gdy klient jest w stanie nadawania
            radio_module.transmit(change_to_433)
            radio_module.frequency_433()
            freq = 433
            freq_conn_test = True
            freq_conn_test_info = True
            pass

    #print(nopkt_condition)
    
    if flag_nopkt_condition:
        nopkt_condition = 0
        flag_nopkt_condition = False
        if freq == 433:
            radio_module.frequency_868()
            freq = 868
            #print("zmiana f na 868")
        elif freq == 868:
            radio_module.frequency_433()
            freq = 433
            #print("zmiana f na 433")

    if no_condition_check:
        check_conditions = False
        no_condition_check_counter = no_condition_check_counter + 1
        #print("NO CONDITIONS CHECK!!!")
        if no_condition_check_counter == 300:
            check_conditions = True
            no_condition_check = False
            no_condition_check_counter = 0

    if start_time - current_time > 60:
        current_time = start_time
        radio_module.transmit(data_connect_info)
        time.sleep(0.5) # na wypadek gdyby nadanie było podczas gdy klient jest w stanie nadawania
        radio_module.transmit(data_connect_info)
