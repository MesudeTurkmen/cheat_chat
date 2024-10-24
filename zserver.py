import socket
import threading
import os



# Bağlı olan istemciler için bir liste
clients = []
clients_lock = threading.Lock()


#Function to clear the terminal
def clear():
    if os.name== 'nt': #For win
        os.system('cls')
    else: #For lin and mac
        os.system('clear')

# Mesajları tüm bağlı istemcilere yayan fonksiyon
def broadcast(message, sender_socket):
    with clients_lock:
        for client in clients:
            if client != sender_socket:  # Mesajı gönderen istemciye tekrar gönderme
                try:
                    client.sendall(message.encode('utf-8'))
                except:
                    print("unknown error")
                    pass
"""
# İstemciden gelen mesajları işleyen fonksiyon
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                message_decoded = message.decode('utf-8')
                username = message_decoded.split('~')[0]
                msg = message_decoded.split('~')[1]

                final_message = f"{username}~:{msg}"

                print(final_message)
                broadcast(message, client_socket)  # Mesajı diğer istemcilere yay
        except:
            print("Unexpected error")
            pass
"""

def listen_for_messages(client_socket):
    while True:
        message = client_socket.recv(2048).decode('utf-8')
        if message != '':
            username = message.split('~')[0]
            msg = message.split('~')[1]

            final_message = f"{username}~:{msg}"

            print(final_message)
            broadcast(final_message, client_socket)
            #CHAT_HISTORY.append(final_msg)
        else:
            print(f"The message sent from client {username} is empty")



# Sunucuyu başlatma fonksiyonu
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(10)

    print("Sunucu başlatıldı ve bağlantılar bekleniyor...")

    while True:
        client_socket, client_address = server.accept()
        print(f"Yeni bağlantı: {client_address}")

        with clients_lock:
            clients.append(client_socket)

        # Her istemci için yeni bir thread başlat
        client_thread = threading.Thread(target=listen_for_messages, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()

