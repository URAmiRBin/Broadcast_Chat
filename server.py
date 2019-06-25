import time, socket, sys
from threading import Thread
import tkinter
import random

senwords = ["shit", "fuck", "nigga", "anus"]
def censort(l):
    global senwords
    words = l.split(' ')                       #split the words into a list
    for i in range(len(words)):
        for j in range(len(senwords)):             #for each word in the text
            if senwords[j] in words[i]:                       #if it needs to be censoredx
                words[i] = "*"*len(senwords[j])            #replace it with X's
    x=" ".join(words)
    return x     
# ======================= TKINKER FUNCTIONS =======================
# When send button pressed, sends the text in textbox
# Event passed by binders
def send_event(event = None):
    text_field_output = text_field.get()
    text_field_output = censort(text_field_output)
    text_field.set("")
    if text_field_output == "[!q]":
        message = "has left the chat"
        connection.send(message.encode())
        # connection.close()
        top.quit()
        return
    connection.send(bytes(text_field_output, "utf8"))
    message3 = "You > {}".format(text_field_output)
    messages_list.insert(tkinter.END, message3)


# Close Window Event
def on_closing(event=None):
    message = "has left the chat"
    connection.send(message.encode())
    # connection.close()
    top.quit()
    sys.exit(0)

# ======================= CLI FUNCTIONS =======================
def menu(start):
    if action == "1":
        get_port = udp_broadcaster_sender()
        if get_port is False:
            print("No one responded")
            print("Going back to main menu")
            sleep(1)
            menu(False)
        else:
            return get_port, 0
    elif action == "2":
        addr, my_port = udp_listener_receiver()
        if addr is False:
            print("Couldn't Find anyone")
            print("Going back to main menu")
            sleep(1)
            menu(False)
        else:
            return addr, my_port


# ======================= NETWORK FUNCTIONS =======================
# recv function recieves messages and runs sepretaly on a thread
def recv():
    while True:
        message = connection.recv(1024)
        message = message.decode()
        message2 = "{} > {}".format(name2, message) 
        if "has left" in message2:
            connection.close()
            top.quit()
            sys.exit(0)
        messages_list.insert(tkinter.END, message2)


# ======================= BROADCAST FUNCTIONS =======================
def udp_broadcaster_sender():
    # Creates a UDP socket on port 2222
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)
    server.bind(("", PORT1))
    message = b"hello"
    scounter = 0
    # broadcasts datagram message hello on port 3333
    print("BROADCASTING ...")
    while scounter < 8:
        scounter += 1
        server.sendto(message, ('<broadcast>', PORT2))
        time.sleep(0.5)
    print("FINISHED BROADCASTING")
    # Listens on port 4444 to find target
    print("STARTIN LISTENING")
    port = udp_broadcaster_receiver()
    return port


def udp_broadcaster_receiver():
    # Creates a UDP Socket on port 4444 to listen
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", PORT3))
    # Gets target data and address
    client.settimeout(5)
    data, addr = client.recvfrom(1024)
    # Listens to find message "im ready on port"
    if b'im ready on port' in data:
        numbers = [int(s) for s in data.split() if s.isdigit()]
        port = numbers[0]
        print("Target found")
        print("Port Requested: ", port)
        return port
    print("NO ONE FOUND")
    return False
    

# ======================= LISTENER FUNCTIONS =======================
def udp_listener_receiver():
    # Create a UDP socket on port 33333 to listen
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", PORT2))
    client.settimeout(5)
    # Listens to find message "hello"
    try:
        data, addr = client.recvfrom(1024)
        if data == b'hello':
            print("listener found someone")
            # if found "hello", sends a port to target to connect
            print(addr)
            my_port = udp_listener_sender(addr)
            return addr[0], my_port
    except socket.error:
        print("SOCKET ERROR")
    return False


def udp_listener_sender(addr):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)
    STATIC_PORT = random.randint(1024,65535)
    str1 = "im ready on port "
    str2 = str(STATIC_PORT)
    message_str = str1 + str2
    print(message_str)
    server.bind(("", STATIC_PORT))
    message = str.encode(message_str)
    scounter = 0
    try:
        while scounter < 7:
            scounter += 1
            server.sendto(message, (addr[0], PORT3))
            time.sleep(0.7)
    except socket.error:
        print("SOCKET ERROR SENDING")
    return STATIC_PORT


# ======================= MAIN =======================
# Tkinker Initialaztion
top = tkinter.Tk()
top.title("Chatbox")
top.option_add('*font', ('IRANSansWeb', 12))
top.geometry("320x480")
# Frame and field
messages_frame = tkinter.Frame(top)
text_field = tkinter.StringVar()
text_field.set("")
# Scrollbar for more messages
scrollbar = tkinter.Scrollbar(messages_frame)
# Chat windows
messages_list = tkinter.Listbox(messages_frame, height=15, width=30, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
messages_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages_list.pack()
messages_frame.pack()
entry_field = tkinter.Entry(top, textvariable=text_field)
entry_field.bind("<Return>", send_event)
entry_field.pack(side=tkinter.LEFT, expand = tkinter.YES)
send_button = tkinter.Button(top, text="Send", command=send_event)
send_button.pack(side=tkinter.RIGHT)
top.protocol("WM_DELETE_WINDOW", on_closing)

# Static Variables
PORT1 = 2222
PORT2 = 3333
PORT3 = 4444
# Menu inputs
action = sys.argv[1]
name = sys.argv[2]
menu_out, my_port = menu(True)


# Menu actions
if action == "1": 
    print("SERVER INIT")
    time.sleep(1)
    # Gets Server IP and Port and binds
    server_socket = socket.socket()
    host_name = socket.gethostname()
    ip = socket.gethostbyname(host_name)
    port = menu_out
    server_socket.bind((host_name, port))
    print(host_name, '({})'.format(ip))
    # Waits on given port for someone to connect
    server_socket.listen(1)
    print("Waiting ...")
    connection, addr = server_socket.accept()
    # Gets name
    name2 = connection.recv(1024)
    name2 = name2.decode()
    connection.send(name.encode())
    
elif action == "2":
    print("CLIENT INIT")
    time.sleep(1)
    # Gets Client IP and Port and connects
    connection = socket.socket()
    shost = socket.gethostname()
    ip = socket.gethostbyname(shost)
    # Gets server information
    print(shost, '({})'.format(ip))
    server_host = menu_out
    port = my_port
    print("connecting to the server: {}, ({})".format(server_host, port))
    time.sleep(1)
    connection.connect((server_host, port))
    connection.send(name.encode())
    name2 = connection.recv(1024)
    name2 = name2.decode()
recv_thread = Thread(target = recv)
recv_thread.start()
tkinter.mainloop()
