"""
AES (Advanced Encryption Standard) Implementation
Uses PyCryptodome library for AES encryption/decryption
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64


class AESCipher:
    def __init__(self, key=None):
        """Initialize AES cipher with a key (16, 24, or 32 bytes)"""
        if key is None:
            self.key = get_random_bytes(16)  # AES-128
        else:
            self.key = key if isinstance(key, bytes) else key.encode()
    
    def encrypt(self, plaintext):
        """Encrypt plaintext using AES in CBC mode"""
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        return iv + ':' + ct
    
    def decrypt(self, ciphertext):
        """Decrypt ciphertext using AES in CBC mode"""
        try:
            iv, ct = ciphertext.split(':')
            iv = base64.b64decode(iv)
            ct = base64.b64decode(ct)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt.decode('utf-8')
        except Exception as e:
            return f"Decryption failed: {str(e)}"
    
    def encrypt_file(self, data):
        """Encrypt binary file data"""
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        # Return IV + ciphertext as binary
        return cipher.iv + ct_bytes
    
    def decrypt_file(self, data):
        """Decrypt binary file data"""
        # Extract IV (first 16 bytes) and ciphertext
        iv = data[:16]
        ct = data[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt
