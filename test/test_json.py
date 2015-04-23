import pyopencl as cl
import json

data = []
for platform in cl.get_platforms() :
    for device in platform.get_devices():
        data.append({"name":device.name.strip()})

en_data = json.dumps(data)

de_data = json.loads(en_data)

print de_data[0]['name']
