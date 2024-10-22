import socket

# Sunucu IP'sini ve portunu belirleyin
SERVER_IP = 'sunucunun-aws-ip-adresi'
SERVER_PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

while True:
    message = input("Enter message to send: ")
    if message.lower() == 'exit':
        break
    client_socket.send(message.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Received from server: {response}")

client_socket.close()
