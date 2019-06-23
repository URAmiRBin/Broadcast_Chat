import time, socket, sys
from threading import Thread
import tkinter
import random

# ======================= TKINKER FUNCTIONS =======================
# When send button pressed, sends the text in textbox
# Event passed by binders
def send_event(event=None):
    text_field_output = text_field.get()
    text_field.set("Type here")
    if text_field_output == "[!q]":
        message = "has left the chat"
        connection.send(message.encode())
        connection.close()
        top.quit()
        return
    connection.send(bytes(text_field_output, "utf8"))
    msg_list.insert(tkinter.END, (name, '>', text_field_output))


# Close Window Event
def on_closing(event=None):
    text_field.set("[!q]")
    send()


# ======================= CLI FUNCTIONS =======================
def menu(start):
    if start:
        print("Hello and welcome to Chatbox, Developed by @Amir_Bin")
    print("=================== MENU =================")
    print("1. Broadcast")
    print("2. Listen")
    print("Press Numbers to start (1 or 2)")
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


# ======================= NETWORK FUNCTIONS =======================
# recv function recieves messages and runs sepretaly on a thread
def recv():
    while True:
        message = connection.recv(1024)
        message = message.decode()
        message = message[1 : -1]
        msg_list.insert(tkinter.END, (name2, '>', message))


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
        time.sleep(1)
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
    

# ======================= BROADCAST FUNCTIONS =======================
def udp_listener_receiver():
    # Create a UDP socket on port 33333 to listen
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", 33333))
    rcounter = 0
    # Listens to find message "hello"
    try:
        while rcounter < 7:
            rcounter += 1
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
    # message = b"im ready on port 1234"
    message = str.encode(message_str)
    scounter = 0
    try:
        while scounter < 7:
            scounter += 1
            server.sendto(message, (addr[0], int(addr[1]) - 1))
            time.sleep(1)
    except socket.error:
        print("SOCKET ERROR SENDING")
    return STATIC_PORT


# ======================= MAIN =======================
# Tkinker Initialaztion
top = tkinter.Tk()
top.title("Chatter")
messages_frame = tkinter.Frame(top)
text_field = tkinter.StringVar()
text_field.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
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
    print('Setup Server...')
    time.sleep(1)
    #Get Server Information
    soc = socket.socket()
    host_name = socket.gethostname()
    ip = socket.gethostbyname(host_name)
    port = menu_out
    soc.bind((host_name, port))
    print(host_name, '({})'.format(ip))
    name = input('Enter name: ')
    soc.listen(1)
    print('Waiting for incoming connections...')
    connection, addr = soc.accept()
    print("Received connection from ", addr[0], "(", addr[1], ")\n")
    print('Connection Established. Connected From: {}, ({})'.format(addr[0], addr[0]))
    #get a connection from client side
    name2 = connection.recv(1024)
    name2 = name2.decode()
    print(name2 + ' has connected.')
    print('Press [!q] to leave the chat room')
    connection.send(name.encode())
    
elif action == "2":
    print('Client Server...')
    time.sleep(1)
    #Get the hostname, IP Address from socket and set Port
    connection = socket.socket()
    shost = socket.gethostname()
    ip = socket.gethostbyname(shost)
    #get information to connect with the server
    print(shost, '({})'.format(ip))
    # server_host = input('Enter server\'s IP address:')
    server_host = menu_out
    name = input('Enter Client\'s name: ')
    port = my_port
    print('Trying to connect to the server: {}, ({})'.format(server_host, port))
    time.sleep(1)
    connection.connect((server_host, port))
    print("Connected...\n")
    connection.send(name.encode())
    name2 = connection.recv(1024)
    name2 = name2.decode()
    print('{} has joined...'.format(name2))
    print('Enter [!q] to exit.')
recv_thread = Thread(target = recv)
recv_thread.start()
tkinter.mainloop()