import broadcast
import config

def is_online(obj, data):
    for x in config.relaying_to:
        if x['address'] == data['address']:
            obj.send("Yes")
            obj.close()
            return
    obj.close()

def send(address):
    out = broadcast.send({"cmd":"is_online", "address":address}, False, output_as_array=True)
    if out:
        return True
    else:
        return False
