import asyncio

class Server():
    def __init__(self,host = '0.0.0.0', port = 6666):
        self.host = host
        self.port = port
        self.server = None
        self.clients = []
  
    async def start_server(self):
        self.server = await asyncio.start_server(
            self.handle_client,
            self.host,
            self.port
        )
        print('server activated...')
    
        async with self.server:
            await self.server.serve_forever()

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Connection established with {addr}")
        self.clients.append(writer)

        try:
            while True:
                data = await reader.read(100)
                message = data.decode()

                if not data:
                    print(f"Connection closed by {addr}")
                    break

                print(f"{addr}: {message}")

                for client in self.clients:
                    if client != writer:
                        client.write(data)
                        await client.drain()
        except Exception as e:
            print(f"Error with client {addr}: {e}")
        
        finally:
            print(f"Closing connection with {addr}")
            writer.close()
            await writer.wait_closed()
            self.client.remove(writer)


    async def stop_server(self,server):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            print('server determinated')
    
    def authenticate_user(nickname, password):
    session = Session()
    user = session.query(User).filter_by(nickname=nickname).first()
    if user and verify_password(password, user.password):
        print("Authentication successful.")
        return True
    else:
        print("Invalid nickname or password.")
        return False


if __name__ == '__main__':
    myServer = Server()
    try:
        asyncio.run(myServer.start_server())
    except KeyboardInterrupt:
        print("Server interrupted by user")