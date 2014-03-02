
import config
import send_message
import thread

def start():
    while True:
        cmd = raw_input("> ")
        cmd = cmd.split()
        if cmd[0] == "send_message":
            send_message.send(cmd[1], cmd[2])

        elif cmd[0] == "addr":
            print config.my_data.find("data", "all")[0]["address"]
