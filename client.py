import socket
import get_nodes
import get_nodes_count
import register
import send_message
import find_convo
import thread
import json
import time
import rsa
import uuid
import config

class Sperre:
    def __init__(self):
        self.cmds = {
                "get_nodes":get_nodes.get_nodes,
                "get_nodes_count":get_nodes_count.get_nodes_count,
                "register":register.register,
                "send_message":send_message.send_message,
                "find_convo":find_convo.find_convo,

        } #This is where all the protocol commands will be held, they all point to some function that will process them.

    
    def first_run(self):
        print "Sperre seems to be running for the first time"
        print "Generating keys..."
        address = "SRE_"+uuid.uuid4().hex
        pubkey, privkey = rsa.newkeys(1024)
        config.my_data.insert("data", {"address":address, "publickey":str(pubkey), "privatekey":str(privkey)})
        config.my_data.save()
        print "Keys generated!"
        print "Getting node list..."
        get_nodes.send()
        print "Registering..."
        register.send()
        print "Registered!"
        print "Your address is: {0}".format(address)

    def relay(self):
        thread.start_new_thread(self.non_relay, ()) # Because a relay node is just a regular node that allows incoming connections as well
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((config.host, config.port))
        sock.listen(5)
        while True:
            obj, conn = sock.accept()
            thread.start_new_thread(self.relay_handle, (obj, conn[0]))

    def relay_handle(self, obj, ip):
        data = obj.recv(10240000) #The message may be long but it most likely will not
        if not data:
            obj.close()
            return
        else:
            try:
                data = json.loads(data) #Data is transfered in the JSON format, if it isn't JSON we will not continue trying to parse it.
            except:
                obj.close()
                return
            else:
                if "cmd" in data:
                    if data["cmd"] in self.cmds:
                        cmd = data['cmd']
                        del data['cmd']
                        data["ip"] = ip
                        self.cmds[cmd](obj, data) # Start the function that matches the command.


    def non_relay(self):
        register.send() #Re register with the network every time the node starts in case some of the config settings have changed.
        while True:
            if config.relay:
                for num,x in enumerate(config.relaying_to):
                    try:
                        x["object"].send(" ")
                    except:
                        config.relaying_to.pop(num)
            get_nodes_count.send()
            if not config.found_convo:
                thread.start_new_thread(find_convo.send, ())
            time.sleep(30)

    
def run():
    sperre = Sperre()

    if not config.my_data.find("data", {}):
        sperre.first_run()

    if config.relay:
        print "Sperre has started as a relay node on port {0}".format(config.port)
        sperre.relay()

    else:
        print "Sperre has started as a non relay node."
        sperre.non_relay()

if __name__ == "__main__":
    run()
