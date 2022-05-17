from cc1101 import CC1101
import time
import json

#----------------Measurements variables-----------
data0_sum = 0
data1_sum = 0
number = 0
measurements = 60
crc0_count = 0
nopacket_count = 0
measurement_finish = False
#-------------------------------------------------

data = {"Data":{},
        "Radio_connection":{},
        }

radio_module = CC1101()
radio_module.prepare()
#radio_module.write_single_byte(0x0F, 0x62)
#radio_module.write_single_byte(0x0E, 0xA7)
#radio_module.write_single_byte(0x0D, 0x10)

while True:

    received_data = radio_module.receive()
    print(received_data)
    if received_data != None:   #pokombinować bo jezeli np będzie jakiś błąd to wejdzie tutaj bo nie bedzie wartości None powodując błędy
        temperature = received_data[0] - 100
        humidity = received_data[1]
        antena_name = ""
        print(received_data)
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
        data["SensorID"] = serial_name
        data["Source"] = "Radio"

        json_radio_data = json.dumps(data)
        print(json_radio_data)


    #-----------------Measurement-----------------------------    
        data23 = [rssi,lqi]
        if crc == 128:
            if number<measurements:

                f = open("800again_50", "a")
                string = str(data23[0])+", "+str(data23[1])+"\n"
                f.write(string)
                data0_sum = data0_sum + data23[0]
                data1_sum = data1_sum + data23[1]
                if number == measurements-1:
                    string1 = "Podsumowanie:"+str(data0_sum/measurements)+", "+str(data1_sum/measurements)+", crc0->"+str(crc0_count)+", no_packet->"+str(nopacket_count-1)+"\n"
                    f.write(string1)
                    f.close()
                    measurement_finish = True
            number = number + 1
        else:
            crc0_count = crc0_count + 1
            print("crc0count",crc0_count)
    else:
        nopacket_count = nopacket_count + 1
        print("npktcount",nopacket_count)
    if measurement_finish:
        print("MEASUREMENT IS COMPLETE")
    #-------------------------------------------------------------
    send_data_test = [0,1,2,3,4,5]
    
    #time.sleep(2)
    #radio_module.transmit(send_data_test)