#Importing Libraries
import socket
import threading
import json
import os
#______________________________________________________________________

#Loading Predefined Credentials
with open("predefined_credentials.txt","r") as file:
    valid_credentials = json.load(file)
#______________________________________________________________________

#Creating Server Configurations 
SERVER =  '3.72.107.47'            #socket.gethostbyname(socket.gethostname())     #Get machine's IP address
PORT = 6666                                             #Setting port
LIMIT = 0                                               #Server's limit default set to 0
FORMAT = 'utf-8'                                        #Encyption format set to utf-8
DISCONNECT_MESSAGE = '!DISCONNECT'                      
#______________________________________________________________________

#Storing Sessions And Messages
ACTIVE_SESSIONS = []                                   #Stores active client_socket objects
ACTIVE_USERS = []                                      #Stores active user's usernames
ACTIVE_IPS = []                                        #Stores active users ip address
CHAT_HISTORY = []                                      #Stores the messages sent to the chat
#______________________________________________________________________

#Clears The Terminal
def clear():
    if os.name == 'nt': #For Windows
        os.system('cls')
    else: #For Unix/Linux/MacOS
        os.system('clear')
#______________________________________________________________________

#Displays menu options
def display_menu(menu):
    match menu:
        case 'server_config':
            print("1) Set Server Limit")
            print("2) Change Port")
            print("3) Run Server")
#______________________________________________________________________

#Validates user input for menu options
def get_user_choice(menu):
    while True:
        clear()
        display_menu(menu)
        choice = input("Your choice: ")
        if choice in ['1', '2','3']:
            return choice
        print("\nPlease enter a valid number (1-3).")
        input("Press ENTER to continue...")
#______________________________________________________________________

#Handles setting the server limit
def set_server_limit():
    global LIMIT
    while True:
        clear()
        limit_input = input("\nMaximum Limit can be set to 20!\nSet the new server limit: ")
        if limit_input.isdigit() and 1 <= int(limit_input) <= 20:
            LIMIT = int(limit_input)
            print(f"New Limit: {LIMIT}")
            break
        print(f"[ERROR!] '{limit_input}' is an invalid input.")
        input("Press ENTER to continue...")
#______________________________________________________________________

#Changes the assigned default PORT value 
def set_new_port():
    global PORT
    while True:
        clear()
        Port_input = input("\nMake sure to enter a valid Port.\nSet the new port to: ")
        if Port_input.isdigit() and 1024 <= int(Port_input) <= 65535:
            PORT = int(Port_input)
            print(f"New Port: {PORT}")
            break
        print(f"[ERROR!] '{Port_input}' is an invalid Port input")
        input("Press ENTER to continue...")
#______________________________________________________________________

#Change The Server Configurations
#Finally Run The Server
## Main configuration loop
def server_config():
    while True:
        choice = get_user_choice('server_config')
        match choice:
            case '1':
                set_server_limit()
                continue
            case '2':
                set_new_port()
                continue
            case '3':
                print("Running the server...")
                break  # Exit the loop and start the server
            case _:
                continue
#______________________________________________________________________

#Sends the message to the corresponding client_socket object (also encodes)
def send_message_to_client(client_socket, message):
    client_socket.sendall(message.encode(FORMAT))
#______________________________________________________________________

#Loops through every active client_socket object 
#Finally sending every single message to ever single user
def send_messages_to_all(message):
    for client in ACTIVE_SESSIONS:
        send_message_to_client(client, message)
#______________________________________________________________________

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
#______________________________________________________________________
  
    # Getting the authentication credentials
    #Authenticating...
    #The session will be terminated if the credentials 
    #do not match the predefined_credentials.
def godfry_authenticate(client_socket, address):

    credentials = client_socket.recv(64).decode(FORMAT)
    username = credentials.split(',')[0]
    password = credentials.split(',')[1]
    #Checks username in predefined_credentials.
    if username not in valid_credentials:
        auth_condition = "Invalid Username!"
        return
    #Checks the password of the username in predefined_credentials.
    elif valid_credentials[username] != password:
        auth_condition = "Invalid Password!"
        return
    #Checks the connection status of the username.
    elif username in ACTIVE_USERS:
        auth_condition = "[ERROR] Access Denied!"
        return
    #Checks the client_socket connection status in ACTIVE_SESSIONS.
    elif client_socket in ACTIVE_SESSIONS:
        auth_condition = "[ERROR] Access Denied!"
        return
    #Checks the client's address's connection status in ACTIVE_IPS.
    elif address in ACTIVE_IPS:
        auth_condition = "[ERROR] Access Denied!"
        return
    #If all the conditions are met Approves the connection.
    else:
        auth_condition = "ACCESS_APPROVED!"
    #Sending server response
    send_message_to_client(client_socket, auth_condition)
    if auth_condition != "ACCESS_APPROVED!":
        client_socket.close()   #Terminates the socket connection
        print(f"[SERVER] Client {address} with {username} was kicked off due to invalid authentication. ")
        return
    else:
        print(f"[SERVER] Successfully connected to {username} {address[1]} {address[1]}\nListening.")
        prompt_message = f"SERVER~ {username} joined." 
        send_messages_to_all(prompt_message)            #Notifys the users of the newcommers
        ACTIVE_USERS.append(username)                   #Appends the username to the connected users's usernames
        ACTIVE_SESSIONS.append(client_socket)           #Appends the client_socket
        ACTIVE_IPS.append(address)                      #Appends the ip address
        threading.Thread(target=listen_for_messages, args=(client_socket)).start    #Starts a new thread for listening to the messages.
        #Actually starting a new thread here might be unnecessary because this function's functionality is aloready over
        #I might consider replacing the new thread with calling the function instead in the near future
#______________________________________________________________________

def client_handler(client_socket, address):
    # Server will listen for client messages here
    godfry_authenticate(client_socket, address)
#______________________________________________________________________

def main():
    #Socket class object being created
    #AF_INET stands for IPV4, SOCK_STREAM stands for TCP
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #server_config()

    try:
        server.bind((SERVER, PORT))
        server.listen(LIMIT)
        print(f"[ONLINE] The Server Is Running")
    except:
        print(f"[ERROR] Unable To Bind To {SERVER} {PORT}")
        exit()
    
    clear()
    input(f"[SERVER] Running The Server On {SERVER} {PORT}\nENTER...")

    while True:
        print("Listening...")
        client_socket, address = server.accept()
        print("[CONNECTING] Client {address[0]} {address[1]} Sent A Connection Request.")
        threading.Thread(target=client_handler, args=(client_socket, address)).start()
#______________________________________________________________________

if __name__ == "__main__":
    main()