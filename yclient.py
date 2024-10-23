import socket
import threading

# Sunucudan gelen mesajları dinle ve ekrana yazdır
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            print("An error occurred.")
            client_socket.close()
            break

# Mesaj gönderme işlemi
def send_message(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode())
        if message == "/exit":
            client_socket.close()
            break

# Sunucuya bağlan
def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    
    # Thread başlat: Gelen mesajları dinlemek için
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Thread başlat: Mesaj göndermek için
    send_message_thread = threading.Thread(target=send_message, args=(client_socket,))
    send_message_thread.start()

if __name__ == "__main__":
    connect_to_server()
