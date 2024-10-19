#This is a studying sheet for python socket
#This time it is a server running on bluetooth

import socket
import threading
import time
import bluetooth
#_______________________________________________

"""HOST = "192.168.1.38" """                            #const, ipconfig in cmd

HEADER = 64                                             #const, 64bytes 
PORT = 6666                                             #const
HOST = socket.gethostbyname(socket.gethostname())     #finds the ipv4 address automaticlly
#ADDR = (SERVER, PORT)                                   #Tuple for binding the server
FORMAT = 'utf-8'                                        #encoding format
DISCONNECT_MESSAGE = "!DISCONNECT"          
BLUETOOTH = bluetooth.read_local_bdaddr()[0]            
#_______________________________________________


while True:
    choice = input("1)Run server on Internet\n2)Run server on Bluetooth\nYour choice: ")

    if choice == "1":
        SERVER = HOST  
        HOST_NAME = "Internet"
    elif choice == "2":
        SERVER = BLUETOOTH
        HOST_NAME = "Bluetooth"
        
    else:
        continue
    ADDR = (SERVER, PORT)  
    print(f"Local {HOST_NAME} Address: {SERVER}")
    break

#AF_INET for ipv4, SOCK_STREAM for TCP
server = socket.socket(socket.AF_BLUETOOTH, socket.BTPROTO_RFCOMM)
server.bind(ADDR) #socket being connected to the address

def handleClient(conns, addrs):
    print(f"[NEW CONNECTION ESTABLISHED] {addrs} connected.")

    connected = True
    while connected:
        msgLength = conns.recv(HEADER).decode(FORMAT)       #recieving the header msg.
        if msgLength:                                       #not null
            msgLength = int(msgLength)                          #converting to int
            msg = conns.recv(msgLength).decode(FORMAT)          #recieving the msg according to msg_length's size

            if msg == DISCONNECT_MESSAGE:
                connected = False                               #disconnecting...

            print(f"[{addrs}]: {msg}")                          #print the message and back into the loop
            conns.send("Msg received".encode(FORMAT))

    conns.close()                                           #connection terminated.
#_______________________________________________

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER} {PORT}")
    while True:
        conns, addrs = server.accept()
        thread = threading.Thread(target=handleClient, args=(conns, addrs))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}.")
#_______________________________________________


print("[STARTING] server is starting...")
start()


