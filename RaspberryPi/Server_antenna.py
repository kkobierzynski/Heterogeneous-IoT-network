
import time
import json

data = {}

for x in range(5):
    data["Second"] = x
    json_data = json.dumps(data)
    print(json_data)
    time.sleep(1)