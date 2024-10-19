#godfryLib.py 

import random

def setEncryption(): #Assigning random values to string characters thus creating a unique encryption.
    charMain = (
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
        'U', 'V', 'W', 'X', 'Y', 'Z',                           # Uppercase letters
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
        'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
        'u', 'v', 'w', 'x', 'y', 'z',                           # Lowercase letters
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',       # Numbers
        '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
        '-', '_', '=', '+', '[', ']', '{', '}', '\\', '|',
        ';', ':', '\'', '"', ',', '.', '/', '<', '>', '?',
        '`', '~',  # Symbols
        ' ',  # Space
        'Ç', 'Ğ', 'İ', 'Ö', 'Ş', 'Ü',  # Uppercase Turkish characters
        'ç', 'ğ', 'ı', 'ö', 'ş', 'ü',  # Lowercase Turkish characters
    )
    
    char_list = list(charMain) #convert it to a list to shuffle
    random.shuffle(char_list)

    # Create a dictionary for encryption
    encryption_map = {charMain[i]: char_list[i] for i in range(len(charMain))}
    # Create a reverse dictionary for decryption
    decryption_map = {char_list[i]: charMain[i] for i in range(len(charMain))}

    return encryption_map, decryption_map
#________________________________________________________________________________________

def encrypt(encryption_map): #Encrypts the string according to the setEncryption 
    rawTxt = input("your message: ")
    encryptList = []

    for char in rawTxt:
        if char in encryption_map:
            encryptList.append(encryption_map[char]) #encrypting
        
        else:
            print(f"ERROR!! Invalid character '{char}' insterted.")
            input("\nPlease press enter to continue.")
            encrypt(encryption_map)

    # Convert the encrypTxt list to a tuple
    encryptTuple = tuple(encryptList)
    # Convert the tuple to a string
    encrypTxt = ''.join(encryptTuple)

    return encrypTxt
#________________________________________________________________________________________

def decrypt(encrypTxt, decryption_map):
    decryptList = []

    for char in encrypTxt:
        if char in decryption_map:
            decryptList.append(decryption_map[char])  # Decrypting using the map
        else:
            print(f"ERROR!! Invalid character '{char}' during decryption.")  # Handle invalid characters

    decrypTxt = ''.join(decryptList)
    return decrypTxt
#________________________________________________________________________________________

def main():
    encryption_map, decryption_map = setEncryption()
    input("encyption key set...")

    encrypTxt = encrypt(encryption_map)
    decrypTxt = decrypt(encrypTxt, decryption_map)

if __name__ == '__main__':
    main()