
import config
import send_message
import thread
import cmd
import is_online
import timeago
import time

class SperreShell(cmd.Cmd):
    prompt = "SperreShell> "
    intro = "Welcome to the Sperre Shell!\n\n"

    def do_help(self, line):
        print """

            addr - Show address.
            readmessages <from> - Shows all the messages in order from an address.
            inbox - Shows list of address who are trying to contact you.
            sendmessage <address> <message>- Send a message to an address.
            isonline <address> - Check if an address is currently online in the network.

        """
    
    def do_isonline(self, address):
        print is_online.send(address)

    def do_addr(self, line):
        print config.my_data.find("data", "all")[0]["address"]

    def do_inbox(self, line):
        my_address = config.my_data.find("data", "all")[0]["address"]
        messages = config.cache.find("messages", "all")
        if not messages:
            messages = []
        names = []
        out = []
        messages.reverse()
        for x in messages:
            if x['from'] not in names:
                names.append(x['from'])
                timeago_ = timeago.timeago(int(time.time() - x['time']))
                print x['from']+" "+x['message'] + " " + str(timeago_['value']) +" "+str(timeago_['type'])+" ago"
    
    def do_sendmessage(self, line):
        line = line.split()
        address = line[0]
        message = ' '.join(line[1:])
        send_message.send(message, address)

    def do_readmessages(self, address):
        messages = config.cache.find("messages", {"from":address})
        if not messages:
            messages = []
        sent = config.cache.find("sent", {"contact":address})
        if not sent:
            sent = []
        conversation = messages + sent
        conversation = sorted(conversation, key=lambda x:x['time'])
        for x in conversation:
            if "from" in x:
                print "You: "+x['message']
            else:
                print "Friend: "+x['message']


if __name__ == "__main__":
    cmd_ = SperreShell()
    cmd_.cmdloop()

