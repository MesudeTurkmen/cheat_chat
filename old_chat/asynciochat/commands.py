from asyncio.dbwithroles import normal_user, admin_user, superadmin_user

class Command:
    def __init__(self, command_text):
        self.command_text = command_text
        # Komutların yetki adlarına göre eşleşmesi
        self.required_permission = command_text.strip('/')

    def execute(self, user):
        if user.can_execute(self.required_permission):
            print(f"{user.nickname} komut çalıştırıldı: {self.command_text}")
        else:
            print(f"{user.nickname} komutunu çalıştırmak için yetkisi yok: {self.command_text}")


#kick leave create commands oluşturulacak
    def kick(self, user):
        if user.can_execute(self.required_permission):
            pass

# Kullanıcıdan alınan komut örnekleri
commands = ["/join", "/leave", "/createroom", "/kick"]

# Komutları çalıştırma
for cmd in commands:
    command = Command(cmd)
    command.execute(normal_user)       # normaluser için yetki kontrolü
    command.execute(admin_user)        # adminuser için yetki kontrolü
    command.execute(superadmin_user)   # superadminuser için yetki kontrolü
