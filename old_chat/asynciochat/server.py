import asyncio

class Server:
    def __init__(self, host='0.0.0.0', port=6666):
        self.host = host
        self.port = port
        self.server = None
        self.clients = {}  # Dictionary to hold nickname and writer

    async def start_server(self):
        self.server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print('Server activated...')
    
        async with self.server:
            await self.server.serve_forever()

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Connection established with {addr}")
        
        # Prompt user for nickname
        writer.write(b"Enter your nickname: ")
        await writer.drain()

        # Read nickname
        nickname = (await reader.read(100)).decode().strip()
        print(f"{nickname} has joined the chat.")
        
        # Store the client with their nickname
        self.clients[nickname] = writer

        try:
            while True:
                data = await reader.read(100)

                if not data:
                    print(f"Connection closed by {addr}")
                    break

                message = data.decode()
                print(f"{nickname}: {message}")

                # Broadcast message to other clients
                broadcast_message = f"{nickname}: {message}".encode()
                await asyncio.gather(*(self.send_to_client(client, broadcast_message) for nick, client in self.clients.items() if nick != nickname))

        except Exception as e:
            print(f"Error with client {addr}: {e}")

        finally:
            print(f"Closing connection with {addr}")
            writer.close()
            await writer.wait_closed()
            del self.clients[nickname]  # Remove client from the dictionary

    async def send_to_client(self, client, data):
        client.write(data)
        await client.drain()

if __name__ == '__main__':
    myServer = Server()
    try:
        asyncio.run(myServer.start_server())
    except KeyboardInterrupt:
        print("Server interrupted by user")
