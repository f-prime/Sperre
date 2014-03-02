import config 
import broadcast

def register(obj, data):
    
    check = config.nodes.find("nodes", {"address":data['address']})

    if check:
        check = check[0]
        check["relay"] = data["relay"]
        if check["relay"]:
            check["port"] = data["port"]
            check["ip"] = data["ip"]
        else:
            if "ip" in check:
                del check["ip"]
            if "port" in check:
                del check["port"]

        config.nodes.update("nodes", {"address":data['address']}, check)
    
    else:
        if not data['relay']:
            del data['ip']
            del data['port']
        config.nodes.insert("nodes", data)
    
    config.nodes.save()

def send():
    data = config.my_data.find("data", "all")[0]
    broadcast.send({"cmd":"register", "publickey":data["publickey"], "port":config.port, "relay":config.relay, "address":data["address"]}, False)
