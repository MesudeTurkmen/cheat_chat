import socket
import threading
import subprocess
import os

PORT = 6666
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = ""
username = ''
password = ''

def listen_to_server(client, username):
    new_cmd = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE, text=True)
    while True:
        message = client.recv(2048).decode('utf-8')
        if message == "ACCESS_APPROVED!":
            print("[CONNECTED] Access Approved!")
            threading.Thread(target=texting, args=(client,username,)).start()
        elif message != '':
            index = message.find('~')
            sender_name = message[:index]
            msg = message[index + 1:]
            final_msg = f"{sender_name}:{msg}"
            new_cmd.stdin.write(final_msg)      # Write the message to the CMD window
            new_cmd.stdin.flush()               # Ensure it's sent immediately
            continue
        else:
            client.close()

def clear():    # Clears the terminal
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/MacOS
        os.system('clear')

def send(msg, client):
    if msg != DISCONNECT_MESSAGE:
        msg = f"{username}~{msg}"
    client.sendall(msg.encode(FORMAT))

def texting(client,username):
    print("You can type exit() to exit.")
    while True:
        msg = input(f"{username}:~")
        if msg == "exit()":
            break
        send(msg, client)
        clear()
    client.sendall(DISCONNECT_MESSAGE.encode(FORMAT))

def main():
    SERVER = input("Enter ip: ")
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((SERVER,PORT))
    except:
        print(f"[ERROR!] Unable to connect to the server {SERVER} {PORT}")
    else:
        username = input("Username: ")
        password = input("Password: ")
        print("Waiting for the server...")
        authentication = f"{username},{password}"       #Preparing login message
        client.sendall(authentication.encode(FORMAT))
        threading.Thread(target=listen_to_server, args=(client, username,)).start()




if __name__ == '__main__':
    main()