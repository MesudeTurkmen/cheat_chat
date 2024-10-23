import socket
import threading

# Socket sunucusu ayarları
HOST = '0.0.0.0'  # Tüm IP'lerden gelen bağlantılara izin verir
PORT = 8080     # Kullanacağınız port

def handle_client(client_socket):
    """Her bir istemciyi (client) ayrı bir thread ile yönetir."""
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Received from client: {data}")
            client_socket.send("Echo: ".encode('utf-8') + data.encode('utf-8'))
        except ConnectionResetError:
            break
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server started, listening on {PORT}")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"New connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
