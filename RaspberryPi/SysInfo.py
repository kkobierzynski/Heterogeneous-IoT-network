import subprocess


class NetworkInfo:
    def ssid():
        #save command output to variable
        ssid = subprocess.check_output(['sudo', 'iwgetid'])
        ssid = ssid.split()
        ssid = ssid[1]
        ssid = ssid.decode("utf-8") #convert byte to string

        ssid = list(ssid)
        word = ""
        for character in ssid:
            if(character != '"'):
                word += character
            if(word == "ESSID:"):
                word = ""

        ssid = word
        return ssid

    def rssi():
        #read system file and save it to variable 
        with open("/proc/net/wireless",'r') as wireless_file:
            lines = wireless_file.read().splitlines()
            last_line = lines[-1]
            last_line_split = last_line.split() #split last line of file into segments
            rssi = last_line_split[3]   #select third segment where is information about rssi

            #deleting dot character
            rssi = list(rssi)   #changing to list of characters
            rssi.pop()  #deleting last character
            rssi_string = ""
            for character in rssi:  #changing list to string
                rssi_string += character
            rssi = int(rssi_string)
            return rssi

class BoardInfo:
    def serial():
        with open("/proc/cpuinfo",'r') as wireless_file:
            lines = wireless_file.read().splitlines()
            last_line = lines[-2]
            last_line_split = last_line.split()
            serial = last_line_split[2]
            return serial

    def model():
        with open("/proc/cpuinfo",'r') as wireless_file:
            lines = wireless_file.read().splitlines()
            last_line = lines[-1]
            last_line_split = last_line.split()
            length = len(last_line_split)
            model = ""
            for x in range(2,length):
                model += last_line_split[x]
            return model