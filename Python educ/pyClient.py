import socket

HEADER = 64
PORT = 6666
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = ""


print("STARTING\n")
SERVER = input("Enter ip: ")
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

while True:
    msg = input("Type exit() to exit.\nyour message: ")

    if msg == "exit()":
        break

    send(msg)

send(DISCONNECT_MESSAGE)