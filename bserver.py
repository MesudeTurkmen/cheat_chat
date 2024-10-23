import socket
import threading

from db_models import session
from db_models.user import User
from sqlalchemy import create_engine
from db_models.base import Base  # db_models içindeki Base sınıfı

# Veritabanı bağlantısı (örneğin SQLite kullanarak)
engine = create_engine('sqlite:///db.sqlite3', echo=True)

# Veritabanındaki tabloları oluştur
Base.metadata.create_all(engine)

print("Veritabanı başarıyla oluşturuldu!")


# Yeni bir kullanıcı oluşturma
new_user = User(nickname="darthmint", password="mint")
new_user = User(nickname="godfry", password="abonque")

# Kullanıcıyı veritabanına ekleme
session.add(new_user)
session.commit()  # Veritabanına kaydet

print("Yeni kullanıcı başarıyla eklendi!")



# Bağlı olan istemciler için bir liste
clients = []
clients_lock = threading.Lock()

# Mesajları tüm bağlı istemcilere yayan fonksiyon
def broadcast(message, sender_socket):
    with clients_lock:
        for client in clients:
            if client != sender_socket:  # Mesajı gönderen istemciye tekrar gönderme
                try:
                    client.send(message)
                except:
                    client.close()
                    clients.remove(client)

# İstemciden gelen mesajları işleyen fonksiyon
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"Gelen mesaj: {message.decode('utf-8')}")
                broadcast(message, client_socket)  # Mesajı diğer istemcilere yay
        except:
            with clients_lock:
                clients.remove(client_socket)
            client_socket.close()
            break

# Sunucuyu başlatma fonksiyonu
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen()

    print("Sunucu başlatıldı ve bağlantılar bekleniyor...")

    while True:
        client_socket, client_address = server.accept()
        print(f"Yeni bağlantı: {client_address}")

        with clients_lock:
            clients.append(client_socket)

        # Her istemci için yeni bir thread başlat
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()