"""
Vigenère Cipher Implementation
Classical polyalphabetic substitution cipher
"""


class VigenereCipher:
    def __init__(self, key, table=None):
        """Initialize Vigenère cipher with a key and optional custom table"""
        self.key = key.upper()
        self.table = table if table is not None else self._create_standard_table()
    
    def _create_standard_table(self):
        """Create standard Vigenère table (26x26)"""
        table = []
        for i in range(26):
            row = []
            for j in range(26):
                row.append(chr((i + j) % 26 + ord('A')))
            table.append(row)
        return table
    
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
                # Use table for encryption
                row = ord(key[i]) - ord('A')
                col = ord(char) - ord('A')
                encrypted_char = self.table[row][col]
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
                # Use table for decryption - find column in row
                row = ord(key[i]) - ord('A')
                # Find which column gives us the ciphertext character
                for col in range(26):
                    if self.table[row][col] == char:
                        plaintext += chr(col + ord('A'))
                        break
            else:
                plaintext += char
        
        return plaintext
    
    @classmethod
    def from_table(cls, key, table_content):
        """Create VigenereCipher from a table file content"""
        # Parse the table - expecting 26x26 characters
        chars = ''.join(c.upper() for c in table_content if c.isalpha())
        
        if len(chars) != 676:  # 26x26
            raise ValueError(f"Table must contain exactly 676 alphabetic characters (26x26), got {len(chars)}")
        
        # Create 26x26 table
        table = []
        for i in range(26):
            table.append(list(chars[i*26:(i+1)*26]))
        
        return cls(key, table)
