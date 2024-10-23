import socket
import threading
import os

# Chat odalarını tanımla
chat_rooms = {
    "general": [],  # Genel chat odası
    "sports": [],   # Spor chat odası
    "music": []     # Müzik chat odası
}

# Kullanıcıyı bir odaya ekler
def handle_join_room(client_socket, room_name):
    if room_name in chat_rooms:
        chat_rooms[room_name].append(client_socket)
        client_socket.send(f"You joined {room_name} room.".encode())
    else:
        client_socket.send("Room does not exist.".encode())


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
def broadcast_message(room_name, message, sender_socket):
    for client in chat_rooms[room_name]:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                chat_rooms[room_name].remove(client)

# Yeni bir chat odası oluştur
def create_room(room_name):
    if room_name not in chat_rooms:
        chat_rooms[room_name] = []
        print(f"Room {room_name} created.")
    else:
        print("Room already exists.")

# Kullanıcı bir odadan ayrılır
def leave_room(client_socket, room_name):
    if client_socket in chat_rooms[room_name]:
        chat_rooms[room_name].remove(client_socket)
        client_socket.send(f"You left {room_name} room.".encode())

# Her bir kullanıcıya ait thread'i yönet
def handle_client(client_socket):
    client_socket_room = "general"  # Varsayılan olarak 'general' odasına bağla
    chat_rooms[client_socket_room].append(client_socket)
    
    while True:
        try:
            message = client_socket.recv(1024).decode()

            if message.startswith("/join"):
                new_room_name = message.split()[1]
                leave_room(client_socket, client_socket_room)
                handle_join_room(client_socket, new_room_name)
                client_socket_room = new_room_name

            elif message.startswith("/create"):
                new_room_name = message.split()[1]
                create_room(new_room_name)

            elif message == "/leave":
                leave_room(client_socket, client_socket_room)
                client_socket_room = None

            else:
                broadcast_message(client_socket_room, message, client_socket)

        except:
            if client_socket_room:
                leave_room(client_socket, client_socket_room)
            client_socket.close()
            break

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

