from cc1101 import CC1101
import time
import json

data = {}
test = CC1101()
test.prepare()


for x in range(2000):
    data["Second"] = x
    json_data = json.dumps(data)
    print(json_data)
    test.read_test()
    if x%5 == 0:
        test.strobes_write(0x34)
    if x%5 == 4:
        y = test.read_burst_byte(0x3F, 7)
        print(y)
    #test.read_from_register_test25()
    time.sleep(1)