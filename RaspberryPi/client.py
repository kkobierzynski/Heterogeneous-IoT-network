import paho.mqtt.client as mqtt
import json
import time
import SysInfo

#----------DATA STRUCTURES--------
data = {"Data":{},
        "Network":{},
        }



#---------------GLOBAL VARIABLES---------------
mqtt_username = "myuser"
mqtt_password = "raspberrypi"
mqtt_broker_ip = "192.168.0.220"
current_time = 0
flag_connected_mqtt = False
flag_radio = False
serial = SysInfo.BoardInfo.serial()
model = SysInfo.BoardInfo.model()


#---------TOPICS-----------
topic_data = "kitchen/data"
topic_sub_led = "kitchen/led"




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



#--------------------------------------------
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.username_pw_set(username=mqtt_username, password=mqtt_password)
client.connect(mqtt_broker_ip, 1883, 60)
client.loop_start()

while True:
    start_time = time.time() 

    if start_time-current_time > 1 and flag_connected_mqtt:
        print("mqtt_connection")
        current_time = start_time
        temperature = 20    # ZAMIENIĆ NA ODCZYTYWANIE Z CZUJNIKA
        humidity=40     # ZAMIENIĆ NA DOCZYTYWANIE Z CZUJNIKA
        rssi = SysInfo.NetworkInfo.rssi()
        ssid = SysInfo.NetworkInfo.ssid() #wrzucić w miejsce ponownego połączenia z wifi, tutaj bez sensu marnotractwo zasobów by liczyć to co każdą sekundę


        data["Data"]["Temperature"] = temperature
        data["Data"]["Humidity"] = humidity
        data["Network"]["Wifi_name"] = ssid
        data["Network"]["Server_ip"] = mqtt_broker_ip
        data["Network"]["Signal_strength"] = rssi
        data["SensorID"] = serial
        data["Sensor_Model"] = model

        json_data = json.dumps(data)
        client.publish(topic_data, json_data)
        print(json_data)
    elif start_time-current_time > 1 and flag_radio:
        current_time = start_time
        print("radio_connection")
    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
client.loop_stop()
client.loop_forever()