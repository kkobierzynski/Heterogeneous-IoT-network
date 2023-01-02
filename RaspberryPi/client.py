import paho.mqtt.client as mqtt
import json
import time
import SysInfo
from cc1101 import CC1101
import urllib.request
import random

#----------DATA STRUCTURES--------
data = {"Data":{},
        "Network":{},
        }

radio_module = CC1101()
radio_module.prepare()
tescik_licznik = 0
freq = 433
#test.strobes_write(0x35)

#---------------GLOBAL VARIABLES---------------
mqtt_username = "myuser"
mqtt_password = "raspberrypi"
mqtt_broker_ip = "192.168.0.220"
current_time = 0
current_time_radio_serv = 0   #ponieważ nie chcemy by warunek został spełniony od razu, tylko jezeli minie określony czas -> zmiana częstotliwości. Dlatego nie przypisujemy 0
mqtt_counter = 0
flag_connected_mqtt = False
flag_radio = False
first_client_establish = True
flag_radio_mode_config = True
freq_conn_test = False
freq_conn_test_counter = 0
serial = SysInfo.BoardInfo.serial()
model = SysInfo.BoardInfo.model()

#---------TOPICS-----------
topic_data = "RaspberryPi3/data"
topic_sub_led = "RaspberryPi3/led"




#---------------CALLBACK FUNCTIONS-------------------

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global flag_connected_mqtt
    global flag_radio
    if rc == 0:
        print(str(rc)+": Connection successful")
        flag_connected_mqtt = True
        flag_radio = False
    elif rc == 1:
        print(str(rc)+": Connection refused – incorrect protocol version")
    elif rc == 2:
        print(str(rc)+": Connection refused – invalid client identifier")
    elif rc == 3:
        print(str(rc)+": Connection refused – server unavailable")
    elif rc == 4:
        print(str(rc)+": Connection refused – bad username or password")
    elif rc == 5:
        print(str(rc)+": Connection refused – not authorised")
    else:
        print(str(rc)+": Unknown error")    
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_sub_led)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == topic_sub_led:
        print(msg.topic+" "+str(msg.payload))




def on_disconnect(client, userdata, rc):
    global flag_connected_mqtt
    global flag_radio

    flag_connected_mqtt = False
    flag_radio = True
    print("cos",flag_connected_mqtt)


def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

#--------------------------------------------
if connect():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.username_pw_set(username=mqtt_username, password=mqtt_password)
    try:    #na wypadek jezeli klient ma połączenie z internetem ale serwer nie działa 
        client.connect(mqtt_broker_ip, 1883, 1)
        client.loop_start()
        first_client_establish = False
    except:
        first_client_establish = True
        flag_radio = True
else:
    flag_radio = True

