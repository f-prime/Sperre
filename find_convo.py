import config
import json
import thread
import socket
import re
from rsa import *
import aes
import base64

def find_convo(obj, data):
    config.relaying_to.append({"address":data['address'], "object":obj})

def send():
    address = config.my_data.find("data", "all")[0]['address']
    privatekey = config.my_data.find("data", "all")[0]["privatekey"]
    privatekey = filter(None, re.findall("[0-9]*", privatekey))
    privatekey = PrivateKey(int(privatekey[0]), int(privatekey[1]), int(privatekey[2]), int(privatekey[3]), int(privatekey[4]))
    sock = socket.socket()
    sock.connect(find_node())
    sock.send(json.dumps({"cmd":"find_convo", "address":address}))
    config.found_convo = True
    print "In contact with relay node"
    while True:
        data = sock.recv(1024000)
        if not data:
            config.found_convo = False
            break
        else:
            data += "\n"
            data = data.split("\n")
            for x in data:
                try:
                    x = json.loads(x)
                except ValueError:
                    continue
                from_ = x['from']
                message = base64.b64decode(x['message'])
                message = aes.decryptData(decrypt(base64.b64decode(x['key']), privatekey), message)
                print message
                
def find_node():
    nodes = config.nodes.find("nodes", {"relay":True})
    for x in nodes:
        ip, port = x['ip'], x['port']
        sock = socket.socket()
        try:
            sock.settimeout(60)
            sock.connect((ip, port))
        except:
            sock.close()
            continue
        else:
            sock.close()
            return (ip, port)


