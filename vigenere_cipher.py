"""
Vigenère Cipher Implementation
Classical polyalphabetic substitution cipher
"""


class VigenereCipher:
    def __init__(self, key):
        """Initialize Vigenère cipher with a key"""
        self.key = key.upper()
    
    def _extend_key(self, text):
        """Extend key to match text length"""
        key = ""
        key_index = 0
        
        for char in text:
            if char.isalpha():
                key += self.key[key_index % len(self.key)]
                key_index += 1
            else:
                key += char
        
        return key
    
    def encrypt(self, plaintext):
        """Encrypt plaintext using Vigenère cipher"""
        plaintext = plaintext.upper()
        key = self._extend_key(plaintext)
        ciphertext = ""
        
        for i, char in enumerate(plaintext):
            if char.isalpha():
                # Shift character by key
                shift = ord(key[i]) - ord('A')
                encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                ciphertext += encrypted_char
            else:
                ciphertext += char
        
        return ciphertext
    
    def decrypt(self, ciphertext):
        """Decrypt ciphertext using Vigenère cipher"""
        ciphertext = ciphertext.upper()
        key = self._extend_key(ciphertext)
        plaintext = ""
        
        for i, char in enumerate(ciphertext):
            if char.isalpha():
                # Reverse shift by key
                shift = ord(key[i]) - ord('A')
                decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                plaintext += decrypted_char
            else:
                plaintext += char
        
        return plaintext
