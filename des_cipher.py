"""
DES (Data Encryption Standard) Implementation
Uses PyCryptodome library for DES encryption/decryption
"""

from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64


class DESCipher:
    def __init__(self, key=None):
        """Initialize DES cipher with an 8-byte key"""
        if key is None:
            self.key = get_random_bytes(8)  # DES key is 8 bytes
        else:
            self.key = key.encode() if isinstance(key, str) else key
            if len(self.key) != 8:
                raise ValueError("DES key must be exactly 8 bytes")
    
    def encrypt(self, plaintext):
        """Encrypt plaintext using DES in CBC mode"""
        cipher = DES.new(self.key, DES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(plaintext.encode(), DES.block_size))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        return iv + ':' + ct
    
    def decrypt(self, ciphertext):
        """Decrypt ciphertext using DES in CBC mode"""
        try:
            iv, ct = ciphertext.split(':')
            iv = base64.b64decode(iv)
            ct = base64.b64decode(ct)
            cipher = DES.new(self.key, DES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), DES.block_size)
            return pt.decode('utf-8')
        except Exception as e:
            return f"Decryption failed: {str(e)}"
