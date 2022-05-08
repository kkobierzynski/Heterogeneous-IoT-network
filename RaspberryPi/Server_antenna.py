from cc1101 import CC1101
import time
import json

data = {"Data":{},
        "Radio_connection":{},
        }

radio_module = CC1101()
radio_module.prepare()


while True:

    received_data = radio_module.receive()
    #print(received_data)
    if received_data != None:   #pokombinować bo jezeli np będzie jakiś błąd to wejdzie tutaj bo nie bedzie wartości None powodując błędy
        temperature = received_data[0] - 100
        humidity = received_data[1]
        antena_name = ""
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
        print(crc)

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
    
    time.sleep(1)