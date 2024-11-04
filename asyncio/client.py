import asyncio
from db import register_user, authenticate_user

class Client():
    def __init__(self, username, password, host = '63.176.122.3', port = 6666):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.client = None 

    async def start_client(self):
        self.client = asyncio.open_connection(
            self.host,
            self.port
            #ssl_handshake_timeout ilerde ayarlanacak!!!
        )

if __name__ == '__main__':
    myClient = Client()
    action = input("Do you want to register (r) or login (l)? ")
    nickname = input("Enter your nickname: ")
    password = input("Enter your password: ")
    
    if action == 'r':
        if register_user(nickname, password):
            print("You can now login.")
        else:
            print("Registration failed.")
    elif action == 'l':
        if authenticate_user(nickname, password):
            print("Connecting to server...")
            myClient.start_client()
        else:
            print("Login failed.")