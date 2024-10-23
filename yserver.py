import socket
import threading

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

# Odadaki kullanıcılara mesaj yayar (broadcast)
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

# Sunucuyu başlat
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen()

    print("Server started on port 12345...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
