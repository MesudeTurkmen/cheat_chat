import socket
import threading


PORT = 6666
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = ""
username = ''
password = ''

def listen_to_server(client):
    while True:
        message = client.recv(2048).decode('utf-8')
        if message == "ACCESS_APPROVED!":
            print("[CONNECTED] Access Approved!")
        elif message != '':
            final_msg = f"{username}~{message}"
            print(final_msg)
        else:
            print(f"{username}~  ")

def send(msg, client):
    if msg != DISCONNECT_MESSAGE:
        msg = f"{username}~{msg}"
    client.sendall(msg.encode(FORMAT))

def main():
    SERVER = input("Enter ip: ")
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        client.connect((SERVER,PORT))
        print("[CONNECTED] Successfully connected to server.")
    except:
        print(f"[ERROR!] Unable to connect to the server {SERVER} {PORT}")
    else:
        username = input("Username: ")
        password = input("Password: ")
        authentication = f"{username},{password}"       #Preparing login message
        client.sendall(authentication.encode(FORMAT))
        threading.Thread(target=listen_to_server, args=(client, )).start()

    print("Type exit() to exit.")
    while True:
        msg = input("Message: ")
        if msg == "exit()":
            break
        send(msg, client)
    send(DISCONNECT_MESSAGE)

if __name__ == '__main__':
    main()