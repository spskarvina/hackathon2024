import subprocess

def getList():
    test = subprocess.Popen(["bch", "node", "list"], stdout=subprocess.PIPE)
    output, _ = test.communicate()
    decoded_output = output.decode('utf-8')
    lines = decoded_output.splitlines()
    
    data = lines[2:]
    devices = []
    for line in data:
        device_id, alias = line.split(maxsplit=1)
        devices.append({"id": device_id, "alias": alias})
    return devices
