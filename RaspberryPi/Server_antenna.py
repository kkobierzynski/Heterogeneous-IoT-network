from cc1101 import CC1101
import time
import json

data = {}
radio_module = CC1101()
radio_module.prepare()


for x in range(2000):
    data["Second"] = x
    json_data = json.dumps(data)
    print(json_data)
    rxbytes = radio_module.rxbytes_status()
    print(rxbytes)
    x = radio_module.receive()
    rxbytes = radio_module.rxbytes_status()
    print(rxbytes)
    print(x)
    time.sleep(1)