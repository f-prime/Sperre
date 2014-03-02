import broadcast

def get_nodes(obj, data):
    with open("nodes.db", "rb") as file:
        while True:
            data = file.read(1000)
            if data == "":
                break
            obj.send(data)
    
    obj.close()

def send():
    data = broadcast.send({"cmd":"get_nodes"}, True)
    with open("nodes.db", 'wb') as file:
        file.write(data)
