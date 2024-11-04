import asyncio
from db import register_user, authenticate_user

class Client:
    def __init__(self, host='63.176.122.3', port=6666):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def start_client(self):
        try:
            self.reader, self.writer = await asyncio.open_connection(
                self.host,
                self.port
            )
            print("Connected to the server.")
            await asyncio.gather(
                self.send_message(),
                self.receive_message()
            )
        except Exception as e:
            print(f"Connection error: {e}")

    async def send_message(self):
        while True:
            message = input("You: ")
            if message.lower() == 'quit':
                print("Exiting chat.")
                self.writer.close()
                await self.writer.wait_closed()
                break
            
            if message:  # Boş mesaj gönderilmemesi için kontrol
                self.writer.write(message.encode())
                await self.writer.drain()  # Gönderme işleminin tamamlanmasını bekle

    async def receive_message(self):
        while True:
            try:
                data = await self.reader.read(1024)  # Sunucudan gelen mesajı oku
                if data:
                    print(f"Server: {data.decode()}")
                else:
                    print("Server closed the connection.")
                    self.writer.close()
                    await self.writer.wait_closed()
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

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
            try:
                asyncio.run(myClient.start_client())
            except KeyboardInterrupt:
                print("Client interrupted by user")
        else:
            print("Login failed.")
