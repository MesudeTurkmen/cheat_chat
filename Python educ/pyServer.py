#This is a studying sheet for python socket

import socket
import threading
import time
#_______________________________________________

"""HOST = "192.168.1.38" """                            #const, ipconfig in cmd
#SERVER = "194.27.19.117"
HEADER = 64                                             #const, 64bytes 
PORT = 8080                                             #const
SERVER = socket.gethostbyname(socket.gethostname())     #finds the ipv4 address automaticlly
ADDR = (SERVER, PORT)                                   #Tuple for binding the server
FORMAT = 'utf-8'                                        #encoding format
DISCONNECT_MESSAGE = "!DISCONNECT"                      
#_______________________________________________


#AF_INET for ipv4, SOCK_STREAM for TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            conns.send(msg.encode(FORMAT))

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


  