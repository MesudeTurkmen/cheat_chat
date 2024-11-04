import asyncio

class Server:
    def __init__(self, host='0.0.0.0', port=6666):
        self.host = host
        self.port = port
        self.server = None
        self.clients = []
  
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
            while True:
                data = await reader.read(100)
                
                if not data:
                    print(f"Connection closed by {addr}")
                    break

                message = data.decode()
                print(f"{addr}: {message}")

                # Broadcast message using gather for concurrent sending
                await asyncio.gather(*(self.send_to_client(client, data) for client in self.clients if client != writer))

        except Exception as e:
            print(f"Error with client {addr}: {e}")
        
        finally:
            print(f"Closing connection with {addr}")
            writer.close()
            await writer.wait_closed()
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
