"""
Cryptography Project - Main Entry Point
Implements AES, DES, Playfair, and Vigenère ciphers
"""

import os
from aes_cipher import AESCipher
from des_cipher import DESCipher
from playfair_cipher import PlayfairCipher
from vigenere_cipher import VigenereCipher


def run_aes():
    """Run AES cipher with file-based operations"""
    print("\n=== AES Cipher ===")
    
    # Read key from file
    key_file = input("Enter key file path: ")
    try:
        with open(key_file, 'r', encoding='ascii') as f:
            key = f.read().strip()
        
        # Validate key length (16, 24, or 32 bytes for AES-128, AES-192, AES-256)
        key_bytes = key.encode('ascii')
        if len(key_bytes) not in [16, 24, 32]:
            print(f"Error: Key must be 16, 24, or 32 bytes (128, 192, or 256 bits). Current length: {len(key_bytes)} bytes")
            return
    except FileNotFoundError:
        print(f"Error: Key file '{key_file}' not found")
        return
    except Exception as e:
        print(f"Error reading key file: {e}")
        return
    
    # Choose operation
    operation = input("Choose operation (1-Encrypt / 2-Decrypt): ")
    
    # Get input file
    input_file = input("Enter input file path: ")
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        return
    
    # Get output file
    output_file = input("Enter output file path: ")
    
    try:
        aes = AESCipher(key_bytes)
        
        if operation == "1":
            # Encrypt - read binary, write binary
            with open(input_file, 'rb') as f:
                data = f.read()
            
            encrypted = aes.encrypt_file(data)
            
            with open(output_file, 'wb') as f:
                f.write(encrypted)
            
            print(f"File encrypted successfully to '{output_file}'")
        
        elif operation == "2":
            # Decrypt - read binary, write binary
            with open(input_file, 'rb') as f:
                data = f.read()
            
            decrypted = aes.decrypt_file(data)
            
            with open(output_file, 'wb') as f:
                f.write(decrypted)
            
            print(f"File decrypted successfully to '{output_file}'")
        else:
            print("Invalid operation")
    
    except Exception as e:
        print(f"Error: {e}")


def run_des():
    """Run DES cipher with file-based operations"""
    print("\n=== DES Cipher ===")
    
    # Read key from file
    key_file = input("Enter key file path: ")
    try:
        with open(key_file, 'r', encoding='ascii') as f:
            key = f.read().strip()
        
        # Validate key length (8 bytes for DES)
        key_bytes = key.encode('ascii')
        if len(key_bytes) != 8:
            print(f"Error: DES key must be exactly 8 bytes. Current length: {len(key_bytes)} bytes")
            return
    except FileNotFoundError:
        print(f"Error: Key file '{key_file}' not found")
        return
    except Exception as e:
        print(f"Error reading key file: {e}")
        return
    
    # Choose operation
    operation = input("Choose operation (1-Encrypt / 2-Decrypt): ")
    
    # Get input file
    input_file = input("Enter input file path: ")
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        return
    
    # Get output file
    output_file = input("Enter output file path: ")
    
    try:
        des = DESCipher(key_bytes)
        
        if operation == "1":
            # Encrypt - read binary, write binary
            with open(input_file, 'rb') as f:
                data = f.read()
            
            encrypted = des.encrypt_file(data)
            
            with open(output_file, 'wb') as f:
                f.write(encrypted)
            
            print(f"File encrypted successfully to '{output_file}'")
        
        elif operation == "2":
            # Decrypt - read binary, write binary
            with open(input_file, 'rb') as f:
                data = f.read()
            
            decrypted = des.decrypt_file(data)
            
            with open(output_file, 'wb') as f:
                f.write(decrypted)
            
            print(f"File decrypted successfully to '{output_file}'")
        else:
            print("Invalid operation")
    
    except Exception as e:
        print(f"Error: {e}")


def run_playfair():
    """Run Playfair cipher with file-based operations"""
    print("\n=== Playfair Cipher ===")
    
    # Read table/matrix from file
    table_file = input("Enter table file path (5x5 matrix): ")
    try:
        with open(table_file, 'r', encoding='ascii') as f:
            table_content = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Table file '{table_file}' not found")
        return
    except Exception as e:
        print(f"Error reading table file: {e}")
        return
    
    # Choose operation
    operation = input("Choose operation (1-Encrypt / 2-Decrypt): ")
    
    # Get input file
    input_file = input("Enter input file path: ")
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        return
    
    # Get output file
    output_file = input("Enter output file path: ")
    
    try:
        # Read message from file (ASCII only)
        with open(input_file, 'r', encoding='ascii') as f:
            message = f.read()
        
        playfair = PlayfairCipher.from_matrix(table_content)
        
        if operation == "1":
            # Encrypt
            result = playfair.encrypt(message)
        elif operation == "2":
            # Decrypt
            result = playfair.decrypt(message)
        else:
            print("Invalid operation")
            return
        
        # Write result to file (ASCII only)
        with open(output_file, 'w', encoding='ascii') as f:
            f.write(result)
        
        operation_name = "encrypted" if operation == "1" else "decrypted"
        print(f"File {operation_name} successfully to '{output_file}'")
    
    except Exception as e:
        print(f"Error: {e}")


def run_vigenere():
    """Run Vigenère cipher with file-based operations"""
    print("\n=== Vigenère Cipher ===")
    
    # Read table from file
    table_file = input("Enter table file path: ")
    try:
        with open(table_file, 'r', encoding='ascii') as f:
            table_content = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Table file '{table_file}' not found")
        return
    except Exception as e:
        print(f"Error reading table file: {e}")
        return
    
    # Read key from file
    key_file = input("Enter key file path: ")
    try:
        with open(key_file, 'r', encoding='ascii') as f:
            key = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Key file '{key_file}' not found")
        return
    except Exception as e:
        print(f"Error reading key file: {e}")
        return
    
    # Choose operation
    operation = input("Choose operation (1-Encrypt / 2-Decrypt): ")
    
    # Get input file
    input_file = input("Enter input file path: ")
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        return
    
    # Get output file
    output_file = input("Enter output file path: ")
    
    try:
        # Read message from file (ASCII only)
        with open(input_file, 'r', encoding='ascii') as f:
            message = f.read()
        
        vigenere = VigenereCipher.from_table(key, table_content)
        
        if operation == "1":
            # Encrypt
            result = vigenere.encrypt(message)
        elif operation == "2":
            # Decrypt
            result = vigenere.decrypt(message)
        else:
            print("Invalid operation")
            return
        
        # Write result to file (ASCII only)
        with open(output_file, 'w', encoding='ascii') as f:
            f.write(result)
        
        operation_name = "encrypted" if operation == "1" else "decrypted"
        print(f"File {operation_name} successfully to '{output_file}'")
    
    except Exception as e:
        print(f"Error: {e}")


def main():
    print("=== Cryptography Project ===")
    print("\nAvailable Ciphers:")
    print("1. AES (Advanced Encryption Standard)")
    print("2. DES (Data Encryption Standard)")
    print("3. Playfair Cipher")
    print("4. Vigenère Cipher")
    
    choice = input("\nSelect cipher (1-4): ")
    
    if choice == "1":
        run_aes()
    elif choice == "2":
        run_des()
    elif choice == "3":
        run_playfair()
    elif choice == "4":
        run_vigenere()
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
