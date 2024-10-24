import socket
import threading
import json
import os

#Loading user info
with open("predefinedCredentials.txt","r") as file:
    valid_credentials = json.load(file)

SERVER = socket.gethostbyname(socket.gethostname())     #Get machine's ip address
PORT = 6666                                             
LIMIT = 0                                               #Server Limit's default value set to 1
ADDR = (SERVER, PORT)                                   #Tuple for binding the server
FORMAT = 'utf-8'                                        #Encryption format
DISCONNECT_MESSAGE = "!DISCONNECT"
ACTIVE_SESSIONS = []                                    #Connected clients' list
ACTIVE_USERS = []                                       #Connected users' list of usernames
ACTIVE_IPS = []                                         #Connected users' list of ips
CHAT_HISTORY = []                                       #Chat Log (list). To be saved to a txt later.

def clear():    # Clears the terminal
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/MacOS
        os.system('clear')

def admin_logIn():
    #Admin's menu
    while True:
        while True:
            clear()
            choice = input("1) Set Server Limit\n2) Run Server\n\nYour choice: ")
    
            #Check if the choice is within expected values
            if choice in ['1', '2']:
                break  # Exit the loop if the input is valid
            else:
                input("Please enter a valid number (1 or 2).\nPress ENTER...")
                clear()

        if choice == '1':   #Resetting the server Limit
            global LIMIT
            Limit = input("\n\nMaximum Limit can be set to 20!\n set the new server limit: ")
            if Limit.isdigit() and int(Limit) <= 20:
                LIMIT = int(Limit)
                print(f"New Limit: {LIMIT}")
                continue
            else:
                input(f"[ERROR!] {Limit} Is An Invalid Input.\nPress ENTER To Continue...")
                continue
        clear()
        break

# Sending Message To Given Client
def send_message_to_client(client, message):
    client.sendall(message.encode(FORMAT))

# Function to send any new message to all the clients that
# are currently connected to this server
def send_messages_to_all(message):
    for user in ACTIVE_SESSIONS:
        send_message_to_client(user, message)

# Function to listen for upcoming messages from a client
def listen_for_messages(client, username):
    while True:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
            CHAT_HISTORY.append(final_msg)
        else:
            print(f"The message send from client {username} is empty")

def godfry_authenticate(username, password):
    # Commparing username and password with predefined credentials dict
    # Checking within currently connected users
    if username in valid_credentials and valid_credentials[username] == password:
        if username not in ACTIVE_USERS:
            response = "ACCESS_APPROVED!"
    else:
        response = "ACCESS_DENIED!"
    return response

def client_handler(client, address):
    # Server will listen for client messages here
    # Getting the authentication credentials
    credentials = client.recv(64).decode(FORMAT)
    username = credentials.split(',')[0]
    password = credentials.split(',')[1]

    # Authenticating. The session will terminate if the credentials do not match.
    response = godfry_authenticate(username, password)
    send_message_to_client(client, response)    # Delivering The Approval Message
    if response == "ACCESS_DENIED!":
        client.close()
        print(f"Client {address} with {username} username was kicked off due to invalid Authentication.")
        return
    elif response == "ACCESS_APPROVED!":
        print(f"[CONNECTED] Successfully connected to client {address[0]} {address[1]}\nListening...")

    prompt_message = "SERVER~" + f"{username} joined to the chat"
    send_messages_to_all(prompt_message)        # Announcing the new commers
    ACTIVE_USERS.append(username)
    ACTIVE_SESSIONS.append(client)
    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

def main():
    #Socket class object being created
    #AF_INET stands for IPV4, SOCK_STREAM stands for TCP
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    admin_logIn()
    try:    #ERROR Handling
        server.bind(ADDR)
        server.listen(LIMIT)    #Setting server's limit
        print(f"[ONLINE!] The Server Is Running")
    except:
        print(f"[ERROR!] Unable To Bind To {SERVER} {PORT}")
        
    clear()
    input(f"[SERVER] The Server Is Online On {SERVER} {PORT}\nMax Limit Is Set To {LIMIT}\nPress ENTER To Start Listening.")

    while True:
        print("Listening...")
        client, address = server.accept()
        print(f"[CONNECTING] Client {address[0]} {address[1]} Sent A Connection Request.")
        threading.Thread(target=client_handler, args=(client,address)).start()     #New thread to handle the new client

if __name__ == '__main__':
    main()          #Calling the main function