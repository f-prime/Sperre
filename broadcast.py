import socket
import config
import json
import random

def send(command, output_wanted, output_as_array=False):
    nodes = config.nodes.find("nodes", {"relay":True})
    if nodes:
        nodes.append({"ip":config.master_dns, "port":7070})
        random.shuffle(nodes)
    else:
        nodes = [{"ip":config.master_dns, "port":7070}] # This is normally only needed when first running Sperre to sync with the network.
    output = [] #If output_as_array is True
    for node in nodes:
        if not node:
            continue
        
        ip = node["ip"]
        port = node["port"]
        
        sock = socket.socket()
        try:
            sock.settimeout(60)
            sock.connect((ip, port))
        except:
            sock.close()
            continue
        else:
            sock.send(json.dumps(command))
            if output_wanted:
                output = ""
                while True:
                    data = sock.recv(1024)
                    if not data:
                        sock.close()
                        break
                    output += data
                return output
            
            if output_as_array: # This was used when I had a different idea for the way the protocol would work. I have since moved away from that idea but kept it here because it may prove useful in the future for some reason.
                output_ = ""
                while True:
                    data = sock.recv(1024)
                    if not data:
                        sock.close()
                        if output:
                            output.append({"ip":ip, "port":port, "response":output_})
                        break
                    output_ += data
        sock.close()
    
    if output_as_array:
        return output
