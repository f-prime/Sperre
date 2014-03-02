import config
import json
import broadcast
import aes
from rsa import *
import re
import uuid
import base64

def send_message(obj, data):
    for x in config.relaying_to:
        if x['address'] == data['contact']:
            x['object'].send(json.dumps({"message":data['message'], "from":data['address'], "key":data['key']}))

def send(message, contact):
    data = config.my_data.find("data", "all")[0]
    target = config.nodes.find("nodes", {"address":contact})[0]
    address = data['address']
    public_key = filter(None, re.findall("[0-9]*", target['publickey'])) #Safe way of extracting the public key from a string
    public_key = PublicKey(int(public_key[0]), int(public_key[1])) # Re build public key
    key = uuid.uuid4().hex  # Generate AES key
    k = encrypt(key, public_key) #Encrypt the key with the RSA public key of the target
    k = base64.b64encode(k) #Encode the encrypted data
    message = base64.b64encode(aes.encryptData(key, message)) #Encrypt the message with the AES key and then encode it
    broadcast.send({"cmd":"send_message", "message":message, "contact":contact, "address":address, "key":k}, False) #Broadcast the message
