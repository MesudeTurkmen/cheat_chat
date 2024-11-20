import socket
import threading
import bcrypt
import mysql.connector
import random


class User:

    @staticmethod
    def __database_and_cursor(database_credentials:list):           #Connects to the database and creates the cursor object
        hostname = database_credentials[0]
        user = database_credentials[1]
        passwd = database_credentials[2]
        database = database_credentials[3]

        global my_database, my_cursor
        my_database = mysql.connector.connect(
            host = hostname,
            user = user,
            passwd = passwd,
            database = database
        )

        my_cursor = my_database.cursor()

    def __init__(self, user_credentials):
        full_name = user_credentials[0]                                 #full name
        sequence =  user_credentials[1]                                 #sequence(optional)
        self.user_id = self.__get_unique_id(full_name, sequence)        
        self.username =  user_credentials[2]                            #username
        self.password = self.__hash_passwd(user_credentials[3])
        self.rank = self.__assign_or_check_rank(user_credentials[4])    #rank


    def __hash_passwd(self, password):                      #encrypts the password into a hash
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    

    def __get_unique_id(self, full_name, sequence):         #generates a unique user_id
        name_prefix = self.__generate_name_prefix(full_name)
        if sequence == None:
            sequence = f"{random.randint(0, 255):02X}"
        hex = f"{random.randint(0, 255):03X}"

        user_id = f"{sequence}{name_prefix}{hex}"
        return user_id
    
    
    def __generate_name_prefix(self, full_name):            #generates a name prefx according to the given full_name
        name_list = (full_name.strip()).split(' ')
        name_prefix = []
        for name in name_list:
            name_prefix.append(name.index[0])

        while len(name_prefix) < 3:
            name_prefix.append('0')

        name_prefix = (''.join(name_prefix)).upper()
        return name_prefix
    
    
    def __assign_or_check_rank(self, rank_or_id, key):
        rank_credentials = ['god', 'admin', 'peasent', 'slave', 'arap']
        if key == 'set':
            rank = rank_or_id
            return rank if rank in rank_credentials else None

        elif key == 'check':
            user_id = rank_or_id
            sql = "SELECT user_rank FROM Users WHERE user_id = %s "
            val = (user_id,)
            my_cursor.execute(sql, val)
            user_rank = (my_cursor.fetchone)[0]
            return user_rank
       