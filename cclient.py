import socket
import threading
import os

def clear():
    if os.name== 'nt': #For win
        os.system('cls')
    else: #For lin and mac
        os.system('clear')


# Sunucudan gelen mesajları dinleyen fonksiyon
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                message_decoded = message.decode('utf-8')
                sender_name = message_decoded.split('~')[0]
                msg = message_decoded.split('~')[1]
                final_message = f"{sender_name}~:{msg}"

                print(final_message)
        except:
            print("Bağlantı kesildi.")
            client_socket.close()
            break

# İstemci tarafında sunucuya bağlanma ve mesaj gönderme
def start_client():
    username = input("Enter username: ")
    clear()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('63.176.122.3', 8080))

    # Sunucudan gelen mesajları almak için yeni bir thread başlat
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input(f"{username}: ")
        if message.lower() == "exit":
            break
        client_socket.send(message.encode('utf-8'))

    client_socket.close()

if __name__ == "__main__":
    start_client()
