import socket
import threading
import os

# Socket sunucusu ayarları
SERVER = '0.0.0.0'            # Tüm IP'lerden gelen bağlantılara izin verir
PORT = 8080                 # Kullanacağınız port
LIMIT = 12                  #Temp just for now
FORMAT = "utf-8"            #Encryption format
DISCONNECT_MESSAGE = '!DISCONNECT'  
valid_credentials = ''

#Storing Sessions And Messages
ACTIVE_SESSIONS = []                           #Stores active client_socket objects
ACTIVE_USERS = []                              #Stores active user's usernames
ACTIVE_IPS = []                                #Stores active users ip address
CHAT_HISTORY = []                              #Stores the messages sent to the chat


def access_denied(client_socket, address, username):
    clear()
    send_message_to_client(client_socket, "[ERROR] Access Denied!")
    print(f"[SERVER] Client {address} with {username} was kicked off due to invalid authentication. ")
    clear()
    return

#Runs in a seperate thread
#Infinite loop, listens for upcoming messages from users
#Formats the message
#Redirects the formated message to send_messages_to_all
#Appends the formatted message to the CHAT_HISTORY
def listen_for_messages(client_socket, username):
    while True:
        message = client_socket.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
            CHAT_HISTORY.append(final_msg)
        else:
            print(f"The message sent from client {username} is empty")

def check_valid_credentials(username, password):
    if username not in valid_credentials or valid_credentials[username] != password:
        return

def is_user_active(username):
    if username not in ACTIVE_USERS:
        return
    
def is_session_in_use(client_socket):
    if client_socket not in ACTIVE_SESSIONS:
        return
    
def is_address_in_use(address):
    if address not in ACTIVE_IPS:
        return

def godfry_authenticate(client_socket, address):
    credentials = client_socket.recv(64).decode(FORMAT)
    username = credentials.split(',')[0]
    password = credentials.split(',')[1]

    if not check_valid_credentials(username, password,client_socket):
        if not is_user_active(username,client_socket):
            if not is_session_in_use(client_socket):
                if not is_address_in_use(address,client_socket):
                    return username

    if access_denied(client_socket, address, username):
        return 1

def send_message_to_client(client_socket, message):
    client_socket.sendall(message.encode(FORMAT))

def send_messages_to_all(message):
    for client in ACTIVE_SESSIONS:
        send_message_to_client(client, message)

def client_handler(client_socket, address):
    authenticate = godfry_authenticate(client_socket, address)
    if authenticate == 1:
        client_socket.close()       #Connection terminated
        return
    else:
        username = authenticate
        prompt_message = f"SERVER~ {username} joined." 

    send_message_to_client(client_socket, "ACCESS_APPROVED!")
    send_messages_to_all(prompt_message)            #Notifys the users of the newcommers
    ACTIVE_USERS.append(username)                   #Appends the username to the connected users's usernames
    ACTIVE_SESSIONS.append(client_socket)           #Appends the client_socket
    ACTIVE_IPS.append(address)                      #Appends the ip address
    threading.Thread(target=listen_for_messages, args=(client_socket, username)).start    #Starts a new thread for listening to the messages.
    #Actually starting a new thread here might be unnecessary because this function's functionality is aloready over
    #I might consider replacing the new thread with calling the function instead in the near future


#Clears The Terminal
def clear():
    if os.name == 'nt': #For Windows
        os.system('cls')
    else: #For Unix/Linux/MacOS
        os.system('clear')


def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        server.bind((SERVER,PORT))
        server.listen(LIMIT)
        print(f"[ONLINE] The Server Is Running...")
    except:
        print(f"[ERROR] Unable To Bind To {SERVER} {PORT}")
        exit()

    clear()
    print(f"[SERVER] Running The Server On {SERVER} {PORT}")

    while True:
        print("Listening...")
        client_socket, address = server.accept()
        print("[CONNECTING] Client {address[0]} {address[1]} Sent A Connection Request.")
        threading.Thread(target=client_handler, args=(client_socket, address)).start()



if __name__ == "__main__":
    main()
