import time, socket, sys
from threading import Thread
import tkinter
import random

# ======================= TKINKER FUNCTIONS =======================
# When send button pressed, sends the text in textbox
# Event passed by binders
def send_event(event = None):
    text_field_output = text_field.get()
    text_field.set("Type here")
    if text_field_output == "[!q]":
        message = "has left the chat"
        connection.send(message.encode())
        connection.close()
        top.quit()
        return
    connection.send(bytes(text_field_output, "utf8"))
    message3 = "{} > {}".format(name, text_field_output)
    messages_list.insert(tkinter.END, message3)


# Close Window Event
def on_closing(event=None):
    message = "has left the chat"
    connection.send(message.encode())
    connection.close()
    top.quit()
    quit()


# ======================= CLI FUNCTIONS =======================
def menu(start):
    if start:
        print("Hello and welcome to Chatbox, Developed by @Amir_Bin")
    print("=================== MENU =================")
    print("1. Broadcast")
    print("2. Listen")
    print("3. Help")
    print("Press Numbers to start (1 or 2 or 3)")
    action = input(" > ")
    if action == "1":
        get_port = udp_broadcaster_sender()
        if get_port is False:
            print("No one responded")
            print("Going back to main menu")
            sleep(1)
            menu(False)
        else:
            return action, get_port, 0
    elif action == "2":
        addr, my_port = udp_listener_receiver()
        if addr is False:
            print("Couldn't Find anyone")
            print("Going back to main menu")
            sleep(1)
            menu(False)
        else:
            return action, addr, my_port
    else:
        print("First Run the broadcast then listener")
        print("WARNING: Broadcaster, broadcasts for about 4 seconds and if can't find someone crashes!!!!")
        print("Type in [!q] in chat to disconnect")

        input("Press Any key to go back to menu ")
        menu(False)


# ======================= NETWORK FUNCTIONS =======================
# recv function recieves messages and runs sepretaly on a thread
def recv():
    while True:
        message = connection.recv(1024)
        message = message.decode()
        message2 = "{} > {}".format(name2, message) 
        messages_list.insert(tkinter.END, message2)


# ======================= BROADCAST FUNCTIONS =======================
def udp_broadcaster_sender():
    # Creates a UDP socket on port 22222
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)
    server.bind(("", 22222))
    message = b"hello"
    scounter = 0
    # broadcasts datagram message hello on port 33333
    print("BROADCASTING ...")
    while scounter < 7:
        scounter += 1
        server.sendto(message, ('<broadcast>', 33333))
        time.sleep(0.5)
    print("FINISHED BROADCASTING")
    # Listens on port 22221 to find target
    print("STARTIN LISTENING")
    port = udp_broadcaster_receiver()
    return port


def udp_broadcaster_receiver():
    # Creates a UDP Socket on port 22221 to listen
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", 22221))
    # Gets target data and address
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
    client.bind(("", 33333))
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
            server.sendto(message, (addr[0], int(addr[1]) - 1))
            time.sleep(0.7)
    except socket.error:
        print("SOCKET ERROR SENDING")
    return STATIC_PORT


# ======================= MAIN =======================
# Tkinker Initialaztion
top = tkinter.Tk()
top.title("Chatbox")
# Frame and field
messages_frame = tkinter.Frame(top)
text_field = tkinter.StringVar()
text_field.set("Type here")
# Scrollbar for more messages
scrollbar = tkinter.Scrollbar(messages_frame)
# Chat windows
messages_list = tkinter.Listbox(messages_frame, height=25, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
messages_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages_list.pack()
messages_frame.pack()
entry_field = tkinter.Entry(top, textvariable=text_field)
entry_field.bind("<Return>", send_event)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send_event)
send_button.pack()
top.protocol("WM_DELETE_WINDOW", on_closing)


# Menu inputs
action = ""
action, menu_out, my_port = menu(True)


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
    name = input("What's your name: ")
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
    name = input("What's your name: ")
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