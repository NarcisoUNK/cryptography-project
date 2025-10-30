"""
Cryptography Project - Main Entry Point
Implements AES, DES, Playfair, and Vigenère ciphers
"""

from aes_cipher import AESCipher
from des_cipher import DESCipher
from playfair_cipher import PlayfairCipher
from vigenere_cipher import VigenereCipher


def main():
    print("=== Cryptography Project ===")
    print("\nAvailable Ciphers:")
    print("1. AES (Advanced Encryption Standard)")
    print("2. DES (Data Encryption Standard)")
    print("3. Playfair Cipher")
    print("4. Vigenère Cipher")
    
    choice = input("\nSelect cipher (1-4): ")
    
    if choice == "1":
        # AES example
        aes = AESCipher()
        plaintext = input("Enter text to encrypt: ")
        encrypted = aes.encrypt(plaintext)
        print(f"Encrypted: {encrypted}")
        decrypted = aes.decrypt(encrypted)
        print(f"Decrypted: {decrypted}")
    
    elif choice == "2":
        # DES example
        des = DESCipher()
        plaintext = input("Enter text to encrypt: ")
        encrypted = des.encrypt(plaintext)
        print(f"Encrypted: {encrypted}")
        decrypted = des.decrypt(encrypted)
        print(f"Decrypted: {decrypted}")
    
    elif choice == "3":
        # Playfair example
        key = input("Enter key: ")
        playfair = PlayfairCipher(key)
        plaintext = input("Enter text to encrypt: ")
        encrypted = playfair.encrypt(plaintext)
        print(f"Encrypted: {encrypted}")
        decrypted = playfair.decrypt(encrypted)
        print(f"Decrypted: {decrypted}")
    
    elif choice == "4":
        # Vigenère example
        key = input("Enter key: ")
        vigenere = VigenereCipher(key)
        plaintext = input("Enter text to encrypt: ")
        encrypted = vigenere.encrypt(plaintext)
        print(f"Encrypted: {encrypted}")
        decrypted = vigenere.decrypt(encrypted)
        print(f"Decrypted: {decrypted}")
    
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