while True:
    start_time = time.time() 
    start_time_radio_serv = time.time()
    #print("przed if",flag_connected_mqtt)
    

    if start_time-current_time > 5 and flag_connected_mqtt:
        print("mqtt_connection")
        current_time = start_time
        temperature = 20    # ZAMIENIĆ NA ODCZYTYWANIE Z CZUJNIKA
        humidity=40     # ZAMIENIĆ NA DOCZYTYWANIE Z CZUJNIKA
        flag_radio_mode_config = True

        if flag_connected_mqtt:
            rssi = SysInfo.NetworkInfo.rssi()
            ssid = SysInfo.NetworkInfo.ssid() #wrzucić w miejsce ponownego połączenia z wifi, tutaj bez sensu marnotractwo zasobów by liczyć to co każdą sekundę


        data["Data"]["Temperature"] = temperature
        data["Data"]["Humidity"] = humidity
        data["Network"]["Wifi_name"] = ssid
        data["Network"]["Server_ip"] = mqtt_broker_ip
        data["Network"]["Signal_strength"] = rssi
        data["SensorID"] = serial
        data["Sensor_Model"] = model
        data["Source"] = "MQTT"

        json_data = json.dumps(data)
        client.publish(topic_data, json_data)
        print(json_data)



        tescik_licznik = tescik_licznik + 1



    elif start_time-current_time > 1 and flag_radio:
        if flag_radio_mode_config:
            current_time_radio_serv = time.time()
            flag_radio_mode_config = False
            freq_conn_test = False
            freq_conn_test_counter = 0

        if first_client_establish and connect():
            mqtt_counter = mqtt_counter + 1
            if mqtt_counter == 20:
                try:
                    client = mqtt.Client()
                    client.on_connect = on_connect
                    client.on_message = on_message
                    client.on_disconnect = on_disconnect
                    client.username_pw_set(username=mqtt_username, password=mqtt_password)
                    client.connect(mqtt_broker_ip, 1883, 1)
                    client.loop_start()
                    first_client_establish = False
                except:
                    print("Mqtt Client establish error")
                    first_client_establish = True
                    mqtt_counter = 0

        current_time = start_time
        radio_data = []
        ascii_antena_name = []
        ascii_serial_name = []
        ip_number_data = []
        ip_number = ""
        counter = 0
        temperature = random.randint(-30, 90)    # ZAMIENIĆ NA ODCZYTYWANIE Z CZUJNIKA
        converted_temp = temperature + 100
        humidity=random.randint(0, 100)     # ZAMIENIĆ NA DOCZYTYWANIE Z CZUJNIKA
        reserved_data = [0,0,0,0,0,0,0,0]

        antena_name = "cc1101"
        for character in antena_name:
            counter+=1
            if counter <= 10:
                ascii_antena_name.append(ord(character))
            else:
                break
        if len(antena_name) < 10:
            for x in range(0,10-len(antena_name)):
                ascii_antena_name.append(0)
        counter = 0

        for character in mqtt_broker_ip:
            if character != ".":
                ip_number = ip_number + character
            else:
                ip_number_data.append(int(ip_number))
                ip_number = ""
        ip_number_data.append(int(ip_number))

        for character in serial:
            counter+=1
            if counter <= 16:
                ascii_serial_name.append(ord(character))
            else:
                break
        if len(serial) < 16:
            for x in range(0,16-len(serial)):
                ascii_serial_name.append(0)
        counter = 0

        radio_data.append(converted_temp)
        radio_data.append(humidity)
        radio_data.extend(reserved_data)
        radio_data.extend(ascii_antena_name)
        radio_data.extend(ip_number_data)
        radio_data.extend(ascii_serial_name)
        radio_data_len = len(radio_data)
        if radio_data_len < 64:
            radio_module.transmit(radio_data)
            print("radio_connection")
        else:
            print("Actually currently sending over 64 bytes causes errors, the problem will be fixed in the future please reduce amount of sending data")
        
        #Próba odbiotu informacji od serwera
        received_data = radio_module.receive()
        if received_data != None:
            print(received_data)
            received_data = received_data[:-3]
            print(received_data)
        if received_data == [0,1,2,3,4,5]:
            print("Server radio connection reset")
            current_time_radio_serv = start_time_radio_serv
        if received_data == [4,4,4,4,4,4]:
            if freq != 433:
                radio_module.frequency_433()
                freq = 433
                freq_conn_test = True
        if received_data == [8,8,8,8,8,8]:
            if freq != 868:
                radio_module.frequency_868()
                freq = 868
                freq_conn_test = True

        if freq_conn_test:
            if received_data == [1,1,1,1,1,1]:
                freq_conn_test = False
                freq_conn_test_counter = 0
            else:
                freq_conn_test_counter = freq_conn_test_counter + 1
            if freq_conn_test_counter == 5:
                if freq == 433:
                    radio_module.frequency_868()
                    freq = 868
                elif freq == 868:
                    radio_module.frequency_433()
                    freq = 433
        
        # Jezeli brak informacji od serwera po 180 sekundach zmień częstotliwość
        if start_time_radio_serv - current_time_radio_serv > 180:
            current_time_radio_serv = start_time_radio_serv
            if freq == 433:
                radio_module.frequency_868()
                freq = 868
            elif freq == 868:
                radio_module.frequency_433()
                freq = 433
            #print("Zmieniono częstotliwość")

        #time.sleep(1)
        print(received_data)
        
    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
client.loop_stop()
client.loop_forever()