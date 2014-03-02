import config
import json
import broadcast
import get_nodes

def get_nodes_count(obj, data):
    try:
        my_count = len(config.nodes.find("nodes", "all"))
    except TypeError:
        config.nodes.insert("nodes", {})
        config.nodes.save()
        my_count = len(config.nodes.find("nodes", "all"))

    output = {"response":my_count}
    obj.send(json.dumps(output))
    obj.close()

def send():
    try:
        check = len(config.nodes.find("nodes", "all"))
    except TypeError:
        config.nodes.insert("nodes", {})
        config.nodes.save()
        check = len(config.nodes.find("nodes", "all"))
    
    output = broadcast.send({"cmd":"get_nodes_count"}, True) #(to_send, output wanted)
    try:
        data = json.loads(output)
    except:
        print "Something went wrong with get_nodes_count send"
        return
    else:
        if data != "null" and data["response"] > check:
            get_nodes.send()
        
