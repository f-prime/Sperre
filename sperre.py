from bottle import *
import config
import send_message
import thread
import client

@route("/")
def index():
    my_address = config.my_data.find("data", "all")[0]["address"]
    messages = config.cache.find("messages", "all")
    if not messages:
        messages = []
    names = []
    out = []
    for x in messages:
        if x['from'] not in names:
            names.append(x['from'])
            data = {}
            data["from"] = x['from']
            data['message'] = x['message']
            out.append(data)
    
    return jinja2_template("templates/index.html", messages=out, my_address=my_address)

@route("/conversation/<address>")
def conversation(address):
    my_address = config.my_data.find("data", "all")[0]["address"]
    messages = config.cache.find("messages", {"from":address})
    if not messages:
        messages = []
    sent = config.cache.find("sent", {"contact":address})
    if not sent:
        sent = []
    conversation = messages + sent
    conversation = sorted(conversation, key=lambda x:x['time'])
    return jinja2_template("templates/conversation.html", my_address=my_address, messages=conversation)

@route("/conversation/<address>", method="POST")
def send_message_form(address):
    message_ = request.forms.get("message")
    if message_:
        thread.start_new_thread(send_message.send, (message_,  address))
        redirect("/conversation/"+address)


@route("/startconvo/")
def start_convo():
    return jinja2_template("templates/start_convo.html")

@route("/startconvo/", method="POST")
def start_convo_form():
    address = request.form.get("address")
    check = config.nodes.find("nodes", {"address":address})
    if not check:
        return "Address does not exist."
    else:
        redirect("/conversation/"+address)


if __name__ == "__main__":
    thread.start_new_thread(client.run, ())
    run(host="localhost", port="4321", debug=True)
