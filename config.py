#This is the file that will have all the config files such as where to find nodes and all the database connections
import landerdb

version = "0.1.0"
my_data = landerdb.Connect("data.db")
nodes = landerdb.Connect("nodes.db")
cache = landerdb.Connect("cache.db") # This is the local data such as messages that aren't held on the network itself.
master_dns = "sperre.zapto.org"
host = "0.0.0.0"
port = 7070
conversation_servers = {} # address:server Used by the nodes that are looking to send messages in an already open conversation
relay = False
found_convo = False
relaying_to = [] # For relay nodes only, this is a list of active connections that the node is proxying messages to.
