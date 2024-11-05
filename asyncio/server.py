import asyncio
from db import User

class Server:
    def __init__(self, host='0.0.0.0', port=6666):
        self.host = host
        self.port = port
        self.server = None
        self.clients = {}  # Client ile nickname eşleşmesi için dict kullanıyoruz
  
    async def start_server(self):
        self.server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print('Server activated...')
    
        async with self.server:
            await self.server.serve_forever()

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Connection established with {addr}")
        self.clients.append(writer)
    
        try:
            writer.write(b"Enter your nickname: ")
            await writer.drain()
            
            # Nickname'i okuma
            nickname = (await reader.read(1024)).decode().strip()
            print(f"{nickname} has joined the chat.")
            
            while True:
            data = await reader.read(100)
            if not data:
                print(f"Connection closed by {addr}")
                break

            message = data.decode()
            print(f"{nickname}: {message}")

            # Mesajı diğer kullanıcılara yayma
            broadcast_message = f"{nickname}: {message}".encode()
            await asyncio.gather(*(self.send_to_client(client, broadcast_message) for client in self.clients if client != writer))
    
        except Exception as e:
            print(f"Error with client {addr}: {e}")
    
        finally:
            print(f"Closing connection with {addr}")
            writer.close()
            await writer.wait_closed()
            # Burada writer'ı clients listesinden çıkarıyoruz.
            if writer in self.clients:
            self.clients.remove(writer)


    async def send_to_client(self, client, data):
        client.write(data)
        await client.drain()

if __name__ == '__main__':
    myServer = Server()
    try:
        asyncio.run(myServer.start_server())
    except KeyboardInterrupt:
        print("Server interrupted by user")  
