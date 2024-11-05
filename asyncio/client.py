import asyncio
from db import register_user, authenticate_user

class Client:
    def __init__(self, nickname, host='63.176.122.3', port=6666):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.nickname = nickname

    async def start_client(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        print("Connected to the server.")

        # İlk olarak sunucuya nickname'i gönderiyoruz
        self.writer.write(self.nickname.encode())
        await self.writer.drain()

        await asyncio.gather(self.send_message(), self.receive_message())

    async def send_message(self):
        while True:
            message = input(f"{self.nickname}: ")
            full_message = f"{self.nickname}: {message}"
            self.writer.write(full_message.encode())
            await self.writer.drain()
            if message.lower() == 'quit':
                print("Exiting chat.")
                self.writer.close()
                await self.writer.wait_closed()
                break

    async def receive_message(self):
        while True:
            data = await self.reader.read(1024)
            if data:
                incoming_message = data.decode()
                
                display_message = incoming_message
                    
                print(display_message)
            else:
                print("Server closed the connection.")
                self.writer.close()
                await self.writer.wait_closed()
                break

if __name__ == '__main__':
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
            client = Client(nickname)
            try:
                asyncio.run(client.start_client())
            except KeyboardInterrupt:
                print("Client interrupted by user")
        else:
            print("Login failed.")
